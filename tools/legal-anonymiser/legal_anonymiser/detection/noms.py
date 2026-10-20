"""Candidats de noms : personnes (civilité, nom sans civilité, nom d'usage) et sociétés.

Une société est repérée par sa forme sociale (SAS, SCI…) ou un mot d'annonce (« La
société », « Association »). Quand une forme a un nom plausible de chaque côté
(« LA SOCIÉTÉ SAS DUVALCOURT CONSEIL », « DUVALCOURT CONSEIL SAS IMMATRICULÉE »), les
deux côtés sont des candidats indépendants, jugés chacun sur ses propres mots : un
candidat est rejeté s'il n'est fait que de mots du vocabulaire ou de mots vides, et un
nom placé avant sa forme ne commence jamais par un article ou une préposition suivis
d'un mot capitalisé. Un côté ne supprime jamais l'autre. La forme sociale reste hors
du nom, elle demeure visible (spec 6.4). « SA » devant un mot en capitales est le possessif
(« EXERCER SA MISSION ») sauf marqueur de société qui suit ou annonce qui précède.
"""
from __future__ import annotations

import re
from itertools import dropwhile
from typing import List, Optional, Set, Tuple

from .. import texte
from .regles import SP

ROLE_WORDS = frozenset({
    "BAILLEUR", "LOCATAIRE", "EMPLOYEUR", "SALARIE", "PRESTATAIRE", "CLIENT", "VENDEUR",
    "ACHETEUR", "CAUTION", "MANDANT", "MANDATAIRE", "PRETEUR", "EMPRUNTEUR", "REPRESENTANT",
    "ACQUEREUR", "CEDANT", "CESSIONNAIRE", "GARANT", "COLOCATAIRE", "PRENEUR",
})
# Féminins et pluriels ramenés au masculin singulier (sur la forme texte.norm).
_SUFFIXES = (("eresse", "eur"), ("euse", "eur"), ("trice", "teur"), ("es", ""), ("e", ""), ("s", ""))
_COLLECTIVE = {"PARTIE", "PARTIES"}  # « ci-après ensemble les Parties » : pas un rôle
STOPWORDS = {"de", "du", "des", "la", "le", "les", "l", "d", "a", "et", "en", "au", "aux", "un", "une", "&"}
# Mots-outils sans ambiguïté, jamais un nom : liste fixe, car les mots vides de spaCy contiennent de vrais
# noms (HUI, MIN, SON, VU, TA, LI…). Comparés en minuscules, apostrophe droite.
FUNCTION_WORDS = frozenset({
    "est", "et", "ou", "de", "du", "des", "le", "la", "les", "l'", "un", "une", "en", "par", "pour", "sur", "sous",
    "avec", "sans", "dans", "qui", "que", "dont", "au", "aux", "ce", "ces", "cette", "ne", "se", "lui", "leur",
    "leurs", "nos", "vos", "votre", "notre", "à",
})
NAME_JOINERS = frozenset({"de", "du", "des", "le", "la", "les", "l'", "d'", "sur", "sous", "en", "lès", "et", "&"})
# Verbes et auxiliaires courants des contrats : en capitales, un nom s'arrête avant eux (« AWA SIGNE LE CONTRAT »).
CAPS_VERBS = frozenset({
    "SIGNE", "SIGNENT", "ACCEPTE", "ACCEPTENT", "DÉCLARE", "DÉCLARENT", "RECONNAÎT", "RECONNAISSENT", "S'ENGAGE",
    "S'ENGAGENT", "EST", "SONT", "SERA", "SERONT", "A", "ONT", "AURA", "AURONT", "DOIT", "DOIVENT", "PEUT",
    "PEUVENT", "CERTIFIE", "ATTESTE", "REMET", "REMETTRA", "VERSE", "VERSERA", "PAIE", "PAIERA", "OCCUPE",
    "OCCUPERA", "LOUE", "PREND", "PRENDRA", "DONNE", "DONNERA", "RENCONTRE", "ACQUITTE", "RESTITUE", "RECEVRA",
    "REÇOIT", "EXERCE", "EXERCERA", "TRAVAILLE", "TRAVAILLERA", "DEMEURE", "RÉSIDE", "AGIT", "AGISSANT",
})

