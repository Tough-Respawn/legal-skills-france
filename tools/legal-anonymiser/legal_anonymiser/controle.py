"""Seconde passe : relecture du texte masqué, dernier filet avant la validation humaine.

Alertes A1, A2… dans l'ordre du document, positions sur le texte masqué (détail : README) :
1. valeur_connue : valeur d'une entité (forme canonique, ses formes, texte des mentions si les blocs
   d'origine sont donnés), sans casse ni accents, minuscules comprises ; jamais exemptée par garder.
   Un mot seul courant (« Juin ») n'alerte que collé à une civilité, un rôle, une voie ou un mot signalé.
2. majuscule : mot capitalisé hors début de phrase, placeholder, ou mot courant non collé à une
   civilité, un rôle ou une voie ; 3. en ligne capitale, mot hors vocabulaire, mot-outil, verbe courant
   et mots vides de spaCy, ou collé à une civilité. Mots signalés consécutifs : une alerte.
4. chiffres (6 ou plus, hors date, montant, référence), 5. arobase, url, 6. date_naissance.
Une décision garder (entites.Ranks.key sur le texte masqué) exempte une occurrence des motifs 2 à 6 ;
une commune gardée aussi, sauf après une civilité. Une étendue, une alerte : valeur_connue d'abord.
"""
from __future__ import annotations

import re
from bisect import bisect_right
from functools import lru_cache
from typing import Callable, FrozenSet, Iterable, Iterator, List, Optional, Set, Tuple

from . import texte
from .detection.noms import CIVILITY, PARTICLE_RX, caps_verb, function_word, known, role, stem
from .detection.regles import MONTHS, SP
from .entites import Ranks
from .modele import Alert, Block, Decisions, Entity
from .propagation import WORD_RX, forms, pattern, span

Hit = Tuple[int, int, str]    # début, fin, motif (dans un bloc)
Word = Tuple[int, int, str]   # début, fin, mot
ORDER = {"valeur_connue": 0, "date_naissance": 1, "arobase": 2, "url": 2, "chiffres": 3, "majuscule": 4}
CIV_WORD_RX = re.compile(r"(?:" + CIVILITY + r")(?![\w'’])")
PLACEHOLDER_RX = re.compile(r"\[(?:[A-Z]+(?:_[A-Z]+)*_\d+|IMAGE|SIGNATURE|LOGO)\]")
STREET = frozenset(texte.norm(w) for w in
                   "rue avenue boulevard place chemin allée impasse route quai lieu-dit résidence bâtiment".split())
ABBREV = frozenset("m mm mme mmes mlle mr dr pr me st ste art arts ref cf al no av bd ch chap p pp vol ets".split())
ELISION_RX = re.compile(r"(?:[a-z]|qu|jusqu|lorsqu|puisqu|quoiqu)['’](?=[^\W\d_])")
BULLET_RX = re.compile(r"[ \t]*(?:[-•*–—▪◦]|\d{1,3}[.)]|[a-z]\))")
ARTICLE = {"le", "la", "les", "l", "l'"}
LINKS = {"et", "l", "d", "l'", "d'"}   # sautés comme les particules entre une civilité et le nom
GAP_RX = re.compile(r"[.,;:!?()«»\"“”\[\]\n\t]|" + SP + r"{2}")
JOIN_RX = re.compile(SP + r"|" + SP + r"?['’-]" + SP + r"?")
BEFORE_RX = re.compile(r"(?:" + JOIN_RX.pattern + r")$")
DATE = (r"(?:\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}|\d{4}-\d{2}-\d{2}|\d{1,2}(?i:er)?" + SP + r"+(?i:" + MONTHS + r")" + SP
        + r"+\d{4})")
DATE_RX = re.compile(r"(?<!\d)(?<!\d[./-])" + DATE + r"(?![./-]?\d)")   # pas dans « 06.12.34.56.78 »
BIRTH_RX = re.compile(r"(?i:\bn(?:ée?s?|ees?)\b|\bdate" + SP + r"+de" + SP + r"+naissance\b)|\bNE(?=" + SP
                      + r"+(?:LE|À|A)\b)")   # « NE LE » en capitales sans accent ; « ne le résiliera » non
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


