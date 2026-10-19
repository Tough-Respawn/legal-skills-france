"""Masquage : chaque mention remplacée par son placeholder, de droite à gauche, dans tous les blocs.

Une ambiguïté non tranchée devient `[AMBIGU_<n>]`. Une civilité collée devant une personne
(« M. Kerbrat » propagé depuis « Kerbrat ») part avec elle. Deux étendues qui se chevauchent :
la plus longue l'emporte, puis la plus à gauche. Les blocs rendus gardent leur localisation et
leur section.
"""
from __future__ import annotations

from dataclasses import replace
from typing import Dict, List, Tuple

from .detection.noms import CIV_RX
from .entites import ambiguity_placeholder
from .modele import Ambiguity, Block, Entity, Mention

_CIV_REACH = 40   # longueur maximale d'une civilité (« Mademoiselle et Monsieur »)


def _civility_start(text: str, start: int, floor: int) -> int:
    """Début de la civilité qui finit juste devant start (sans dépasser floor), sinon start."""
    for p in range(max(floor, start - _CIV_REACH), start):
        if p and (text[p - 1].isalnum() or text[p - 1] == "."):
            continue
        m = CIV_RX.match(text, p)
        if m and m.end() == start:
            return p
    return start


def apply(blocks: List[Block], entities: List[Entity], ambiguities: List[Ambiguity]) -> List[Block]:
    """Blocs masqués, dans le même ordre."""
    spans: Dict[int, List[Tuple[Mention, str]]] = {}
    for e in entities:
        for m in e.mentions:
            spans.setdefault(m.block, []).append((m, e.placeholder))
    for a in ambiguities:
        spans.setdefault(a.mention.block, []).append((a.mention, ambiguity_placeholder(a)))
    out = []
    for bi, block in enumerate(blocks):
        chosen: List[Tuple[Mention, str]] = []
        for m, ph in sorted(spans.get(bi, ()), key=lambda x: (x[0].start - x[0].end, x[0].start)):
            if all(m.end <= k.start or k.end <= m.start for k, _ in chosen):
                chosen.append((m, ph))
        chosen.sort(key=lambda x: x[0].start)
        text = block.text
        for i in range(len(chosen) - 1, -1, -1):
            m, ph = chosen[i]
            s = m.start
            if m.kind == "PERSONNE":
                s = _civility_start(text, s, chosen[i - 1][0].end if i else 0)
            text = text[:s] + ph + text[m.end:]
        out.append(replace(block, text=text))
    return out