UP = "A-ZÀ-ÖØ-ÞŒ"
LOW = "a-zß-öø-ÿœ"
ALLCAPS = r"[" + UP + r"](?:[" + UP + r"]|['’-][" + UP + r"])+"
FIRST = r"[" + UP + r"][" + LOW + r"]+(?:['’-][" + UP + r"]?[" + LOW + r"]+)*"
CIVILITY = (r"(?:(?:M|MM|MME|MR|MLLE)\.|(?:Mr|Mme|Mmes|Mlle|Dr|Pr|MME|MR|MLLE|PR)\.?|Monsieur|Madame|"
            r"Mademoiselle|MONSIEUR|MADAME|MADEMOISELLE|Me|Maître|MAÎTRE|Docteur|Professeur"
            r"|M(?=" + SP + r"+" + ALLCAPS + SP + r"+" + ALLCAPS + r"))")   # M sans point : « M JEAN DUPONT »
FORMS = r"(?:SAS|SASU|SARL|EURL|SA|SCI|SNC|SCP|SELARL|SELAS|SCM|GIE|SCEA|EARL|SCOP)"
# Prépositions en capitales : hors d'un nom seulement devant un mot en capitales (« AVANT LE », pas « M. AVANT né »).
PREP_CORE = r"(?:À|AU|AUX|EN|PAR|POUR|SUR|DANS|AVEC|CHEZ|DEVANT|CONTRE|ENTRE|ENVERS|SELON|VERS|DONT|QUI|QUE)"
PREP = r"(?:" + PREP_CORE + r"|SOUS|SANS|APRÈS|AVANT)" + SP + r"+[" + UP + "]"
# Mots de contexte qui suivent un nom et n'en font jamais partie.
CONTEXT = (r"(?i:née?s?|épouse|veuve|divorcée?|dite?|demeurant|domiciliée?s?|représentée?s?|immatriculée?s?"
           r"|inscrite?s?|enregistrée?s?|prises?|ayant|agissant|sises?|située?s?|dénommée?s?|désignée?s?"
           r"|ci-après|ci-dessous|d['’](?:une|autre))\b")
# Mot capitalisé (Jean-Pierre, N'Diaye, DUPONT, LE) : ni « Et », ni civilité, ni « LE » d'une date (LE 3 MARS).
CAP_ANY = (r"(?!(?:Et|ET|Ou|OU)\b)(?!" + CONTEXT + r")(?!" + CIVILITY + "(?:" + SP + r"|$))"
           r"(?!(?i:le|la|les|de|du|des)" + SP + r"+\d)[" + UP + r"][^\W\d_]*(?:['’-][^\W\d_]+)*")
CAP = r"(?!" + PREP + r")" + CAP_ANY
PARTICLES = r"(?:de|du|des|da|dos|di|del|el|al|ben|bin|van|von|der|den|ter|le|la)"
JOIN_P = SP + r"(?:" + PARTICLES + SP + r"){0,2}(?:[dl]['’])?"
# Particule en tête de nom (M. de Villiers, Mme d'Arcy) ; jamais « le », « la », « l' » seuls (M. le Maire).
LEAD_P = (r"(?:(?:de|du|des|da|dos|di|del|el|al|ben|bin|van|von|der|den|ter)" + SP + r"+(?:" + PARTICLES + SP
          + r"+)?(?:[dl]['’])?|d['’])")
# Liaison dans un nom de société : « Les Hauts de Valmorin », « Dupont et Fils », « Martin & Associés » ;
# « et » ne joint pas un article (« DUPONT ET FILS ET LA SCI »).
JOIN_C = (SP + r"(?:(?:de|du|des|la|le|les|au|aux|en|sur)" + SP + r"|(?:et|Et|ET|&)" + SP
          + r"(?!(?i:(?:le|la|les|un|une)(?:" + SP + r"|$))|[dl]['’]))?(?:[dl]['’])?")
