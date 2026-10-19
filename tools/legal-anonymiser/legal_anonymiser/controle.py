"""Seconde passe : relecture du texte masqué, dernier filet avant la validation humaine.

Chaque alerte porte sur le texte masqué ; identifiants A1, A2… dans l'ordre du document. Motifs :
1. valeur_connue : valeur d'une entité (forme canonique et ses formes, propagation.forms ; texte de
   chaque mention si les blocs d'origine sont donnés) retrouvée sans casse ni accents, minuscules
   comprises (« le dossier kerbrat ») ; jamais exemptée, même par une décision garder. Une valeur de
   moins de 3 caractères, un placeholder ou un capital social (montant répété ailleurs) est ignoré.
2. majuscule : mot capitalisé (composé par trait d'union ou apostrophe : « Jean-Pierre », « N'Diaye ») ;
   exempté en début de phrase (début de bloc, après . ! ? : ; hors abréviation « M. », « J. », « art. »,
   après une puce), dans un placeholder, ou s'il est au vocabulaire ou mot-outil sans être juxtaposé
   (particules sautées) à une civilité, un rôle ou un mot de voie (« Mme France », « avenue de la
   République »). En début de ligne sans ponctuation avant, seul un mot courant est exempté. Une
   civilité n'est pas signalée : le mot qui la suit l'est.
3. majuscule, ligne en capitales (60 % des lettres au moins) : mot de 3 lettres ou plus qui n'est ni au
   vocabulaire, ni mot-outil, ni verbe courant, ni mot vide de spaCy (chargé à la demande, ignoré s'il
   manque) ; un composé est courant si toutes ses parties le sont (« CI-APRÈS »).
4. chiffres : 6 chiffres ou plus (espaces admis) hors date, montant (€, euros, EUR ou % dans les
   3 caractères), référence d'article (« art. L. 1234-5 ») ou de texte (« loi n° 89-462 »).
5. arobase (@ entre deux caractères de mot), url (http://, https://, www.).
6. date_naissance : date dans les 40 caractères après « né(e)(s) » ou « date de naissance »
   (« née MARTIN le 2 juin 1965 » compris).
Une décision garder (clé entites.occurrence_key, calculée sur le texte masqué) exempte une occurrence
des motifs 2 à 6. Une étendue ne porte qu'une alerte : valeur_connue d'abord.
"""
from __future__ import annotations

import re
from functools import lru_cache
from typing import FrozenSet, Iterator, List, Optional, Set, Tuple

from . import texte
from .detection.noms import CIVILITY, PARTICLE_RX, caps_verb, function_word, known, role, stem
from .detection.regles import MONTHS, SP
from .entites import occurrence_key
from .modele import Alert, Block, Decisions, Entity
from .propagation import WORD_RX, folded, forms, pattern, span

Hit = Tuple[int, int, int, str]   # bloc, début, fin, motif
ORDER = {"valeur_connue": 0, "date_naissance": 1, "arobase": 2, "url": 2, "chiffres": 3, "majuscule": 4}
CIV_WORD_RX = re.compile(r"(?:" + CIVILITY + r")(?![\w'’])")
PLACEHOLDER_RX = re.compile(r"\[(?:[A-Z]+(?:_[A-Z]+)*_\d+|IMAGE|SIGNATURE|LOGO)\]")
STREET = frozenset(texte.norm(w) for w in
                   "rue avenue boulevard place chemin allée impasse route quai lieu-dit résidence bâtiment".split())
ABBREV = frozenset("m mm mme mmes mlle mr dr pr me st ste art arts ref cf al no av bd ch chap p pp vol ets".split())
ELISION_RX = re.compile(r"(?:[a-z]|qu|jusqu|lorsqu|puisqu|quoiqu)['’](?=[^\W\d_])")
BULLET_RX = re.compile(r"[ \t]*(?:[-•*–—▪◦]|\d{1,3}[.)]|[a-z]\))")
ARTICLE = {"le", "la", "les"}
GAP_RX = re.compile(r"[,;:!?()«»\"“”\[\]\n\t]|" + SP + r"{2}")
DATE = (r"(?:\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}|\d{4}-\d{2}-\d{2}|\d{1,2}(?i:er)?" + SP + r"+(?i:" + MONTHS + r")" + SP
        + r"+\d{4})")
