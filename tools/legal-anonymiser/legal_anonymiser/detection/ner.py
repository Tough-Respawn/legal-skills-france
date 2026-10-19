"""Couche 3 : reconnaissance des noms par le modèle français local (spaCy, fr_core_news_lg).

PER devient PERSONNE, ORG devient SOCIETE, LOC devient COMMUNE (un seul mot capitalisé)
ou LIEU ; MISC est ignoré. Le texte part bloc par bloc, découpé aux fins de paragraphe ou
de phrase quand il dépasse `nlp.max_length`. Les étendues perdent la ponctuation qui les
borde, les articles, mots d'annonce (« société ») et formes sociales placés en tête, et la
forme sociale finale (elle reste visible, spec 6.4). Une entité faite seulement de mots du
vocabulaire (rôles, institutions, intitulés) est ignorée : la sortie va droit au masquage.
Une entité qui contient une ponctuation de phrase (« , », « « », « ( »…) est réduite à sa plus
longue partie propre ; un saut de ligne n'en est pas une (nom coupé en fin de ligne), sauf si chaque
ligne porte deux mots capitalisés hors particules (deux noms) ; deux entités que le modèle coupe à une
particule (« Jean Dupont\\nDe », « La Fontaine ») sont recollées d'abord. En capitales, l'entité s'arrête avant
son premier verbe courant (noms.verb_cut : « AWA SIGNE LE CONTRAT » donne « AWA », « SIGNE HANSEN »
reste entier) ; un verbe en tête d'une société lui appartient (« VERSE SAS »). Les bords et l'intérieur
se jugent sur une liste fixe de mots-outils (noms.FUNCTION_WORDS), jamais sur les mots vides de
spaCy, qui contiennent de vrais noms (« LI HUI MIN »).

Le modèle lit mal les capitales : un bloc dont 60 % des lettres au moins sont des capitales
est lu sur une copie à l'initiale majuscule (même longueur, mêmes positions), et seules
les entités de 2 à 4 mots porteurs, sans mot vide intérieur autre qu'une particule ou « et »
(« TÉMOIN EST PRÉSENT » écarté) ni chiffre (« SOMME DE 300 EUROS » lu LOC), y sont gardées : un mot seul y est souvent un mot courant
(« CI-APRÈS », « DÉNOMMÉ »), au-delà de 4 c'est une clause entière. Une commune d'un seul mot
en capitales n'est donc pas trouvée ici : elle l'est après un code postal, après « NÉ(E) LE …
À » (règles), après « FAIT À » (structure), et ailleurs par propagation de ces mentions ; seule
dans le texte libre, elle reste visible et la seconde passe la signale.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import re
import warnings
from functools import lru_cache
from typing import Iterator, List, Optional, Set, Tuple

from .. import texte
from ..extraction import MissingDependency
from ..modele import Block, Mention
from .noms import (FORMS, FUNCTION_WORDS, GENERIC, NAME_JOINERS, PARTICLE_RX, STOPWORDS, WORD_RX, function_word,
                   known, stem, tokens, verb_cut)

MODEL = "fr_core_news_lg"
_EXCLUDE = ["tagger", "parser", "attribute_ruler", "lemmatizer", "morphologizer", "senter"]
_KINDS = {"PER": "PERSONNE", "ORG": "SOCIETE", "LOC": "LIEU"}
_CAPS_SHARE = 0.6
_CAPS_MAX_WORDS = 4
_FORM_RX = re.compile(FORMS)
_INNER = FUNCTION_WORDS - NAME_JOINERS   # mots-outils jamais à l'intérieur d'un nom
_LINE_RX = re.compile(r"[^\n]+")
_CLEAN_RX = re.compile(r"[^«»“”\"(),;:!?]+")   # parties sans ponctuation de phrase ; un saut de ligne est une espace


class ModelMissing(MissingDependency):
    """Modèle spaCy fr_core_news_lg absent."""


def model_installed() -> bool:
    try:
        return importlib.util.find_spec(MODEL) is not None
    except (ImportError, ValueError):
        return False


def _load():
    """Charge le modèle sans ses composants inutiles, dépendances réduites au silence."""
    if not model_installed():
        raise ModelMissing("Le modèle fr_core_news_lg est requis : python -m spacy download fr_core_news_lg")
    with contextlib.redirect_stderr(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import spacy
        return spacy.load(MODEL, exclude=_EXCLUDE)


_nlp = lru_cache(maxsize=1)(_load)   # un chargement par processus


def _mostly_caps(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and sum(c.isupper() for c in letters) >= _CAPS_SHARE * len(letters)


def _title(text: str) -> str:
    """Initiale majuscule, reste en minuscules, caractère par caractère : longueur conservée."""
    out, prev = [], False
    for c in text:
        x = c.lower() if prev else c.upper()
        out.append(x if len(x) == 1 else c)
        prev = c.isalpha()
    return "".join(out)


def _chunks(text: str, size: int) -> Iterator[Tuple[int, str]]:
    """(position, morceau) de taille au plus size, coupés à un saut de ligne, une fin de phrase ou une espace."""
    start = 0
    while len(text) - start > size:
        window = text[start:start + size]
        cut = max(window.rfind("\n"), window.rfind(". ") + 1)
        if cut <= 0:
            cut = window.rfind(" ")
        if cut <= 0:
            cut = size
        yield start, text[start:start + cut]
        start += cut
    yield start, text[start:]


def _edge(word: str, lead: bool) -> bool:
    """Mot à retirer au bord d'une entité : mot-outil, forme sociale, et en tête mot d'annonce."""
    w = stem(word)
    return (w in STOPWORDS or function_word(word) or _FORM_RX.fullmatch(word) is not None
            or (lead and w in GENERIC))


def _trim(text: str, s: int, e: int) -> Tuple[int, int]:
    """Étendue du premier au dernier mot gardé (ponctuation et chiffres des bords retirés) ; rien
    avant le dernier mot d'annonce intérieur (« Équipe de la Société Duvalcourt Conseil »)."""
    words = list(WORD_RX.finditer(text, s, e))
    inner = [i for i, w in enumerate(words[:-1]) if stem(w.group()) in GENERIC]
    if inner:
        words = words[inner[-1] + 1:]
    while words and _edge(words[0].group(), True):
        words.pop(0)
    while words and _edge(words[-1].group(), False):
        words.pop()
    return (words[0].start(), words[-1].end()) if words else (s, s)


