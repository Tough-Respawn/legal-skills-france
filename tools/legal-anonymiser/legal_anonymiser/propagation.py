"""Formes d'une entité et recherche sans casse ni accents, positions d'origine conservées.

Une personne porte sa forme complète sans civilité, « prénom nom » et « nom prénom », son nom
seul (dernier mot, ou mots en capitales quand le nom en a ; particules comprises ou non), son
premier prénom seul s'il a au moins 3 lettres, et ses initiales (« J.-P. D. », « J.-P. Dupont »,
« J. Dupont », « JP Dupont ») ; un mot seul n'est jamais un mot vide ni un mot du vocabulaire.
Une société porte son nom, avec et sans article en tête (la forme sociale en est déjà exclue).
Une commune ou un lieu porte son nom. Les autres types (numéros, montants, adresses) ne se
propagent pas : un « 12 » ou un capital répétés ailleurs ne sont pas des identifiants.
"""
from __future__ import annotations

import re
import unicodedata
from functools import lru_cache
from typing import List, Set, Tuple

from . import texte
from .detection.noms import (CAPS_VERBS, CIVILITY, FUNCTION_WORDS, NAME_JOINERS, PARTICLES, STOPWORDS, caps_verb,
                             function_word, known)
from .detection.regles import SP

Key = Tuple[str, str, int]
Span = Tuple[int, int]
CIV_RX = re.compile(r"(?:" + CIVILITY + SP + r"+(?:et|ET)" + SP + r"+)?" + CIVILITY + SP + r"+")
ARTICLE_RX = re.compile(r"(?i:(?:le|la|les)" + SP + r"+|l['’])")
PARTICLE_RX = re.compile(r"(?i:" + PARTICLES + r")")
WORD_RX = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*")
PROPAGATED = ("PERSONNE", "SOCIETE", "COMMUNE", "LIEU")
BANNED = frozenset(texte.norm(w) for w in FUNCTION_WORDS | CAPS_VERBS)   # jamais une forme d'un mot


@lru_cache(maxsize=None)
def _fold(c: str) -> str:
    return " " if c.isspace() else texte.norm(c)


def folded(text: str) -> Tuple[str, List[int]]:
    """Texte normalisé comme texte.norm (espaces fusionnés) et position d'origine de chaque caractère."""
    out: List[str] = []
    pos: List[int] = []
    for i, c in enumerate(text):
        f = _fold(c)
        if f == " " and out and out[-1] == " ":
            continue
        out.extend(f)
        pos.extend([i] * len(f))
    return "".join(out), pos


@lru_cache(maxsize=4096)
def pattern(form: str) -> "re.Pattern[str]":
    """Forme normalisée bornée : ni lettre, ni chiffre, ni trait d'union autour ; une apostrophe avant
    ne borne pas (« d'Élodie », « qu'Élodie ») ; dans « N'Diaye », au pire, on masque trop."""
    return re.compile(r"(?<![\w-])" + re.escape(form) + r"(?![\w'-])")


def span(text: str, pos: List[int], start: int, end: int) -> Tuple[int, int]:
    """Étendue d'origine des caractères normalisés [start, end), accents combinants finaux compris."""
    s, e = pos[start], pos[end - 1] + 1
    while e < len(text) and unicodedata.combining(text[e]):
        e += 1
    return s, e


def strip_civility(text: str) -> str:
    m = CIV_RX.match(text)
    return text[m.end():] if m and m.end() < len(text) else text


def name_part(kind: str, text: str) -> str:
    return strip_civility(text) if kind == "PERSONNE" else text


def name_words(name: str) -> List[str]:
    """Mots du nom hors particules (de, La, van…)."""
    return [w for w in WORD_RX.findall(name) if not PARTICLE_RX.fullmatch(w)]


def _single(form: str, vocab: Set[str], letters: int) -> bool:
    return (len(re.sub(r"\W", "", form)) >= letters and form not in STOPWORDS and form not in BANNED
            and not known(form, vocab))


def head(name: str, vocab: Set[str]) -> str:
    """Début d'un nom en capitales sur-capturé, avant le premier verbe courant, mot-outil (hors liaisons
    de nom : de, la, sur…) ou mot du vocabulaire : « AWA DUPONT EST TÉMOIN » donne « AWA DUPONT »."""
    kept: list = []
    for w in WORD_RX.finditer(name):
        word = w.group()
        joiner = word.lower().replace("’", "'") in NAME_JOINERS
        if kept and not joiner and (caps_verb(word) or function_word(word) or known(word, vocab)):
            break
        kept.append(w)
    while len(kept) > 1 and kept[-1].group().lower() in NAME_JOINERS:
        kept.pop()
    return name[:kept[-1].end()] if kept else name


def _person(name: str, vocab: Set[str]) -> Set[str]:
    words = WORD_RX.findall(name)
    names = name_words(name)
    out = {texte.norm(name)}
    if not names:
        return out
    caps = [w for w in names if w.isupper() and len(w) > 1]
    surname = caps if caps and len(caps) < len(names) else names[-1:]
    first = [w for w in names if w not in surname]
    sur = texte.norm(" ".join(surname))
    if _single(sur, vocab, 2):
        out.add(sur)
    k = len(words) - 1 - words[::-1].index(surname[-1])
    j = k
    while j > 0 and PARTICLE_RX.fullmatch(words[j - 1]):
        j -= 1
    if j < k:
        out.add(texte.norm(" ".join(words[j:k + 1])))   # « de la fontaine », « le gall »
    if first:
        given = texte.norm(" ".join(first))
        out |= {given + " " + sur, sur + " " + given}
        f0 = texte.norm(first[0])
        if _single(f0, vocab, 3):
            out.add(f0)
        parts = [p for p in f0.split("-") if p]
        dotted = "-".join(p[0] + "." for p in parts)
        out |= {dotted + " " + sur, dotted + " " + sur[0] + ".", parts[0][0] + ". " + sur}
        if len(parts) > 1:
            out.add("".join(p[0] for p in parts) + " " + sur)
    return out


def forms(kind: str, text: str, vocab: Set[str]) -> Set[str]:
    """Formes normalisées sous lesquelles une mention de ce type peut réapparaître."""
    if kind not in PROPAGATED:
        return set()
    if kind == "PERSONNE":
        return _person(strip_civility(text), vocab) - {""}
    out = {texte.norm(text)}
    a = ARTICLE_RX.match(text)
    if kind == "SOCIETE" and a and a.end() < len(text):
        out.add(texte.norm(text[a.end():]))
    return out - {""}