PERSON = CAP + r"(?:" + JOIN_P + CAP + r"){0,3}"
CO_CAP = r"(?!" + FORMS + r"\b)" + CAP  # la forme sociale reste hors du nom
COMPANY = CO_CAP + r"(?:" + JOIN_C + CO_CAP + r"){0,5}"
# Nom placé avant sa forme (« SANS SOUCI SAS », « DUPONT ET FILS SARL ») : jamais ouvert par un article ou une
# préposition devant un mot capitalisé (« LA SOCIÉTÉ SAS X », « Pour SCI X », « CONSENTI PAR X SAS ») ; les
# articles restent admis au milieu (« LES HAUTS DE VALMORIN SCI ») ; « SANS », « SOUS » peuvent l'ouvrir.
FUNC_START = (r"(?i:le|la|les|un|une|de|du|des|a|à|au|aux|en|par|pour|sur|dans|avec|chez|devant|contre|entre"
              r"|envers|selon|vers|dont|qui|que|et|ou)" + SP + r"+[" + UP + "]")   # « L'Oréal SA » reste admis
# Mots d'ouverture retirés en tête d'un nom placé avant sa forme (« CONTRAT X SAS », « Gérant SARL X ») ;
# un reste fait seulement de mots d'annonce (« LA SOCIÉTÉ SAS X ») n'est pas un nom.
LEAD_STRIP = {"entre", "contrat", "convention", "pour", "gerant", "president", "directeur", "la", "le", "les", "l",
              "de", "du", "des", "a", "par", "contre"}
GENERIC = {"societe", "association", "entreprise", "groupe", "cabinet", "ets", "etablissements"}
# « SA » devant un mot en capitales : forme sociale seulement si un marqueur de société suit dans les 80
# caractères, si « la », « entre », « société » précède, ou si une préposition suit (« X SA ENTRE ») ;
# sinon possessif, quel que soit le mot qui suit (« EXERCER SA MISSION », « MET SA VOITURE »). Une virgule
# seule n'est pas un marqueur.
SA_MARK_RX = re.compile(r"(?<!\w)(?i:au" + SP + r"+capital|immatricul|rcs|siren|siret|dont" + SP + r"+le" + SP
                        + r"+si[èe]ge|repr[ée]sent[ée]e?" + SP + r"+par|ci-apr[èe]s|soci[ée]t[ée]" + SP
                        + r"+anonyme)")
SA_LEAD_RX = re.compile(r"(?<!\w)(?i:(?:la" + SP + r"+)?soci[ée]t[ée]|la|entre)" + SP + r"+$")
CO_CAP_ANY = r"(?!" + FORMS + r"\b)" + CAP_ANY
CO_START = r"(?!" + FUNC_START + r")" + CO_CAP_ANY
CO_IN = r"(?!" + PREP_CORE + SP + r"+[" + UP + r"])" + CO_CAP_ANY
COMPANY_BEFORE_FORM = CO_START + r"(?:" + JOIN_C + CO_IN + r"){0,5}"

CIVIL_RX = re.compile(r"(?<![\w.])(?:" + CIVILITY + SP + r"+(?:et|ET)" + SP + r"+)?(?P<civ>" + CIVILITY + ")"
                      + SP + r"+(?P<lead>" + LEAD_P + r")?(?P<name>" + PERSON + ")")
ALIAS_RX = re.compile(r"(?<![\w-])(?i:née|nee|épouse|epouse|veuve|divorcée|divorcee|dite?)" + SP
                      + r"+(?P<name>" + PERSON + ")")
NUMBER_BEFORE_RX = re.compile(r"(?:\d|\b(?i:un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|vingt|cent))"
                              + SP + r"*$")   # « 2 M DE HAUTEUR » : M est une unité
