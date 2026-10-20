"""Validation humaine : ouverture locale des fichiers relus, puis question posée à l'utilisateur.

Le modèle ne peut pas répondre à sa place : la réponse vient d'une boîte de dialogue du système
(`TaskDialogIndirect` sous Windows, `osascript` sous macOS), sinon de `tkinter`, sinon d'un terminal
interactif. Jamais d'une variable d'environnement, d'un argument, d'un fichier ni d'un tube. Aucune
sortie console ici en dehors de la question elle-même.
"""
from __future__ import annotations

import ctypes
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable, List, Optional, Sequence

QUESTION = "Relisez les fichiers ouverts. Publier ce contrat masqué ?"
CHOICES = ("publier", "ajuster", "abandonner")
IMPOSSIBLE = "impossible"
_ABANDON = "abandonner"
TITLE = "legal-france"

# Constantes commctrl.h : identifiants de boutons (jamais IDOK=1, qu'Entrée pourrait viser), croix active.
TDF_ALLOW_DIALOG_CANCELLATION = 0x0008
IDCANCEL = 2
_BUTTON_IDS = {"publier": 101, "ajuster": 102, "abandonner": 103}
_PCWSTR = ctypes.c_wchar_p
_HANDLE = ctypes.c_void_p


class TASKDIALOG_BUTTON(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("nButtonID", ctypes.c_int), ("pszButtonText", _PCWSTR)]


class TASKDIALOGCONFIG(ctypes.Structure):
    _pack_ = 1   # commctrl.h entoure ces structures de pshpack1.h
    _fields_ = [
        ("cbSize", ctypes.c_uint), ("hwndParent", _HANDLE), ("hInstance", _HANDLE),
        ("dwFlags", ctypes.c_int), ("dwCommonButtons", ctypes.c_int), ("pszWindowTitle", _PCWSTR),
        ("pszMainIcon", _HANDLE), ("pszMainInstruction", _PCWSTR), ("pszContent", _PCWSTR),
        ("cButtons", ctypes.c_uint), ("pButtons", ctypes.POINTER(TASKDIALOG_BUTTON)),
        ("nDefaultButton", ctypes.c_int), ("cRadioButtons", ctypes.c_uint),
        ("pRadioButtons", ctypes.POINTER(TASKDIALOG_BUTTON)), ("nDefaultRadioButton", ctypes.c_int),
        ("pszVerificationText", _PCWSTR), ("pszExpandedInformation", _PCWSTR),
        ("pszExpandedControlText", _PCWSTR), ("pszCollapsedControlText", _PCWSTR),
        ("pszFooterIcon", _HANDLE), ("pszFooter", _PCWSTR), ("pfCallback", ctypes.c_void_p),
        ("lpCallbackData", ctypes.c_ssize_t), ("cxWidth", ctypes.c_uint),
    ]


class _ACTCTXW(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint), ("dwFlags", ctypes.c_uint), ("lpSource", _PCWSTR),
        ("wProcessorArchitecture", ctypes.c_ushort), ("wLangId", ctypes.c_ushort),
        ("lpAssemblyDirectory", _PCWSTR), ("lpResourceName", _HANDLE), ("lpApplicationName", _PCWSTR),
        ("hModule", _HANDLE),
    ]


def _activate_comctl6() -> bool:
    """Active le manifeste des contrôles communs v6 embarqué dans shell32 (ressource 124), pour le fil courant."""
    try:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        ctx = _ACTCTXW()
        ctx.cbSize = ctypes.sizeof(ctx)
        ctx.dwFlags = 0x0008   # ACTCTX_FLAG_RESOURCE_NAME_VALID
        ctx.lpSource = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "shell32.dll")
        ctx.lpResourceName = 124   # MAKEINTRESOURCE(124) : manifeste des contrôles communs v6
        # HANDLE = c_void_p, ULONG_PTR = c_size_t : sans argtypes, un handle 64 bits lève ArgumentError.
        kernel32.CreateActCtxW.argtypes = [ctypes.POINTER(_ACTCTXW)]
        kernel32.CreateActCtxW.restype = _HANDLE
        kernel32.ActivateActCtx.argtypes = [_HANDLE, ctypes.POINTER(ctypes.c_size_t)]
        kernel32.ActivateActCtx.restype = ctypes.c_int
        handle = kernel32.CreateActCtxW(ctypes.byref(ctx))
        if handle in (None, _HANDLE(-1).value):
            return False
        cookie = ctypes.c_size_t()
        # ponytail: contexte laissé actif jusqu'à la fin du processus (une seule question par passage), donc ni
        # DeactivateActCtx ni ReleaseActCtx ; les déclarer quand une désactivation deviendra utile.
        return bool(kernel32.ActivateActCtx(handle, ctypes.byref(cookie)))
    except (AttributeError, OSError, ValueError, ctypes.ArgumentError):
        return False


