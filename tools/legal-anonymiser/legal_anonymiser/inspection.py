"""Inspection du format : pièges techniques indépendants du contenu juridique."""
import re
from typing import List, Optional, Sequence

from .modele import Block, Entity, Extracted, Finding
from .texte import mixed_script, norm, strip_traps

_AI_PATTERNS = [re.compile(p, re.IGNORECASE) for p in (
    r"ignore[rz]? (les |toutes les )?(instructions|consignes)",
    r"ignore (all |any )?(previous |prior |the above )?instructions",
    r"(tu es|vous êtes|you are) (un |une |an? )?(ia|assistant|ai|llm|language model|modèle de langage)\b(?!\s+social)",
    r"consid[eè]re[rz]? (que )?ce contrat (est |comme )?conforme",
    r"ne (signale|mentionne)[rz]? (rien|aucun)",
    r"system prompt",
    r"\bLLM\b",
    r"prompt injection",
)]

_MONTHS = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet",
           "aout", "septembre", "octobre", "novembre", "decembre"]
_NUM_DATE = re.compile(r"\b(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})\b")
_TXT_DATE = re.compile(r"\b(1er|\d{1,2})\s+([^\W\d_]+)\s+(\d{4})\b", re.IGNORECASE)
_INITIAL = re.compile(r"^\w\.?$")
_SIGNED = re.compile(r"\bfait\s+à|\bsigné\s+le", re.IGNORECASE)


def clean(extracted: Extracted) -> Extracted:
    """Retire les caractères piégés des blocs et signale chaque bloc touché."""
    blocks: List[Block] = []
    findings = list(extracted.findings)
    for b in extracted.blocks:
        text, zw, bidi = strip_traps(b.text)
        if zw or bidi:
            findings.append(Finding("alerte", "caracteres_invisibles", b.location,
                                    f"zero_width={zw} bidi={bidi}"))
        mixed = sum(1 for w in re.findall(r"\w+", text) if mixed_script(w))
        if mixed:
            findings.append(Finding("alerte", "homoglyphes", b.location, str(mixed)))
        blocks.append(Block(text, b.location, b.section))
    return Extracted(blocks, extracted.metadata, findings, extracted.ocr)


def ai_directed(blocks: Sequence[Block]) -> List[Finding]:
    """Un constat par bloc qui s'adresse à une IA."""
    out = []
    for b in blocks:
        n = sum(len(p.findall(b.text)) for p in _AI_PATTERNS)
        if n:
            out.append(Finding("alerte", "texte_adresse_ia", b.location, str(n)))
    return out


def _dates(text: str) -> List[tuple]:
    """Dates (position, (année, mois, jour)) triées par position."""
    found = []
    for m in _NUM_DATE.finditer(text):
        found.append((m.start(), (int(m.group(3)), int(m.group(2)), int(m.group(1)))))
    for m in _TXT_DATE.finditer(text):
        mois = norm(m.group(2))
        if mois in _MONTHS:
            day = 1 if m.group(1).lower() == "1er" else int(m.group(1))
            found.append((m.start(), (int(m.group(3)), _MONTHS.index(mois) + 1, day)))
    return sorted(found)


def _signature_date(blocks: Sequence[Block]) -> Optional[tuple]:
    last = None
    for b in blocks:
        mark = _SIGNED.search(b.text)
        if mark:
            ds = _dates(b.text)
            after = [d for pos, d in ds if pos >= mark.start()]
            if after:
                last = after[0]
            elif ds:
                last = ds[-1][1]
    return last


def _iso_date(value: str) -> Optional[tuple]:
    m = re.match(r"\s*(\d{4})-(\d{2})-(\d{2})", value or "")
    return tuple(int(g) for g in m.groups()) if m else None


def _contains_word(haystack: str, needle: str) -> bool:
    return re.search(r"(?<!\w)" + re.escape(needle) + r"(?!\w)", haystack) is not None


def metadata_findings(extracted: Extracted, entities: Sequence[Entity]) -> List[Finding]:
    """Métadonnées postérieures à la signature ou portant le nom d'une partie."""
    out: List[Finding] = []
    meta = extracted.metadata
    sig = _signature_date(extracted.blocks)
    if sig:
        for key in ("cree", "modifie"):
            d = _iso_date(meta.get(key, ""))
            if d and d > sig:
                out.append(Finding("attention", "metadonnees_posterieures", "métadonnées", key))
    values = [v for v in (norm(meta.get(k) or "") for k in ("auteur", "modifie_par", "societe")) if v]
    for ent in entities:
        names = {norm(ent.canonical)}
        for m in ent.mentions:
            names.add(norm(extracted.blocks[m.block].text[m.start:m.end]))
        names.discard("")
        if any(v == n or (len(v) >= 3 and not _INITIAL.match(v) and _contains_word(n, v)) for v in values for n in names):
            out.append(Finding("info", "auteur_partie", "métadonnées", ent.placeholder))
    return out