CO_PRE_RX = re.compile(
    r"(?<!\w)(?:(?:[Ll]a|LA)" + SP + r"+(?:société|Société|SOCIÉTÉ)|[Ll]['’](?:association|Association|ASSOCIATION)"
    r"|Société|SOCIÉTÉ|Sté|Ets\.?|Établissements|Etablissements|Association|(?P<form>" + FORMS + r")\b)"
    + SP + r"+(?P<co>" + COMPANY + ")")
CO_POST_RX = re.compile(r"(?<![\w'’-])(?P<co>" + COMPANY_BEFORE_FORM + ")" + SP + r"+(?P<form>" + FORMS + r")\b")
JOINER_RX = re.compile(SP + r"*(?:(?:et|Et|ET|&)" + SP + r"+)?")
# Nom sans civilité : DUPONT Jean, Jean DUPONT ; seulement en contexte (comparution, signature, né le).
BARE_RX = re.compile(
    r"(?<![\w'’-])(?:" + ALLCAPS + r"(?:" + SP + ALLCAPS + r")?(?:" + SP + FIRST + r"){1,2}"
    r"|" + FIRST + r"(?:" + SP + FIRST + r")?(?:" + SP + ALLCAPS + r"){1,2})(?![\w'’-])")
BORN_RX = re.compile(r"\s*,?\s*n[ée]e?" + SP + r"+le\b")
LINE_NAME_RX = re.compile(SP + r"*(" + CAP + r"(?:" + JOIN_P + CAP + r"){1,3})" + SP + r"*(?:[,(–-].*)?$")
CELL_RX = re.compile(r"[^\t   ]+(?:[   ][^\t   ]+)*")  # colonnes : tabulation ou 2 espaces
CAPTION_LEAD_RX = re.compile(r"\s*(?i:(?:pour\s+)?(?:le|la|les|l['’])\s*([^\W\d_]+))\s*[,:]?\s*")
SIG_CAPTION_RX = re.compile(r"\s*(?i:signatures?(?:\s+des\s+parties)?|pour\s+[^.]{1,60})\s*:?\s*")
WORD_RX = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*|&")
CIV_RX = re.compile(r"(?:" + CIVILITY + SP + r"+(?:et|ET)" + SP + r"+)?" + CIVILITY + SP + r"+")
PARTICLE_RX = re.compile(r"(?i:" + PARTICLES + r")")
_LINKS = NAME_JOINERS | {"au", "aux"}   # liaisons d'un nom de société (JOIN_C)


def lower_word(word: str) -> bool:
    """Mot en minuscules, élision « l' », « d' » retirée, qui n'est ni une particule ni une liaison de nom :
    « sans », « l'accord », « né » oui ; « de », « et », « sur », « d'Arcy » non."""
    w = word.replace("’", "'")
    return (re.sub(r"^[dl]'", "", w, flags=re.I)[:1].islower() and not PARTICLE_RX.fullmatch(w)
            and w.lower() not in _LINKS)

Cand = Tuple[int, int, int, int, str]  # début, fin, étendue (début, fin) du motif, type (ALIAS = nom d'usage)
Span = Tuple[int, int]


def function_word(word: str) -> bool:
    return word.lower().replace("’", "'") in FUNCTION_WORDS


def caps_verb(word: str) -> bool:
    return word.replace("’", "'") in CAPS_VERBS


def _verb_at(text: str, w: "re.Match[str]") -> bool:
    """Verbe courant, sauf « A. » (initiale)."""
    return caps_verb(w.group()) and not (len(w.group()) == 1 and text.startswith(".", w.end()))