def _overlaps(spans: Iterable[Tuple[int, int]]) -> Callable[[int, int], bool]:
    """Test « [s, e) chevauche une des étendues », par dichotomie sur les étendues fusionnées."""
    starts: List[int] = []
    ends: List[int] = []
    for s, e in sorted(spans):
        if ends and s < ends[-1]:
            ends[-1] = max(ends[-1], e)
        else:
            starts.append(s)
            ends.append(e)

    def hit(s: int, e: int) -> bool:
        i = bisect_right(starts, s) - 1
        return (i >= 0 and ends[i] > s) or (i + 1 < len(starts) and starts[i + 1] < e)
    return hit


class _Lines:
    """Débuts de ligne et lignes en capitales (60 % des lettres hors placeholders, 3 lettres au moins)."""

    def __init__(self, text: str) -> None:
        self.starts = [0] + [m.end() for m in re.finditer("\n", text)]
        self.caps = []
        for line in text.split("\n"):
            letters = [c for c in PLACEHOLDER_RX.sub("", line) if c.isalpha()]
            self.caps.append(len(letters) >= 3 and sum(c.isupper() for c in letters) >= 0.6 * len(letters))

    def start(self, pos: int) -> int:
        return self.starts[bisect_right(self.starts, pos) - 1]

    def capitals(self, pos: int) -> bool:
        return self.caps[bisect_right(self.starts, pos) - 1]


def _words(text: str, inside: Callable[[int, int], bool]) -> List[Word]:
    """Mots hors placeholders, élision minuscule retirée (« d'Élodie » donne « Élodie »)."""
    out = []
    for m in WORD_RX.finditer(text):
        el = ELISION_RX.match(m.group())
        s = m.start() + (el.end() if el else 0)
        if not inside(s, m.end()):
            out.append((s, m.end(), text[s:m.end()]))
    return out


def _common(word: str, vocab: Set[str]) -> bool:
    """Mot courant : vocabulaire, mot-outil, verbe courant ou mot vide (sur le mot ou chaque partie)."""
    def one(w: str) -> bool:
        return (known(w, vocab) or function_word(w) or caps_verb(w.upper()) or texte.norm(w) in _stop_words()
                or stem(w) in _stop_words())
    return one(word) or all(one(p) for p in re.split(r"[-'’]", word) if p)


def _start(text: str, s: int, lines: _Lines) -> int:
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
    if BULLET_RX.fullmatch(text, lines.start(i - 1), i):
        return 2
    return 1 if line else 0


def _marked(text: str, words: List[Word], i: int, roles: bool = True) -> bool:
    """Vrai si le mot i suit une civilité, ou si roles touche un rôle ou une voie (particules sautées, sans
    ponctuation ni colonnes entre). Après une civilité, l'écart se mesure depuis sa fin (« M. FRANCE »)."""
    for step in (-1, 1):
        j, skipped = i + step, []
        while 0 <= j < len(words) and (PARTICLE_RX.fullmatch(words[j][2]) or _link(words[j][2]) in LINKS):
            skipped.append(words[j][2])
            j += step
        if not 0 <= j < len(words):
            continue
        s, e, w = words[j]
        civ = CIV_WORD_RX.match(text, s) if j < i else None   # une civilité annonce le mot qui la suit
        lo, hi = (civ.end() if civ else e, words[i][0]) if j < i else (words[i][1], s)
        if GAP_RX.search(text, lo, hi):
            continue   # « en Avril. M. Kerbrat », « Le Bailleur    Le Locataire »
        if civ and not any(_link(k) in ARTICLE for k in skipped):   # « M. le Maire », « M. LE MAIRE » : titre
            return True
        if roles and (role(w, set()) or texte.norm(w) in STREET):
            return True
    return False


