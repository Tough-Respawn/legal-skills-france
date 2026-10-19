"""Couche 3 : reconnaissance des noms par le modèle français local (spaCy, fr_core_news_lg).

PER devient PERSONNE, ORG devient SOCIETE, LOC devient COMMUNE (un seul mot capitalisé)
ou LIEU ; MISC est ignoré. Le texte part bloc par bloc, découpé aux fins de paragraphe ou
de phrase quand il dépasse `nlp.max_length`. Les étendues perdent la ponctuation qui les
borde, les articles, mots d'annonce (« société ») et formes sociales placés en tête, et la
forme sociale finale (elle reste visible, spec 6.4). Une entité faite seulement de mots du
vocabulaire (rôles, institutions, intitulés) est ignorée : la sortie va droit au masquage.

Le modèle lit mal les capitales : un bloc dont 60 % des lettres au moins sont des capitales
est lu sur une copie à l'initiale majuscule (même longueur, mêmes positions), et seules
les entités de 2 à 4 mots porteurs y sont gardées : un mot seul y est souvent un mot courant
(« CI-APRÈS », « DÉNOMMÉ »), au-delà de 4 c'est une clause entière. Les communes en capitales
restent couvertes par les règles (code postal, « NÉ LE … À ») et la structure (« FAIT À »).
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
from .noms import FORMS, GENERIC, STOPWORDS, WORD_RX, known, stem, tokens

MODEL = "fr_core_news_lg"
_EXCLUDE = ["tagger", "parser", "attribute_ruler", "lemmatizer", "morphologizer", "senter"]
_KINDS = {"PER": "PERSONNE", "ORG": "SOCIETE", "LOC": "LIEU"}
_CAPS_SHARE = 0.6
_CAPS_MAX_WORDS = 4
_FORM_RX = re.compile(FORMS)


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
    """Mot à retirer au bord d'une entité : mot vide, forme sociale, et en tête mot d'annonce."""
    from spacy.lang.fr.stop_words import STOP_WORDS
    w = stem(word)
    return (w in STOPWORDS or word.lower() in STOP_WORDS or _FORM_RX.fullmatch(word) is not None
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


def _kind(label: str, name: str, vocab: Set[str], caps: bool) -> Optional[str]:
    """Type de la mention, ou None si l'entité est à ignorer."""
    kind = _KINDS.get(label)
    words = tokens(name)
    if (not kind or len(name) < 2 or not any(c.isalpha() for c in name) or texte.norm(name) in vocab
            or not words or all(known(w, vocab) for w in words)
            or (caps and not 2 <= len(words) <= _CAPS_MAX_WORDS)):
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
        for ent in doc.ents:
            s, e = _trim(text, base + ent.start_char, base + ent.end_char)
            kind = _kind(ent.label_, text[s:e], vocab, caps) if e > s else None
            if kind:
                out.append(Mention(bi, s, e, kind, "ner"))
    return out