def verb_cut(text: str, s: int, e: int, lead: bool = True) -> Span:
    """Étendue tout en capitales bornée par ses verbes courants. La fin s'arrête au premier verbe qui suit
    au moins un mot de nom, deux si une civilité ouvre l'étendue (« AWA SIGNE LE CONTRAT » donne « AWA »,
    « MADAME SIGNE HANSEN SONT PRÉSENTS » donne « MADAME SIGNE HANSEN », « MADAME CLAIRE DEMEURE EST
    TÉMOIN » garde « MADAME CLAIRE DEMEURE ») ; un verbe en tête n'est retiré (lead) que s'il reste deux
    mots au moins (« SIGNE HANSEN » reste entier). Une étendue qui n'est pas en capitales est rendue telle quelle."""
    if not text[s:e].isupper():
        return s, e
    civ = CIV_RX.match(text, s, e)
    words = list(WORD_RX.finditer(text, civ.end() if civ else s, e))
    if lead and not civ and len(words) > 2 and _verb_at(text, words[0]):
        words, s = words[1:], words[1].start()
    for w in words[2 if civ else 1:]:
        if _verb_at(text, w):
            return s, max(s, len(text[:w.start()].rstrip(" ,\u00a0\u202f\n")))
    return s, e


def stem(word: str) -> str:
    """Forme normalisée sans l'élision (d'Effet → effet)."""
    return re.sub(r"^[dl]'", "", texte.norm(word))


def _forms(word: str) -> List[str]:
    """Forme normalisée et ses variantes au masculin singulier (vendeuse, garants…)."""
    n = stem(word)
    return [n] + [n[:-len(a)] + b for a, b in _SUFFIXES if n.endswith(a) and len(n) > len(a) + 2]


def known(word: str, vocab: Set[str]) -> bool:
    return any(f in vocab or f.upper() in ROLE_WORDS for f in _forms(word))


def tokens(s: str) -> List[str]:
    """Mots porteurs de sens : élisions retirées (d'Effet), mots vides écartés."""
    return [w for w in (stem(w) for w in WORD_RX.findall(s)) if w and w not in STOPWORDS]


def role(term: str, vocab: Set[str]) -> Optional[str]:
    """Rôle canonique d'un terme défini ; "" s'il est à ignorer ; None s'il ressemble à un nom propre."""
    words = tokens(term)
    if len(words) == 1:
        for f in _forms(words[0]):
            if f.upper() in ROLE_WORDS:
                return f.upper()
    if not words or not all(known(w, vocab) for w in words):
        return None
    key = re.sub(r"[^A-Z0-9]+", "_", texte.norm(term).upper()).strip("_")
    return "" if key in _COLLECTIVE else key


def company(text: str, s: int, e: int, vocab: Set[str], loose: bool, before: bool = False) -> Optional[Span]:
    """Nom de société dans (s, e), ou None. Après une forme sociale (loose), le nom reste entier
    (« SARL Expert Conseil »). Avant sa forme (before), il doit la toucher, perd ses mots d'ouverture
    (« CONTRAT DUVALCOURT CONSEIL SAS ») et n'est pas fait que de mots d'annonce (« LA SOCIÉTÉ SAS X ») ;
    les mots courants y restent admis (« Société Générale SA »). Après un mot d'annonce (« Société X »),
    les mots connus en tête sont retirés et un nom tout connu est rejeté (« la dite Société »)."""
    words = list(WORD_RX.finditer(text, s, e))
    real = [w for w in words if stem(w.group()) not in STOPWORDS]
    if before:
        if not real or real[-1].end() != e:
            return None   # « DUPONT ET FILS ET LA » : un article sépare le nom de la forme
        kept = list(dropwhile(lambda w: stem(w.group()) in LEAD_STRIP, real))
        if not kept or all(stem(w.group()) in GENERIC for w in kept):
            return None
        return kept[0].start(), e
    if not real or (not loose and all(known(w.group(), vocab) for w in real)):
        return None
    start = words[0].start() if loose else next(w.start() for w in words if not known(w.group(), vocab))
    return start, real[-1].end()