def _capitals(text: str, words: List[Word], vocab: Set[str], commune: Callable[[int, int], bool]
              ) -> List[Tuple[int, int, bool]]:
    """Motifs 2 et 3 : (début, fin, faible) par mot signalé ; faible = exempté par sa seule place en tête
    de phrase (il ne compte que joint à un mot signalé)."""
    lines = _Lines(text)
    out = []
    for i, (s, e, w) in enumerate(words):
        letters = sum(c.isalpha() for c in w)
        if letters < 2 or not w[0].isupper() or CIV_WORD_RX.match(text, s):
            continue
        civ = _marked(text, words, i, roles=False)
        if commune(s, e) and not civ:
            continue   # commune gardée, sauf « M. Valence »
        if lines.capitals(s):
            if function_word(w):
                continue   # « MONSIEUR LE MAIRE », « M. ET MME DURANT »
            if civ or (letters >= 3 and not _common(w, vocab)):
                out.append((s, e, False))
            continue
        where = _start(text, s, lines)
        if where == 2 and not (w.isupper() and letters >= 3):
            if not _common(w, vocab):
                out.append((s, e, True))
            continue
        if function_word(w):
            if civ:
                out.append((s, e, False))   # « M. Le » ; ailleurs « Le », « Des » ne sont pas des noms seuls
            continue
        if civ or not (_common(w, vocab) if where else known(w, vocab)) or _marked(text, words, i):
            out.append((s, e, False))
    return out


def _link(word: str) -> str:
    return word.lower().replace("’", "'")


def _touches(text: str, s: int, e: int, taken: Callable[[int, int], bool]) -> bool:
    """Vrai si une autre alerte suit ou précède [s, e), séparée au plus par une espace, un trait d'union
    ou une apostrophe."""
    after = JOIN_RX.match(text, e)
    before = BEFORE_RX.search(text, max(0, s - 3), s)
    return bool(after and taken(after.end(), after.end() + 1)) or bool(before and taken(before.start() - 1,
                                                                                        before.start()))


def _runs(text: str, marked: List[Tuple[int, int, bool]], taken: Callable[[int, int], bool]) -> List[Hit]:
    """Mots signalés consécutifs fusionnés en une alerte. Un mot déjà couvert par une autre alerte (valeur
    connue, url…) en est retiré avant la fusion : ses voisins gardent leur alerte (« Paul [Kerbrat] ») ;
    une suite de mots faibles n'est gardée que collée à une autre alerte."""
    runs: List[list] = []
    for s, e, weak in marked:
        if taken(s, e):
            continue
        if runs and JOIN_RX.fullmatch(text, runs[-1][1], s):
            runs[-1][1:] = [e, runs[-1][2] and weak]
        else:
            runs.append([s, e, weak])
    return [(s, e, "majuscule") for s, e, weak in runs if not weak or _touches(text, s, e, taken)]


def _beside(text: str, words: List[Word], i: int, flagged: Set[int]) -> bool:
    """Vrai si un mot voisin du mot i, séparé par une espace, un trait d'union ou une apostrophe, est signalé."""
    return any(0 <= j < len(words) and words[j][0] in flagged
               and JOIN_RX.fullmatch(text, *((words[j][1], words[i][0]) if j < i else (words[i][1], words[j][0])))
               for j in (i - 1, i + 1))


def _patterns(text: str) -> Iterator[Hit]:
    """Motifs 4 à 6 : chiffres, arobase, url, date de naissance."""
    work = list(text)
    for rx in (DATE_RX, REFERENCE_RX, PLACEHOLDER_RX):
        for m in rx.finditer(text):
            work[m.start():m.end()] = "x" * (m.end() - m.start())
    for m in DIGITS_RX.finditer("".join(work)):
        if not AMOUNT_RX.match(text, m.end()):
            yield m.start(), m.end(), "chiffres"
    for rx, reason in ((MAIL_RX, "arobase"), (URL_RX, "url")):
        for m in rx.finditer(text):
            yield m.start(), m.start() + len(m.group().rstrip(".,;:)]-")), reason
    for m in BIRTH_RX.finditer(text):
        d = DATE_RX.search(text, m.end(), m.end() + _REACH + 24)
        if d and d.start() - m.end() <= _REACH:
            yield d.start(), d.end(), "date_naissance"


