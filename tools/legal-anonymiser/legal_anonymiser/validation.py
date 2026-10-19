"""Validation humaine : ouverture locale des fichiers relus, puis question posée à l'utilisateur.

Le modèle ne peut pas répondre à sa place : la réponse vient d'une boîte de dialogue native
(`tkinter`) ou, à défaut, d'un terminal interactif. Jamais d'une variable d'environnement, d'un
argument, d'un fichier ni d'un tube. Aucune sortie console ici en dehors de la question elle-même.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Callable, List, Sequence

QUESTION = "Relisez les fichiers ouverts. Publier ce contrat masqué ?"
CHOICES = ("publier", "ajuster", "abandonner")
IMPOSSIBLE = "impossible"
_ABANDON = "abandonner"


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


def _dialog(tk, question: str, choices: Sequence[str]) -> str:
    """Fenêtre à un bouton par choix ; fermer la fenêtre vaut abandon. Aucun bouton n'a le focus."""
    answer = [_ABANDON]
    root = tk.Tk()
    try:
        root.title("legal-france")
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        tk.Label(root, text=question, wraplength=420, justify="left", padx=20, pady=16).pack()
        row = tk.Frame(root)
        row.pack(padx=20, pady=(0, 16))
        for choice in choices:
            def pick(c: str = choice) -> None:
                answer[0] = c
                root.destroy()
            tk.Button(row, text=choice.capitalize(), width=12, command=pick).pack(side="left", padx=6)
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
    numbered = ", ".join("%d %s" % (i, c) for i, c in enumerate(choices, 1))
    while True:
        try:
            reply = input("%s (%s) : " % (question, numbered)).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return _ABANDON
        for i, c in enumerate(choices, 1):
            if reply in (c, str(i)):
                return c


def default_ask(question: str, choices: Sequence[str]) -> str:
    """Boîte de dialogue `tkinter` ; sans elle, saisie clavier si stdin et stdout sont des terminaux.

    Sinon `impossible` : lancé par un outil du modèle sans dialogue ni terminal, rien n'est publié.
    """
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


def confirm(files: List[Path], *, open_file: Callable[[Path], None] = default_open,
            ask: Callable[[str, Sequence[str]], str] = default_ask) -> str:
    """Ouvre chaque fichier, puis demande : `publier`, `ajuster`, `abandonner` ou `impossible`.

    Aucun paramètre ne peut accepter à la place de l'utilisateur. `open_file` et `ask` n'existent
    que pour les tests : la CLI ne passe jamais autre chose que les valeurs par défaut.
    Une réponse inattendue vaut abandon.
    """
    for f in files:
        open_file(Path(f))
    answer = ask(QUESTION, CHOICES)
    return answer if answer in CHOICES or answer == IMPOSSIBLE else _ABANDON