def _taskdialog() -> Optional[Callable]:
    """`TaskDialogIndirect` des contrôles communs v6, ou None quand ils sont indisponibles."""
    for attempt in (0, 1):
        try:
            fn = ctypes.WinDLL("comctl32").TaskDialogIndirect
        except (AttributeError, OSError):
            if attempt or not _activate_comctl6():
                return None
            continue
        fn.restype = ctypes.c_long
        return fn
    return None


def _windows_dialog(question: str, choices: Sequence[str]) -> Optional[str]:
    """Boîte de dialogue Windows native : trois boutons, « Abandonner » par défaut, croix = abandon."""
    fn = _taskdialog()
    if fn is None:
        return None
    labels = [c.capitalize() for c in choices]   # gardés vivants jusqu'au retour de l'appel
    buttons = (TASKDIALOG_BUTTON * len(choices))(
        *[TASKDIALOG_BUTTON(_BUTTON_IDS[c], label) for c, label in zip(choices, labels)])
    cfg = TASKDIALOGCONFIG()
    cfg.cbSize = ctypes.sizeof(cfg)
    cfg.dwFlags = TDF_ALLOW_DIALOG_CANCELLATION
    cfg.pszWindowTitle = TITLE
    cfg.pszMainInstruction = question
    cfg.cButtons = len(choices)
    cfg.pButtons = buttons
    cfg.nDefaultButton = _BUTTON_IDS[_ABANDON]
    pressed = ctypes.c_int(0)
    if fn(ctypes.byref(cfg), ctypes.byref(pressed), None, None) != 0:
        return None
    by_id = {v: k for k, v in _BUTTON_IDS.items()}
    answer = by_id.get(pressed.value, _ABANDON)
    return answer if answer in choices else _ABANDON


def _mac_dialog(question: str, choices: Sequence[str]) -> Optional[str]:
    """`display dialog` via `osascript -e`, texte passé en argument (aucun shell), « Abandonner » par défaut."""
    labels = {c.capitalize(): c for c in choices}
    script = ('display dialog %s with title %s buttons {%s} default button "Abandonner" cancel button "Abandonner"'
              % (json.dumps(question, ensure_ascii=False), json.dumps(TITLE),
                 ", ".join(json.dumps(l) for l in reversed(list(labels)))))
    try:
        out = subprocess.run(["osascript", "-e", script], stdin=subprocess.DEVNULL, capture_output=True,
                             text=True, encoding="utf-8")
    except (OSError, ValueError):
        return None
    if out.returncode != 0:   # -128 « User canceled » : bouton Abandonner ou Échap ; autre erreur : repli
        return _ABANDON if "(-128)" in (out.stderr or "") else None
    m = re.search(r"button returned:(\S+)", out.stdout or "")
    return labels.get(m.group(1), _ABANDON) if m else _ABANDON


def _native(question: str, choices: Sequence[str]) -> Optional[str]:
    if sys.platform == "win32":
        return _windows_dialog(question, choices)
    if sys.platform == "darwin":
        return _mac_dialog(question, choices)
    return None


