"""Réidentification d'un rapport d'analyse écrit sur le texte masqué : le résultat reste dans le coffre."""
from __future__ import annotations

import json
import re
from pathlib import Path

from .coffre import Vault, atomic_write

PLACEHOLDER_RX = re.compile(r"\[[A-Z]+(?:_[A-Z]+)*_\d+\]")


def run(vault: Vault, cid: str, report: Path) -> Path:
    """Remplace chaque placeholder connu de `correspondance.json` ; les autres restent tels quels.

    Écrit `coffre/<id>/rapport-final.md`. Rapport ou table illisible : `OSError` (ou `UnicodeDecodeError`).
    """
    table = json.loads((vault.root / cid / "correspondance.json").read_text("utf-8"))
    text = Path(report).read_text("utf-8")
    out = PLACEHOLDER_RX.sub(lambda m: table.get(m.group(), m.group()), text)
    target = vault.contract_dir(cid) / "rapport-final.md"
    atomic_write(target, out.encode("utf-8"))
    return target