def _clean(text: str, s: int, e: int) -> Tuple[int, int]:
    """Plus longue partie de l'entité entre deux ponctuations de phrase (« Mme Sophie Carrel (gérante »),
    bornée par _trim ; un nom coupé par un saut de ligne reste entier."""
    parts = [_trim(text, m.start(), m.end()) for m in _CLEAN_RX.finditer(text, s, e)]
    return max(parts, key=lambda p: p[1] - p[0], default=(s, s))


def _lines(text: str, s: int, e: int) -> List[Tuple[int, int]]:
    """Une entité sur plusieurs lignes : une ligne qui porte au moins deux mots capitalisés hors particules
    est un nom entier (« Jean Dupont », puis « Marie Durand » à la ligne) ; une autre ligne se rattache à
    la précédente (« Jean-Baptiste » puis « Lemaire », « JEAN DUPONT » puis « DE LA FONTAINE »)."""
    out: List[List] = []   # [début, fin, nom entier ?]
    for m in _LINE_RX.finditer(text, s, e):
        full = sum(w.group()[0].isupper() and not PARTICLE_RX.fullmatch(w.group())
                   for w in WORD_RX.finditer(text, m.start(), m.end())) >= 2
        if out and not (full and out[-1][2]):
            out[-1][1] = m.end()
        else:
            out.append([m.start(), m.end(), full])
    return [_trim(text, a, b) for a, b, _ in out] if len(out) > 1 else [(s, e)]


def _inner_stop(name: str) -> bool:
    """Vrai si un mot-outil autre qu'une liaison de nom (de, la, sur, et…) est à l'intérieur
    (« TÉMOIN EST PRÉSENT ») ; jamais les mots vides de spaCy (« LI HUI MIN » reste un nom)."""
    return any(w.lower().replace("’", "'") in _INNER for w in WORD_RX.findall(name)[1:-1])


def _kind(label: str, name: str, vocab: Set[str], caps: bool) -> Optional[str]:
    """Type de la mention, ou None si l'entité est à ignorer."""
    kind = _KINDS.get(label)
    words = tokens(name)
    if (not kind or len(name) < 2 or not any(c.isalpha() for c in name) or texte.norm(name) in vocab
            or not words or all(known(w, vocab) for w in words)
            or (caps and not 2 <= len(words) <= _CAPS_MAX_WORDS) or (caps and _inner_stop(name))
            or (caps and any(c.isdigit() for c in name))):   # « SOMME DE 300 EUROS » lu LOC : un bout de clause
        return None
    if kind == "LIEU" and len(WORD_RX.findall(name)) == 1 and name[0].isupper():
        return "COMMUNE"
    return kind


def find(blocks: List[Block], vocab: Set[str]) -> List[Mention]:
    """Mentions du modèle (source « ner »), sans résoudre les chevauchements avec les autres couches."""
    nlp = _nlp()
    jobs = []   # (bloc, position du morceau, lu en capitales ?, morceau)
    for bi, block in enumerate(blocks):
        caps = _mostly_caps(block.text)
        source = _title(block.text) if caps else block.text
        jobs += [(bi, base, caps, chunk) for base, chunk in _chunks(source, nlp.max_length)]
    out: List[Mention] = []
    with contextlib.redirect_stderr(io.StringIO()), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        docs = list(nlp.pipe(job[3] for job in jobs))
    for (bi, base, caps, _), doc in zip(jobs, docs):
        text = blocks[bi].text
        for s0, e0, label in _joined(doc):
            s, e = _clean(text, base + s0, base + e0)
            s, e = verb_cut(text, s, e, lead=label != "ORG")   # « VERSE SAS » : un verbe ouvre une société
            for s, e in _lines(text, s, e):
                kind = _kind(label, text[s:e], vocab, caps) if e > s else None
                if kind:
                    out.append(Mention(bi, s, e, kind, "ner"))
    return out


def _joined(doc) -> List[Tuple[int, int, str]]:
    """Entités du modèle (début, fin, étiquette) ; deux entités de même étiquette que seule une espace
    sépare sont recollées quand une particule les joint (« Jean Dupont\\nDe » puis « La Fontaine »)."""
    out: List[List] = []
    for ent in doc.ents:
        words = ent.text.split()
        if (out and out[-1][2] == ent.label_ and not doc.text[out[-1][1]:ent.start_char].strip() and words
                and (PARTICLE_RX.fullmatch(doc.text[out[-1][0]:out[-1][1]].split()[-1]) or PARTICLE_RX.fullmatch(words[0]))):
            out[-1][1] = ent.end_char
        else:
            out.append([ent.start_char, ent.end_char, ent.label_])
    return [(s, e, label) for s, e, label in out]
