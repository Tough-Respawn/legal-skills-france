"""Installation du verrou Claude Code dans `settings.json` : une entrée `PreToolUse`, sauvegarde, réversible.

Le fichier de réglages est rechargé en JSON et réécrit avec une indentation de 2 : tout ce qui n'est
pas notre entrée est conservé. Un fichier qui n'est pas du JSON valide (commentaires compris) est
refusé sans écriture. Rien à changer = rien d'écrit, la sauvegarde garde l'état précédent.
Format du hook : https://code.claude.com/docs/en/hooks, relue le 2026-10-20 (`args` = forme exec,
sans shell ; `onFailure: "block"` à partir de v2.1.295 ; `timeout` en secondes).
"""
from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from .coffre import atomic_write

MIN_VERSION = (2, 1, 295)   # `onFailure: "block"`, https://code.claude.com/docs/en/hooks lue le 2026-10-20
MARK = "legal_anonymiser.verrou"
MATCHER = "Read|Edit|Write|NotebookEdit|Grep|Glob|Bash|PowerShell"
BACKUP_SUFFIX = ".legal-france.bak"
# `-P` (Python 3.11+) : le dossier de la session n'entre pas dans `sys.path`, un `json.py` du projet ne
# remplace pas le verrou. En 3.9 et 3.10, pas d'équivalent qui garde une installation `pip install --user`.
ISOLATE = ["-P"] if sys.version_info >= (3, 11) else []
_VERSION_RX = re.compile(r"(\d+)\.(\d+)\.(\d+)")


class VersionTooOld(Exception):
    """Claude Code absent ou antérieur à 2.1.295 : le verrou laisserait passer en cas de panne."""


class SettingsInvalid(Exception):
    """`settings.json` n'est pas un objet JSON valide : rien n'est écrit."""


def claude_version() -> Optional[str]:
    exe = shutil.which("claude")
    if not exe:
        return None
    try:
        out = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    m = _VERSION_RX.search(out.stdout or "")
    return m.group(0) if out.returncode == 0 and m else None


def check_version(version: Optional[str]) -> None:
    m = _VERSION_RX.search(version or "")
    if not m or tuple(int(x) for x in m.groups()) < MIN_VERSION:
        raise VersionTooOld()


def _is_ours(hook: object) -> bool:
    return isinstance(hook, dict) and MARK in (hook.get("args") or [])


def _ours(entry: dict) -> bool:
    return any(_is_ours(h) for h in entry.get("hooks", []))


def _load(settings: Path) -> dict:
    try:
        data = json.loads(settings.read_text("utf-8-sig"))   # BOM toléré (Bloc-notes)
    except FileNotFoundError:
        return {}
    except (ValueError, UnicodeDecodeError):
        raise SettingsInvalid() from None
    hooks = data.get("hooks", {}) if isinstance(data, dict) else None
    if not isinstance(hooks, dict) or not isinstance(hooks.get("PreToolUse", []), list):
        raise SettingsInvalid()
    return data


def _save(settings: Path, data: dict) -> None:
    if settings.exists():
        shutil.copyfile(settings, settings.with_name(settings.name + BACKUP_SUFFIX))
    settings.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(settings, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def _entry(coffre: Path) -> dict:
    return {"matcher": MATCHER, "hooks": [{
        "type": "command", "command": sys.executable,
        "args": ISOLATE + ["-m", MARK, "--coffre", str(Path(coffre).resolve())],
        "onFailure": "block", "timeout": 10,
    }]}


def _without_ours(data: dict) -> dict:
    """Retire notre objet hook de chaque entrée ; une entrée n'est retirée que si elle devient vide."""
    data = copy.deepcopy(data)
    hooks = data.get("hooks")
    entries = (hooks or {}).get("PreToolUse", [])
    kept = []
    for e in entries:
        inner = e.get("hooks") if isinstance(e, dict) else None
        if not (isinstance(inner, list) and any(_is_ours(h) for h in inner)):
            kept.append(e)
        elif any(not _is_ours(h) for h in inner):
            kept.append(dict(e, hooks=[h for h in inner if not _is_ours(h)]))
    if kept != entries:   # nettoyage seulement si un hook à nous est retiré
        hooks["PreToolUse"] = kept
        if not kept:
            del hooks["PreToolUse"]
        if not hooks:
            del data["hooks"]
    return data


def install(settings: Path, coffre: Path, version: Optional[str]) -> str:
    """`installé` ou `inchangé` (entrée déjà présente, identique et en dernière position)."""
    check_version(version)
    settings = Path(settings).resolve()   # lien symbolique (dotfiles) : on écrit la cible, le lien reste
    before = _load(settings)
    data = _without_ours(before)
    data.setdefault("hooks", {}).setdefault("PreToolUse", []).append(_entry(coffre))
    if data == before:
        return "inchangé"
    _save(settings, data)
    return "installé"


def uninstall(settings: Path) -> str:
    """`retiré` ou `absent` (aucune entrée à nous, fichier absent compris : rien n'est écrit)."""
    settings = Path(settings).resolve()
    before = _load(settings)
    data = _without_ours(before)
    if data == before:
        return "absent"
    _save(settings, data)
    return "retiré"
