"""Modèle de données commun à toutes les étapes."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

SECTIONS = ("corps", "entete", "pied", "insertion", "suppression", "commentaire", "cache")

KINDS = (
    "PERSONNE", "SOCIETE", "ADRESSE", "COMMUNE", "LIEU", "EMAIL", "TELEPHONE",
    "IBAN", "BIC", "SIREN", "SIRET", "TVA", "RCS", "NIR", "PIECE_IDENTITE",
    "DATE_NAISSANCE", "IMMATRICULATION", "URL", "NUMERO", "CAPITAL", "AUTRE",
)


@dataclass(frozen=True)
class Block:
    text: str
    location: str
    section: str


@dataclass
class Finding:
    """level : info, attention ou alerte. detail ne contient jamais de texte du document."""
    level: str
    code: str
    location: str
    detail: str = ""


@dataclass
class Extracted:
    blocks: List[Block]
    metadata: Dict[str, str]
    findings: List[Finding]
    ocr: bool = False


@dataclass(frozen=True)
class Mention:
    block: int
    start: int
    end: int
    kind: str
    source: str
    role: Optional[str] = None
    party: Optional[int] = None


@dataclass
class Entity:
    kind: str
    role: Optional[str]
    placeholder: str
    canonical: str
    mentions: List[Mention]


@dataclass
class Ambiguity:
    id: str
    mention: Mention
    candidates: Tuple[str, ...]


@dataclass
class Alert:
    id: str
    block: int
    start: int
    end: int
    text: str
    reason: str


@dataclass
class Decisions:
    keep: Set[Tuple[str, str, int]] = field(default_factory=set)
    resolve: Dict[Tuple[str, str, int], str] = field(default_factory=dict)
    unmask: Set[str] = field(default_factory=set)
    mask_more: Set[str] = field(default_factory=set)
    communes: Dict[str, str] = field(default_factory=dict)
