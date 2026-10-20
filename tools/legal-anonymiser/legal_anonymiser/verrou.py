"""Verrou Claude Code : hook `PreToolUse` qui refuse l'accès aux originaux inscrits et au coffre.

Lancé par Claude Code (`python -P -m legal_anonymiser.verrou --coffre <racine>`), événement JSON sur
l'entrée standard. Refus = code 0 et décision JSON `deny` sur la sortie standard : Claude Code montre
alors la raison seule (avec le code 2, il la préfixe de la ligne de commande du hook, chemins absolus
compris, constaté le 2026-10-20). Sortie vide et code 0 = laissé passer. Toute exception vaut refus,
par la même décision JSON avec un message générique ; le code 2 (message générique sur l'erreur
standard) ne sert que si la décision elle-même ne peut pas être écrite. Aucun
contenu de fichier n'est lu, seuls des chemins sont comparés, résolus et normalisés. Les messages ne
contiennent jamais un chemin absolu ni un nom de fichier.
Bibliothèque standard uniquement : ce module ne dépend d'aucun autre module du paquet.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Iterable, List, Optional, Tuple

FILE_TOOLS = ("Read", "Edit", "Write", "NotebookEdit")
SEARCH_TOOLS = ("Grep", "Glob")
SHELL_TOOLS = ("Bash", "PowerShell")
ORIGINAL = ("legal-france : original protégé, accès refusé. Travaillez uniquement sur le fichier publié "
            "contrat-<id>.masque.md.")
COFFRE = "legal-france : coffre protégé, accès refusé. Le coffre n'est jamais lu par le modèle."
SEARCH = ("legal-france : recherche refusée, un original protégé ou le coffre se trouve dans ce dossier ou en "
          "dessous : lancez la recherche dans un sous-dossier qui ne les contient pas.")
GENERIC = "legal-france : verrou en erreur, accès refusé par précaution."
_WIN_PATH_RX = re.compile(r"[A-Za-z]:[\\/][^\s\"'<>|;&`]*")
_WILDCARD_RX = re.compile(r"[*?\[]")


def _long_name(path: str) -> str:
    if sys.platform != "win32":
        return path
    import ctypes
    buf = ctypes.create_unicode_buffer(32768)
    n = ctypes.windll.kernel32.GetLongPathNameW(path, buf, 32768)
    return buf.value if 0 < n < 32768 else path


def _norm(path: str) -> str:
    """Chemin résolu (liens, jonctions, noms courts) et normalisé (casse, séparateurs)."""
    real = _long_name(os.path.realpath(path))
    norm = os.path.normcase(real)
    return norm.lower() if sys.platform == "darwin" else norm


def _within(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def _originals(coffre: str) -> List[Tuple[str, str]]:
    """(chemin normalisé, nom de fichier en minuscules) de chaque original inscrit ; registre absent = aucun."""
    try:
        with open(os.path.join(coffre, "registre.json"), encoding="utf-8") as fh:
            reg = json.load(fh)
    except FileNotFoundError:
        return []
    return [(_norm(p), str(e["nom"]).lower()) for p, e in reg["originaux"].items()]


def _flat(text: str) -> str:
    """Minuscules, `\\` et `/` confondus, séquences de séparateurs réduites (`C:\\\\Users` échappé compris)."""
    return re.sub(r"/+", "/", text.replace("\\", "/")).lower()


def _gitbash(path: str) -> str:
    """`C:/Users/x` → `/c/users/x` ; inchangé hors Windows."""
    flat = _flat(path)
    return "/" + flat[0] + flat[2:] if re.match(r"[a-z]:/", flat) else flat


def _shell_forms(command: str, coffre: str, originals: Iterable[Tuple[str, str]]) -> Optional[str]:
    flat = _flat(command)
    for path in _WIN_PATH_RX.findall(command):   # jetons absolus résolus (noms 8.3, liens)
        try:
            flat += " " + _flat(_norm(path))
        except (OSError, ValueError):
            continue
    for path, name in originals:
        if _flat(path) in flat or _gitbash(path) in flat or name in flat:
            return ORIGINAL
    if _flat(coffre) in flat or _gitbash(coffre) in flat or ".legal-france" in flat:
        return COFFRE
    return None


def decide(event: dict, coffre) -> Optional[str]:
    """Message de refus, ou None si l'appel peut passer."""
    tool = event.get("tool_name")
    inp = event.get("tool_input") or {}
    cwd = event.get("cwd") or os.getcwd()
    root = _norm(str(coffre))
    if tool in SHELL_TOOLS:
        command = inp.get("command")
        return _shell_forms(command, root, _originals(root)) if command else None
    originals = _originals(root)
    if tool in FILE_TOOLS:
        target = inp.get("file_path") or inp.get("notebook_path")
        if not target:
            return None
        path = _norm(os.path.join(cwd, target))
        if _within(path, root):
            return COFFRE
        return ORIGINAL if any(path == o for o, _ in originals) else None
    if tool in SEARCH_TOOLS:
        roots = [_norm(os.path.join(cwd, inp.get("path") or "."))]
        prefix = _WILDCARD_RX.split(inp.get("pattern") or "")[0]
        if os.path.isabs(prefix):
            roots.append(_norm(prefix))
        for base in roots:
            if _within(base, root):
                return COFFRE
            if _within(root, base) or any(_within(o, base) for o, _ in originals):
                return SEARCH
    return None


def _write(stream, text: str) -> None:
    raw = getattr(stream, "buffer", None)   # UTF-8 quel que soit le codage de la console Windows
    if raw is not None:
        raw.write(text.encode("utf-8"))
        raw.flush()
    else:
        stream.write(text)
        stream.flush()


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:   # type: ignore[override]
        raise ValueError("arguments")   # rien sur l'erreur standard : le refus passe par la décision JSON


def main(argv: Optional[List[str]] = None) -> int:
    try:
        parser = _Parser(prog="legal_anonymiser.verrou", add_help=False)
        parser.add_argument("--coffre", required=True)
        args = parser.parse_args(argv)
        message = decide(json.load(sys.stdin), args.coffre)
    except BaseException:   # SystemExit d'argparse compris : jamais de laisser-passer
        message = GENERIC
    if message is None:
        return 0
    try:   # une seule écriture : jamais deux objets JSON ; json.dumps échappe en ASCII
        _write(sys.stdout, json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": message}}) + "\n")
        return 0
    except BaseException:   # sortie standard inutilisable : refus par le code 2
        try:
            _write(sys.stderr, GENERIC + "\n")
        except BaseException:
            pass
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