def _possessive(text: str, m: "re.Match[str]") -> bool:
    """Vrai si la forme du candidat est un « SA » possessif (« EXERCER SA MISSION »), pas une société."""
    fs, fe = m.span("form")
    nxt = WORD_RX.search(text, fe)
    if m.group("form") != "SA" or not nxt or not nxt.group().isupper() or re.fullmatch(PREP_CORE, nxt.group()):
        return False   # « DUVALCOURT CONSEIL SA ENTRE LES SOUSSIGNÉS » : un possessif ne précède pas une préposition
    return not SA_MARK_RX.search(text, fe, fe + 80) and not SA_LEAD_RX.search(text, 0, fs)


def _clear(text: str, s: int, e: int, people: List[Span]) -> Span:
    """Rogne un candidat société sur les personnes déjà reconnues : dans « MONSIEUR PAUL DURAND ET
    DUVALCOURT CONSEIL SAS », la personne garde son étendue, la société commence après « ET »."""
    for ps, pe in people:
        if ps < e and s < pe:
            if s < ps:
                e = ps
            else:
                s = JOINER_RX.match(text, pe).end()
    return s, e


def cells(text: str, vocab: Set[str]) -> List[Tuple[bool, Optional[Span]]]:
    """Colonnes d'une ligne de signature : (légende ?, nom seul de la colonne)."""
    out = []
    for c in CELL_RX.finditer(text):
        s, cell = c.start(), c.group()
        lead = CAPTION_LEAD_RX.match(cell)
        role_lead = bool(lead) and bool(role(lead.group(1), set()))
        if role_lead:
            s += lead.end()
        m = LINE_NAME_RX.match(text, s, c.end())
        name = m.span(1) if m and not any(known(w, vocab) for w in tokens(m.group(1))) else None
        caption = bool(SIG_CAPTION_RX.fullmatch(cell)) or (role_lead and (s == c.end() or name is not None))
        out.append((caption, name))
    return out


def names(text: str, vocab: Set[str], bare: bool, skip: List[Span]) -> List[Cand]:
    """Noms de personnes et de sociétés, sans chevauchement (le motif le plus à gauche puis le plus long)."""
    cands: List[Cand] = []
    for m in CIVIL_RX.finditer(text):
        if m.group("lead") and all(known(w, vocab) for w in tokens(m.group("name"))):
            continue  # « Maître d'Œuvre »
        if m.group("civ") == "M" and NUMBER_BEFORE_RX.search(text, max(0, m.start() - 12), m.start()):
            continue  # « 2 M DE HAUTEUR »
        cands.append((m.start(), m.end(), m.start(), m.end(), "PERSONNE"))
    for m in ALIAS_RX.finditer(text):
        if not all(known(w, vocab) for w in tokens(m.group("name"))):   # pas « la dite Société »
            cands.append((m.start("name"), m.end(), m.start(), m.end(), "ALIAS"))
    people = [(c[0], c[1]) for c in cands]
    for m in CO_PRE_RX.finditer(text):
        if m.group("form") and _possessive(text, m):
            continue
        span = company(text, *_clear(text, *m.span("co"), people), vocab, m.group("form") is not None)
        if span:
            cands.append(span + (m.start(), m.end(), "SOCIETE"))
    for m in CO_POST_RX.finditer(text):
        if _possessive(text, m):
            continue
        span = company(text, *_clear(text, *m.span("co"), people), vocab, False, before=True)
        if span:
            cands.append(span + span + ("SOCIETE",))   # étendue sans la forme : l'autre côté reste candidat
    for m in BARE_RX.finditer(text):
        if (bare or BORN_RX.match(text, m.end())) and not any(known(w, vocab) for w in tokens(m.group())):
            cands.append((m.start(), m.end(), m.start(), m.end(), "PERSONNE"))
    if bare:
        cands += [span + span + ("PERSONNE",) for _, span in cells(text, vocab) if span]
    out: List[Cand] = []
    for c in sorted(cands, key=lambda c: (c[2], c[2] - c[3])):
        if (not out or c[2] >= out[-1][3]) and not any(a < c[3] and c[2] < b for a, b in skip):
            out.append(c)
    return out