def _values(entities: List[Entity], original: Optional[List[Block]], vocab: Set[str]) -> Tuple[List[str], List[str]]:
    """Valeurs connues (la plus longue d'abord), et valeurs d'un seul mot courant à part."""
    out: Set[str] = set()
    for e in entities:
        if e.kind == "CAPITAL":
            continue   # ponytail: un capital répété (« 10 000 euros » de loyer) n'identifie pas la société
        texts = [e.canonical] + ([original[m.block].text[m.start:m.end] for m in e.mentions] if original else [])
        for t in texts:
            out |= {texte.norm(t)} | forms(e.kind, t, vocab)
    values = sorted((v for v in out if len(v) >= 3 and not PLACEHOLDER_RX.fullmatch(v.upper())),
                    key=lambda v: (-len(v), v))
    common = {v for v in values if " " not in v and _common(v, vocab)}   # « juin », « poste » de La Poste
    return [v for v in values if v not in common], [v for v in values if v in common]


def _find(text: str, folds: Tuple[str, List[int]], values: List[str]) -> Iterator[Tuple[int, int]]:
    """Étendues d'origine des valeurs normalisées, bornes de mot comprises (propagation.pattern)."""
    f, pos = folds
    for v in values:
        for hit in pattern(v).finditer(f) if v in f else ():
            yield span(text, pos, hit.start(), hit.end())


def _dedupe(hits: List[Hit]) -> List[Hit]:
    """Une alerte par étendue, la plus prioritaire d'abord (valeur_connue), dans l'ordre du bloc."""
    starts: List[int] = []
    ends: List[int] = []
    out = []
    for s, e, reason in sorted(hits, key=lambda h: (ORDER[h[2]], h[0], h[0] - h[1])):
        i = bisect_right(starts, s)
        if (i and ends[i - 1] > s) or (i < len(starts) and starts[i] < e):
            continue
        starts.insert(i, s)
        ends.insert(i, e)
        out.append((s, e, reason))
    return sorted(out)


def check(masked: List[Block], entities: List[Entity], decisions: Decisions, vocab: Set[str],
          original: Optional[List[Block]] = None) -> List[Alert]:
    """Alertes de la seconde passe ; original (blocs avant masquage) ajoute le texte de chaque mention."""
    values, common = _values(entities, original, vocab)
    communes = sorted((c for c, choice in decisions.communes.items() if choice == "garder" and c), key=len, reverse=True)
    kept = {(k[0], k[1]) for k in decisions.keep}   # clé calculée seulement pour une forme gardée
    ranks = Ranks(masked)
    out: List[Tuple[int, int, int, str]] = []
    for bi, block in enumerate(masked):
        text, folds = block.text, ranks.fold(bi)
        holder = _overlaps(m.span() for m in PLACEHOLDER_RX.finditer(text))
        words = _words(text, holder)
        at = {w[0]: i for i, w in enumerate(words)}
        marked = _capitals(text, words, vocab, _overlaps(_find(text, folds, communes)))
        flagged = {m[0] for m in marked}
        hits = [(s, e, "valeur_connue") for s, e in _find(text, folds, values) if not holder(s, e)]
        hits += [(s, e, "valeur_connue") for s, e in _find(text, folds, common)   # « M. JUIN », « Lucas Juin »
                 if s in at and (_marked(text, words, at[s]) or _beside(text, words, at[s], flagged))]
        hits += [h for h in _patterns(text) if not holder(h[0], h[1])]
        hits += _runs(text, marked, _overlaps((h[0], h[1]) for h in hits))
        hits = [h for h in hits if h[2] == "valeur_connue" or not (
            (block.location, texte.norm(text[h[0]:h[1]])) in kept and ranks.key(bi, h[0], h[1]) in decisions.keep)]
        out += [(bi,) + h for h in _dedupe(hits)]
    return [Alert("A%d" % n, bi, s, e, masked[bi].text[s:e], reason) for n, (bi, s, e, reason) in enumerate(out, 1)]