def default_open(path: Path) -> None:
    """Ouvre `path` avec l'application par défaut du système, sans attendre.

    Seul sous-processus autorisé avec l'OCR (spec 6.6, 6.10). Un échec est ignoré : la question est
    posée quand même, l'utilisateur peut ouvrir le coffre lui-même.
    """
    try:
        if sys.platform == "win32":
            os.startfile(str(path))
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.Popen([opener, str(path)], stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def _ignore(_event: object) -> str:
    return "break"


def _dialog(tk, question: str, choices: Sequence[str]) -> str:
    """Fenêtre à un bouton par choix ; fermer la fenêtre vaut abandon.

    Seul un clic publie : aucun bouton n'a le focus au départ, « Publier » est hors de l'ordre de
    tabulation (Tab puis Espace ne peut pas l'atteindre), Entrée ne déclenche aucun bouton, et la
    commande Tk `send` est retirée pour qu'une autre application Tk ne puisse pas cliquer à distance.
    """
    answer = [_ABANDON]
    root = tk.Tk()
    try:
        try:
            root.tk.call("rename", "send", "")
        except tk.TclError:
            pass  # `send` n'existe pas (Windows, macOS) : rien à retirer.
        root.title("legal-france")
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        tk.Label(root, text=question, wraplength=420, justify="left", padx=20, pady=16).pack()
        row = tk.Frame(root)
        row.pack(padx=20, pady=(0, 16))
        for choice in choices:
            def pick(c: str = choice) -> None:
                answer[0] = c
                root.destroy()
            extra = {"takefocus": 0} if choice == "publier" else {}
            button = tk.Button(row, text=choice.capitalize(), width=12, command=pick, **extra)
            button.bind("<Return>", _ignore)
            button.bind("<KP_Enter>", _ignore)
            button.pack(side="left", padx=6)
        root.attributes("-topmost", True)
        root.lift()
        root.focus_force()
        root.mainloop()
    finally:
        try:
            root.destroy()
        except tk.TclError:
            pass
    return answer[0]


def _interactive() -> bool:
    # ponytail: sous Windows, NUL est un périphérique caractère et isatty() y répond vrai ;
    # input() y lit alors une fin de fichier, donc « abandonner », jamais « publier ».
    try:
        return bool(sys.stdin and sys.stdout and sys.stdin.isatty() and sys.stdout.isatty())
    except (ValueError, OSError):
        return False


def _terminal(question: str, choices: Sequence[str]) -> str:
    """Le mot entier est exigé (casse indifférente) ; toute autre saisie, vide comprise, redemande."""
    while True:
        try:
            reply = input("%s (tapez %s) : " % (question, ", ".join(choices))).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return _ABANDON
        if reply in choices:
            return reply


def default_ask(question: str, choices: Sequence[str]) -> str:
    """Dialogue natif du système, sinon `tkinter`, sinon saisie clavier si stdin et stdout sont des terminaux.

    Sinon `impossible` : lancé par un outil du modèle sans dialogue ni terminal, rien n'est publié.
    """
    try:
        answer = _native(question, choices)
    except Exception:
        answer = None
    if answer is not None:
        return answer
    try:
        import tkinter
    except ImportError:
        tkinter = None
    if tkinter is not None:
        try:
            return _dialog(tkinter, question, choices)
        except tkinter.TclError:
            pass
    return _terminal(question, choices) if _interactive() else IMPOSSIBLE


def confirm(files: List[Path], *, question: str = QUESTION, open_file: Callable[[Path], None] = default_open,
            ask: Callable[[str, Sequence[str]], str] = default_ask) -> str:
    """Ouvre chaque fichier, puis demande : `publier`, `ajuster`, `abandonner` ou `impossible`.

    Aucun paramètre ne peut accepter à la place de l'utilisateur. `question` n'est que le texte
    affiché : la CLI y place l'identifiant neutre du contrat (jamais une valeur du document).
    `open_file` et `ask` n'existent que pour les tests : la CLI ne passe jamais autre chose que les
    valeurs par défaut. Une réponse inattendue vaut abandon.
    """
    for f in files:
        open_file(Path(f))
    answer = ask(question, CHOICES)
    return answer if answer in CHOICES or answer == IMPOSSIBLE else _ABANDON