DATE_RX = re.compile(r"(?<!\d)(?<!\d[./-])" + DATE + r"(?![./-]?\d)")   # pas dans « 06.12.34.56.78 »
BIRTH_RX = re.compile(r"(?i:\bn[ée]e?s?\b|\bdate" + SP + r"+de" + SP + r"+naissance\b)")
# Séparateurs admis : espace, point, barre, tiret (« 06.12.34.56.78 », « RG 23/01234 »), dates et références ôtées avant.
DIGITS_RX = re.compile(r"(?<!\d)\d(?:(?:" + SP + r"|[./-])?\d){5,}(?:,\d{1,2})?(?!\d)")
AMOUNT_RX = re.compile(r"[^\n\d]{0,3}?(?:€|(?i:euros?|eur)(?![^\W\d_])|%)")
REFERENCE_RX = re.compile(r"(?i:\barts?\.?|\barticles?)" + SP + r"?(?:[LRD]\.?" + SP + r"?)?\d[\d.-]*"
                          r"|(?i:\b(?:loi|décret|ordonnance|arrêté|directive|règlement|décision)" + SP + r"+n°)"
                          + SP + r"?\d{2,4}-\d+")
MAIL_RX = re.compile(r"[\w.+-]*\w@\w[\w.-]*")
URL_RX = re.compile(r"(?i:https?://|www\.)[^\s<>\"«»]*")
_REACH = 40


@lru_cache(maxsize=1)
def _stop_words() -> FrozenSet[str]:
    """Mots vides français de spaCy (forme texte.norm), ou rien si spaCy est absent."""
    try:
        from spacy.lang.fr.stop_words import STOP_WORDS
    except ImportError:
        return frozenset()
    return frozenset(texte.norm(w) for w in STOP_WORDS)


def _words(text: str) -> List[Tuple[int, int, str]]:
    """Mots (début, fin, mot), élision minuscule retirée (« d'Élodie » donne « Élodie »)."""
    out = []
    for m in WORD_RX.finditer(text):
        el = ELISION_RX.match(m.group())
        s = m.start() + (el.end() if el else 0)
        out.append((s, m.end(), text[s:m.end()]))
    return out


def _common(word: str, vocab: Set[str]) -> bool:
    """Mot courant : vocabulaire, mot-outil, verbe courant ou mot vide (sur le mot ou chaque partie)."""
    def one(w: str) -> bool:
        return (known(w, vocab) or function_word(w) or caps_verb(w.upper()) or texte.norm(w) in _stop_words()
                or stem(w) in _stop_words())
    return one(word) or all(one(p) for p in re.split(r"[-'’]", word) if p)


def _start(text: str, s: int) -> int:
    """2 : début de phrase ; 1 : début de ligne sans ponctuation avant ; 0 : ailleurs."""
    i, line = s, False
    while i and text[i - 1].isspace():
        line = line or text[i - 1] == "\n"
        i -= 1
    if not i or text[i - 1] in "!?:;…":
        return 2
    if text[i - 1] == ".":
        prev = re.search(r"([^\W_]*)\.$", text[max(0, i - 12):i]).group(1)
        if not prev or prev.isdigit() or (len(prev) > 1 and texte.norm(prev) not in ABBREV):
            return 2
    if BULLET_RX.fullmatch(text, text.rfind("\n", 0, i) + 1, i):
        return 2
    return 1 if line else 0


def _marked(text: str, words: List[Tuple[int, int, str]], i: int, roles: bool = True) -> bool:
    """Vrai si le mot i touche (particules sautées, sans ponctuation entre) une civilité, ou si roles, un rôle
    ou une voie."""
    for step in (-1, 1):
        j, skipped = i + step, []
        while 0 <= j < len(words) and PARTICLE_RX.fullmatch(words[j][2]):
            skipped.append(words[j][2])
            j += step
        if not 0 <= j < len(words):
            continue
        a, b = sorted((i, j))
        if GAP_RX.search(text, words[a][1], words[b][0]):
            continue   # ponctuation, placeholder ou colonnes (« Le Bailleur    Le Locataire ») entre les deux
        s, _, w = words[j]
        if CIV_WORD_RX.match(text, s) and not any(k in ARTICLE for k in skipped):   # « M. le Maire » est un titre
            return True
        if roles and (role(w, set()) or texte.norm(w) in STREET):
            return True
    return False


def _outside(s: int, e: int, spans: List[Tuple[int, int]]) -> bool:
    return all(e <= a or b <= s for a, b in spans)


