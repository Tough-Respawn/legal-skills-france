"""Fichier d'ajustements : les décisions de l'utilisateur, une par ligne, en UTF-8.

    # legal-france ajustements v1, contrat c7f3a2
    A1 ? « Ormeaux » | paragraphe 3 | 1 | majuscule
    M1 ? « M. Kerbrat » | paragraphe 12 | 1 | [LOCATAIRE_1] [LOCATAIRE_2]
    C1 masquer « Valmorin »
    masquer: texte exact
    demasquer: [PLACEHOLDER]

La clé d'une décision se relit sur la ligne : (localisation, texte normalisé, rang). Celle d'une alerte
se calcule sur le texte masqué (comme controle), celle d'une ambiguïté sur le texte d'origine (comme
entites.decide). Une réécriture garde les décisions dont la clé existe encore et liste les autres.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from . import texte
from .entites import Ranks
from .modele import Alert, Ambiguity, Block, Decisions, Entity

NEW = "nouveau"
STALE = "# Décisions périmées (texte modifié) :"
_HEAD_RX = re.compile(r"^([AMC])\d+ (\S+) ")
_QUOTE_RX = re.compile(r"«((?:[^«»]|««|»»)*)»")
_FREE_RX = re.compile(r"^(masquer|demasquer):\s*(.+?)\s*$")


class AdjustmentsError(Exception):
    """Fichier illisible ou mal formé ; le message ne nomme que le chemin neutre."""


def _name(path: Path) -> str:
    return "coffre/%s/ajustements.txt" % path.parent.name


def _quote(s: str) -> str:
    return "« %s »" % s.replace("«", "««").replace("»", "»»")


def _lines(path: Path) -> List[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        raise AdjustmentsError("Fichier d'ajustements illisible : %s." % _name(path)) from None


def _parse(line: str):
    """(type, choix, texte, champs) d'une ligne de décision, ou ('free', 'masquer'|'demasquer', valeur, [])."""
    f = _FREE_RX.match(line)
    h, q = _HEAD_RX.match(line), _QUOTE_RX.search(line)
    if f:
        return "free", f.group(1), f.group(2), []
    if not (h and q):
        return None
    text = q.group(1).strip().replace("««", "«").replace("»»", "»")
    return h.group(1), h.group(2), text, [x.strip() for x in line[q.end():].split(" | ")[1:]]


def _valid(kind: str, choice: str) -> bool:
    return choice in ("masquer", "garder") if kind in "AC" else choice == NEW or bool(re.fullmatch(r"\[[^\]\s]+\]", choice))


def read(path: Path) -> Decisions:
    d = Decisions()
    for line in _lines(path):
        if not line.strip() or line.startswith("#"):
            continue
        p = _parse(line.strip())
        if p is None:
            raise AdjustmentsError("Ligne mal formée dans %s : %s." % (_name(path), line.split(" ")[0][:20]))
        kind, choice, text, fields = p
        if kind == "free":
            (d.mask_more if choice == "masquer" else d.unmask).add(text)
        elif not _valid(kind, choice):
            continue
        elif kind == "C":
            d.communes[texte.norm(text)] = choice if choice == "garder" else d.communes.get(texte.norm(text), "masquer")
        else:
            try:
                key = (fields[0], texte.norm(text), int(fields[1]))
            except (IndexError, ValueError):
                raise AdjustmentsError("Clé illisible dans %s : %s." % (_name(path), line.split(" ")[0])) from None
            if kind == "M":
                d.resolve[key] = choice
            elif choice == "garder":
                d.keep.add(key)
            else:
                d.mask_more.add(text)
    return d


def pending(path: Path) -> int:
    n = 0
    for line in _lines(path):
        p = None if line.startswith("#") else _parse(line.strip())
        n += bool(p) and p[0] != "free" and not _valid(p[0], p[1])
    return n


def write(path: Path, alerts: Sequence[Alert], ambiguities: Sequence[Ambiguity], communes: Sequence[Entity],
          previous: Decisions, *, cid: str, blocks: Optional[Sequence[Block]] = None,
          masked: Optional[Sequence[Block]] = None) -> None:
    out = ["# legal-france ajustements v1, contrat %s" % cid,
           "# Alertes : remplacer ? par masquer ou garder."]
    seen, ranks = set(), Ranks(masked) if alerts else None
    for a in alerts:
        k = ranks.key(a.block, a.start, a.end)
        seen.add(k)
        choice = "garder" if k in previous.keep else "masquer" if a.text in previous.mask_more else "?"
        out.append("%s %s %s | %s | %d | %s" % (a.id, choice, _quote(a.text), k[0], k[2], a.reason))
    out.append("# Mentions ambiguës : remplacer ? par un des placeholders proposés, ou nouveau.")
    ranks = Ranks(blocks) if ambiguities else None
    for m in ambiguities:
        t = m.mention
        k = ranks.key(t.block, t.start, t.end)
        seen.add(k)
        out.append("%s %s %s | %s | %d | %s" % (m.id, previous.resolve.get(k, "?"), _quote(blocks[t.block].text[t.start:t.end]),
                                                 k[0], k[2], " ".join(m.candidates)))
    out.append("# Communes, masquées par défaut : garder si la commune est utile à l'analyse.")
    for i, e in enumerate(communes, 1):
        keep = previous.communes.get(texte.norm(e.canonical)) == "garder"
        out.append("C%d %s %s" % (i, "garder" if keep else "masquer", _quote(e.canonical)))
    out.append("# Ajouts libres :")
    shown = {a.text for a in alerts}
    out += ["masquer: %s" % t for t in sorted(previous.mask_more - shown)]
    out += ["demasquer: %s" % p for p in sorted(previous.unmask)]
    stale = [k for k in sorted(previous.keep | set(previous.resolve)) if k not in seen]
    if stale:
        out += [STALE] + ["#   %s (%s, rang %d)" % (k[1], k[0], k[2]) for k in stale]
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
