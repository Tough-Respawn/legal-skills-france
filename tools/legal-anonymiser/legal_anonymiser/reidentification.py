"""Réidentification d'un rapport d'analyse écrit sur le texte masqué : le résultat reste dans le coffre."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .coffre import Vault, atomic_write
from .rendu import MARKER_RE


class SansPublication(Exception):
    """Rapport dont la première ligne n'est pas le marqueur d'une version publiée de ce contrat."""


def run(vault: Vault, cid: str, report: Path) -> Path:
    """Remplace chaque placeholder de la table figée à la publication (les siens seulement, le plus long
    d'abord) ; tout autre texte, `[INCONNU_1]` ou `[IMAGE]` compris, reste tel quel.

    La première ligne du rapport doit être celle du fichier publié (marqueur de ce contrat avec `corps=` et
    `passage=`) : elle désigne `coffre/<id>/publications/<passage>.json`. Ligne absente, autre contrat,
    passage jamais publié ou marqueur sans ces champs : `SansPublication`, rien n'est écrit. La table de
    travail (`correspondance.json`, réécrite à chaque passage) n'est jamais lue.

    Écrit `coffre/<id>/rapport-final.md`. Rapport ou table illisible : `OSError` (ou `UnicodeDecodeError`).
    """
    text = Path(report).read_text("utf-8")
    m = MARKER_RE.match(text.split("\n", 1)[0].rstrip("\r").lstrip("﻿"))
    if not (m and m.group("id") == cid and m.group("corps") and m.group("passage")
            and vault.was_published(cid, m.group("corps"), m.group("passage"))):
        raise SansPublication()
    snapshot = vault.root / cid / "publications" / ("%s.json" % m.group("passage"))
    if not snapshot.is_file():
        raise SansPublication()
    table = json.loads(snapshot.read_text("utf-8"))
    out = text
    if table:
        rx = re.compile("|".join(re.escape(k) for k in sorted(table, key=len, reverse=True)))
        out = rx.sub(lambda m: table[m.group()], text)
    target = vault.contract_dir(cid) / "rapport-final.md"
    atomic_write(target, out.encode("utf-8"))
    return target