def _capitals(bi: int, text: str, vocab: Set[str], holders: List[Tuple[int, int]]) -> Iterator[Hit]:
    """Motifs 2 et 3 : mots capitalisés hors placeholders, ligne par ligne."""
    words = [w for w in _words(text) if _outside(w[0], w[1], holders)]
    caps_lines = set()
    for lm in re.finditer(r"[^\n]+", text):
        letters = [c for c in PLACEHOLDER_RX.sub("", lm.group()) if c.isalpha()]
        if len(letters) >= 3 and sum(c.isupper() for c in letters) >= 0.6 * len(letters):
            caps_lines.add(lm.start())
    for i, (s, e, w) in enumerate(words):
        letters = sum(c.isalpha() for c in w)
        if text.rfind("\n", 0, s) + 1 in caps_lines:
            if letters >= 3 and w[0].isupper() and not _common(w, vocab):
                yield bi, s, e, "majuscule"
            continue
        if letters < 2 or not w[0].isupper() or CIV_WORD_RX.match(text, s):
            continue
        where = _start(text, s)
        if where == 2 and not (w.isupper() and letters >= 3):
            continue   # en tête de phrase, un mot en capitales (« DUPONT a signé ») reste relu comme en début de ligne
        if function_word(w):
            if _marked(text, words, i, roles=False):
                yield bi, s, e, "majuscule"   # « M. Le » ; ailleurs « Le », « Des » ne sont pas des noms seuls
            continue
        usual = _common(w, vocab) if where else known(w, vocab)
        if not usual or _marked(text, words, i):
            yield bi, s, e, "majuscule"


def _patterns(bi: int, text: str) -> Iterator[Hit]:
    """Motifs 4 à 6 : chiffres, arobase, url, date de naissance."""
    work = list(text)
    for rx in (DATE_RX, REFERENCE_RX, PLACEHOLDER_RX):
        for m in rx.finditer(text):
            work[m.start():m.end()] = "x" * (m.end() - m.start())
    for m in DIGITS_RX.finditer("".join(work)):
        if not AMOUNT_RX.match(text, m.end()):
            yield bi, m.start(), m.end(), "chiffres"
    for rx, reason in ((MAIL_RX, "arobase"), (URL_RX, "url")):
        for m in rx.finditer(text):
            yield bi, m.start(), m.start() + len(m.group().rstrip(".,;:)]-")), reason
    for m in BIRTH_RX.finditer(text):
        d = DATE_RX.search(text, m.end(), m.end() + _REACH + 24)
        if d and d.start() - m.end() <= _REACH:
            yield bi, d.start(), d.end(), "date_naissance"


def _values(entities: List[Entity], original: Optional[List[Block]], vocab: Set[str]) -> List[str]:
    """Valeurs connues, la plus longue d'abord."""
    out: Set[str] = set()
    for e in entities:
        if e.kind == "CAPITAL":
            continue   # ponytail: un capital répété (« 10 000 euros » de loyer) n'identifie pas la société
        texts = [e.canonical] + ([original[m.block].text[m.start:m.end] for m in e.mentions] if original else [])
        for t in texts:
            out |= {texte.norm(t)} | forms(e.kind, t, vocab)
    return sorted((v for v in out if len(v) >= 3 and not PLACEHOLDER_RX.fullmatch(v.upper())
                   and (" " in v or not _common(v, vocab))), key=lambda v: (-len(v), v))   # pas « poste » de La Poste


def _find(text: str, folds: Tuple[str, List[int]], values: List[str]) -> Iterator[Tuple[int, int]]:
    """Étendues d'origine des valeurs normalisées, bornes de mot comprises (propagation.pattern)."""
    f, pos = folds
    for v in values:
        for hit in pattern(v).finditer(f) if v in f else ():
            yield span(text, pos, hit.start(), hit.end())


def check(masked: List[Block], entities: List[Entity], decisions: Decisions, vocab: Set[str],
          original: Optional[List[Block]] = None) -> List[Alert]:
    """Alertes de la seconde passe ; original (blocs avant masquage) ajoute le texte de chaque mention."""
    values = _values(entities, original, vocab)
    communes = sorted((c for c, choice in decisions.communes.items() if choice == "garder" and c), key=len, reverse=True)
    hits: List[Hit] = []
    for bi, block in enumerate(masked):
        text = block.text
        folds = folded(text)
        holders = [m.span() for m in PLACEHOLDER_RX.finditer(text)]
        exempt = holders + list(_find(text, folds, communes))   # commune gardée : ni majuscule ni chiffres
        hits += [(bi, s, e, "valeur_connue") for s, e in _find(text, folds, values) if _outside(s, e, holders)]
        hits += [h for h in list(_capitals(bi, text, vocab, holders)) + list(_patterns(bi, text))
                 if _outside(h[1], h[2], exempt) and occurrence_key(block, h[1], h[2]) not in decisions.keep]
    kept: List[Hit] = []
    for h in sorted(hits, key=lambda h: (ORDER[h[3]], h[0], h[1], h[1] - h[2])):
        if all(k[0] != h[0] or h[2] <= k[1] or k[2] <= h[1] for k in kept):
            kept.append(h)
    kept.sort(key=lambda h: (h[0], h[1]))
    return [Alert("A%d" % n, bi, s, e, masked[bi].text[s:e], reason) for n, (bi, s, e, reason) in enumerate(kept, 1)]
