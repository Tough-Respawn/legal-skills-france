"""Détection par la structure du contrat : comparution, rôles définis, signatures.

Le bloc de comparution (« Entre les soussignés » jusqu'à « Il a été convenu »)
est lu ligne à ligne et découpé en parties : chaque nom de partie reçoit un
index `party`, le rôle défini par « ci-après » (ou annoncé par « LE SALARIÉ : »),
ses représentants et ses noms de naissance ou d'usage. Partout : civilité suivie
d'un nom, société désignée par sa forme, adresse après « demeurant », « dont le
siège est »… Après « Fait à » ou « Lu et approuvé » en début de ligne : noms des
blocs de signature (colonnes comprises) et commune de « Fait à ». Les
chevauchements avec les règles (regles.py) ne sont pas résolus ici.

La civilité est incluse dans la mention ; la forme sociale (SAS, SCI…) en est
exclue, elle reste visible (spec 6.4).
"""
from __future__ import annotations

import re
from dataclasses import replace
from importlib import resources
from typing import List, Optional, Set, Tuple

from .. import texte
from ..modele import Block, Mention
from .regles import NAME as PLACE, SP

ROLE_WORDS = frozenset({
    "BAILLEUR", "LOCATAIRE", "EMPLOYEUR", "SALARIE", "PRESTATAIRE", "CLIENT", "VENDEUR",
    "ACHETEUR", "CAUTION", "MANDANT", "MANDATAIRE", "PRETEUR", "EMPRUNTEUR", "REPRESENTANT",
    "ACQUEREUR", "CEDANT", "CESSIONNAIRE", "GARANT", "COLOCATAIRE", "PRENEUR",
})
# Féminins et pluriels ramenés au masculin singulier (sur la forme texte.norm).
_SUFFIXES = (("eresse", "eur"), ("euse", "eur"), ("trice", "teur"), ("es", ""), ("e", ""), ("s", ""))
_COLLECTIVE = {"PARTIE", "PARTIES"}  # « ci-après ensemble les Parties » : pas un rôle
_STOPWORDS = {"de", "du", "des", "la", "le", "les", "l", "d", "a", "et", "en", "au", "aux", "un", "une"}

UP = "A-ZÀ-ÖØ-ÞŒ"
LOW = "a-zß-öø-ÿœ"
ALLCAPS = r"[" + UP + r"](?:[" + UP + r"]|['’-][" + UP + r"])+"
FIRST = r"[" + UP + r"][" + LOW + r"]+(?:['’-][" + UP + r"]?[" + LOW + r"]+)*"
CIVILITY = (r"(?:(?:M|MM|MME|MR|MLLE)\.|(?:Mr|Mme|Mmes|Mlle|Dr|Pr|MME|MR|MLLE|PR)\.?|Monsieur|Madame|"
            r"Mademoiselle|MONSIEUR|MADAME|MADEMOISELLE|Me|Maître|MAÎTRE|Docteur|Professeur"
            r"|M(?=" + SP + r"+" + ALLCAPS + SP + r"+" + ALLCAPS + r"))")   # M sans point : « M JEAN DUPONT »
FUNC = (r"(?:Et|ET|Ou|OU|À|AU|AUX|EN|PAR|POUR|SUR|SOUS|DANS|AVEC|CHEZ|DEVANT|CONTRE|ENTRE|ENVERS|SELON|VERS"
        r"|SANS|APRÈS|AVANT|DONT|QUI|QUE)\b")   # mots outils en capitales, jamais dans un nom
CONTEXT = (r"(?i:née?s?|épouse|veuve|divorcée?|dite?|demeurant|domiciliée?s?|représentée?s?"
           r"|ci-après|ci-dessous)\b")
# Mot capitalisé (Jean-Pierre, N'Diaye, DUPONT, LE) : ni mot outil, ni civilité, ni « LE » d'une date (LE 3 MARS).
CAP = (r"(?!" + FUNC + r")(?!" + CONTEXT + r")(?!" + CIVILITY + "(?:" + SP + r"|$))"
       r"(?!(?i:le|la|les|de|du|des)" + SP + r"+\d)[" + UP + r"][^\W\d_]*(?:['’-][^\W\d_]+)*")
PARTICLES = r"(?:de|du|des|da|dos|di|del|el|al|ben|bin|van|von|der|den|ter|le|la)"
JOIN_P = SP + r"(?:" + PARTICLES + SP + r"){0,2}(?:[dl]['’])?"
# Particule en tête de nom (M. de Villiers, Mme d'Arcy) ; jamais « le », « la », « l' » seuls (M. le Maire).
LEAD_P = (r"(?:(?:de|du|des|da|dos|di|del|el|al|ben|bin|van|von|der|den|ter)" + SP + r"+(?:" + PARTICLES + SP
          + r"+)?(?:[dl]['’])?|d['’])")
JOIN_C = SP + r"(?:(?:de|du|des|la|le|les|et|&|au|aux|en|sur)" + SP + r")?(?:[dl]['’])?"
FORMS = r"(?:SAS|SASU|SARL|EURL|SA|SCI|SNC|SCP|SELARL|SELAS|SCM|GIE|SCEA|EARL|SCOP)"
PERSON = CAP + r"(?:" + JOIN_P + CAP + r"){0,3}"
CO_CAP = r"(?!" + FORMS + r"\b)" + CAP  # la forme sociale reste hors du nom
COMPANY = CO_CAP + r"(?:" + JOIN_C + CO_CAP + r"){0,5}"

CIVIL_RX = re.compile(r"(?<![\w.])(?:" + CIVILITY + SP + r"+(?:et|ET)" + SP + r"+)?(?P<civ>" + CIVILITY + ")"
                      + SP + r"+(?P<lead>" + LEAD_P + r")?(?P<name>" + PERSON + ")")
ALIAS_RX = re.compile(r"(?<![\w-])(?i:née|nee|épouse|epouse|veuve|divorcée|divorcee|dite?)" + SP
                      + r"+(?P<name>" + PERSON + ")")
NUMBER_BEFORE_RX = re.compile(r"(?:\d|\b(?i:un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|vingt|cent))"
                              + SP + r"*$")   # « 2 M DE HAUTEUR » : M est une unité
CO_PRE_RX = re.compile(
    r"(?<!\w)(?:(?:[Ll]a|LA)" + SP + r"+(?:société|Société|SOCIÉTÉ)|[Ll]['’](?:association|Association|ASSOCIATION)"
    r"|Société|SOCIÉTÉ|Sté|Ets\.?|Établissements|Etablissements|Association|" + FORMS + r"\b)"
    + SP + r"+(" + COMPANY + ")")
CO_POST_RX = re.compile(r"(?<![\w'’-])(" + COMPANY + ")" + SP + r"+(?P<form>" + FORMS + r")\b")
# Nom sans civilité : DUPONT Jean, Jean DUPONT ; seulement en contexte (comparution, signature, né le).
BARE_RX = re.compile(
    r"(?<![\w'’-])(?:" + ALLCAPS + r"(?:" + SP + ALLCAPS + r")?(?:" + SP + FIRST + r"){1,2}"
    r"|" + FIRST + r"(?:" + SP + FIRST + r")?(?:" + SP + ALLCAPS + r"){1,2})(?![\w'’-])")
BORN_RX = re.compile(r"\s*,?\s*n[ée]e?" + SP + r"+le\b")
LINE_NAME_RX = re.compile(SP + r"*(" + CAP + r"(?:" + JOIN_P + CAP + r"){1,3})" + SP + r"*(?:[,(–-].*)?$")
CELL_RX = re.compile(r"[^\t \u00a0\u202f]+(?:[ \u00a0\u202f][^\t \u00a0\u202f]+)*")  # colonnes : tabulation ou 2 espaces
CAPTION_LEAD_RX = re.compile(r"\s*(?i:(?:pour\s+)?(?:le|la|les|l['’])\s*([^\W\d_]+))\s*[,:]?\s*")
SIG_CAPTION_RX = re.compile(r"\s*(?i:signatures?(?:\s+des\s+parties)?|pour\s+[^.]{1,60})\s*:?\s*")

ART = r"(?:(?:le|la|les|un|une|Le|La|Les|Un|Une)" + SP + r"+|[lL]['’])"
ROLE_RX = re.compile(
    r"(?i:ci[-‐‑\s]?(?:après|dessous))(?:" + SP + r"*,)?"
    r"(?:" + SP + r"+(?i:dénommée?s?|désignée?s?|nommée?s?|appelée?s?))?"
    r"(?:" + SP + r"+(?i:ensemble|collectivement|individuellement))?"
    r"(?:" + SP + r"+(?i:par|sous" + SP + r"+le" + SP + r"+nom" + SP + r"+de))?"
    r"(?:" + SP + r"*[,:])?" + SP + r"*" + ART + r"?"
    r"(?:[«\"“]" + SP + r"*(?P<q>[^»\"”\n]{1,60}?)" + SP + r"*[»\"”]"
    r"|(?P<u>" + ART + r"[^\W\d_]+(?:-[^\W\d_]+)*|" + COMPANY + r"))")
ARTICLE_RX = re.compile(r"(?i:(?:le|la|les|un|une)\s+|l['’]\s*)")
PREFIX_ROLE_RX = re.compile(r"(?:^|(?<=[,;.:]))\s*(?i:(?:le|la|les|l['’])" + SP + r"*([^\W\d_]+))" + SP + r"*:")
REP_RX = re.compile(r"(?i:représenté(?:e|s|es)?)" + SP + r"+(?i:par)\b")
SEP_RX = re.compile(r"(?i:\bd['’](?:une|autre)" + SP + r"+part\b)|(?:^|(?<=[,;.:]))\s*(?:Et|ET)\b")
_REP_REACH = 120  # caractères max entre « représenté par » (ou un représentant) et le représentant suivant

ADDR_RX = re.compile(
    r"(?<!\w)(?i:demeurant|domiciliée?s?|dont" + SP + r"+le" + SP + r"+siège(?:" + SP + r"+social)?" + SP
    + r"+est(?:" + SP + r"+situé|" + SP + r"+sis)?(?:" + SP + r"+au|" + SP + r"+à)?|sise?(?:" + SP + r"+à|"
    + SP + r"+au)?|résidant|habitant)" + SP + r"+(?i:(?:ensemble|au|à|aux)" + SP + r"+)?")
POSTAL_RX = re.compile(r"\d{5}" + SP + r"?" + PLACE)
ADDR_STOP_RX = re.compile(r"[;\n]|,?" + SP + r"*\b(?:(?i:née?s?\b|représenté|ci-après|ci-dessous|immatricul"
                          r"|d['’](?:une|autre)" + SP + r"+part|de" + SP + r"+nationalité|agissant|en" + SP
                          + r"+qualité)|(?:Et|ET)\b)")
ADDR_NEXT_RX = re.compile(r"," + SP + r"*[" + UP + r"0-9][^,;\n]*")
_ADDR_REACH = 120

START_RX = re.compile(r"\s*(?:ENTRE\b|(?i:entre)(?:(?i:\s+les\s+soussign|\s+d['’](?:une|autre)\s+part)"
                      r"|\s*[:,]|\s*$))")
# « Entre la société X », « Entre M. X » : ouvre seulement si un nom commence à cet endroit (_opens).
START_NAME_RX = re.compile(r"\s*(?i:entre)\s+(?P<key>(?i:la\s+société|l['’]association)\b|(?=" + CIVILITY + SP
                           + r")|" + FORMS + r"\b)")
END_RX = re.compile(
    r"(?:^|(?<=[.:;]))\s*(?i:il\s+(?:a\s+été|est)\s+(?:préalablement\s+)?(?:convenu|arrêté|exposé)"
    r"|préambule|ceci\s+exposé|exposé\b|art(?:icle|\.)\s*(?:1(?!\d)|1er|premier|i\b))")
# Marqueur de signature en début de ligne, ou « Fait à » après une fin de phrase ; jamais cité dans une clause.
SIGNED_RX = re.compile(r"(?m)^[\W_]*(?i:fait" + SP + r"+à\b|lu\s+et\s+approuvé|signatures?\b)"
                       r"|(?<=[.!?])" + SP + r"*(?:Fait|FAIT)" + SP + r"+(?:à|À)\b")
HEADING_RX = re.compile(r"\s*(?:ANNEXE|Annexe|ARTICLE|Article|TITRE|Titre|CHAPITRE|Chapitre)\b")
FAIT_RX = re.compile(r"\b(?:Fait|FAIT)" + SP + r"+(?:à|À)" + SP + r"+(" + PLACE + ")")
WORD_RX = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*")

Cand = Tuple[int, int, int, int, str]  # début, fin, étendue (début, fin) du motif, type (ALIAS = nom d'usage)
Span = Tuple[int, int]


def load_vocab() -> Set[str]:
    """Vocabulaire livré (data/vocabulaire.txt), en formes texte.norm, sans les commentaires."""
    raw = (resources.files("legal_anonymiser") / "data" / "vocabulaire.txt").read_text(encoding="utf-8")
    return {texte.norm(line) for line in raw.splitlines() if line.strip() and not line.lstrip().startswith("#")}


def _forms(word: str) -> List[str]:
    """Forme normalisée et ses variantes au masculin singulier (vendeuse, garants…)."""
    n = texte.norm(word)
    return [n] + [n[:-len(a)] + b for a, b in _SUFFIXES if n.endswith(a) and len(n) > len(a) + 2]


def _known(word: str, vocab: Set[str]) -> bool:
    return any(f in vocab or f.upper() in ROLE_WORDS for f in _forms(word))


def _tokens(s: str) -> List[str]:
    """Mots porteurs de sens : élisions retirées (d'Effet), mots vides écartés."""
    words = (re.sub(r"^[dlDL]'", "", texte.norm(w)) for w in WORD_RX.findall(s))
    return [w for w in words if w and w not in _STOPWORDS]


def _role(term: str, vocab: Set[str]) -> Optional[str]:
    """Rôle canonique d'un terme défini ; "" s'il est à ignorer ; None s'il ressemble à un nom propre."""
    words = _tokens(term)
    if len(words) == 1:
        for f in _forms(words[0]):
            if f.upper() in ROLE_WORDS:
                return f.upper()
    if not words or not all(_known(w, vocab) for w in words):
        return None
    key = re.sub(r"[^A-Z0-9]+", "_", texte.norm(term).upper()).strip("_")
    return "" if key in _COLLECTIVE else key


def _roles(text: str) -> List[Tuple[int, int, int, int]]:
    """Définitions « ci-après » : (début, fin du motif, début, fin du terme sans article)."""
    out = []
    for m in ROLE_RX.finditer(text):
        s, e = m.span("q" if m.group("q") else "u")
        a = ARTICLE_RX.match(text, s)
        out.append((m.start(), m.end(), a.end() if a and a.end() < e else s, e))
    return out


def _addresses(text: str) -> List[Span]:
    """Adresse après « demeurant », « dont le siège est »… : jusqu'au code postal et sa commune,
    sinon jusqu'à la virgule, en gardant les segments suivants qui commencent par une majuscule."""
    out = []
    for m in ADDR_RX.finditer(text):
        s = m.end()
        stop = ADDR_STOP_RX.search(text, s, s + _ADDR_REACH)
        limit = stop.start() if stop else min(len(text), s + _ADDR_REACH)
        postal = POSTAL_RX.search(text, s, limit)
        if postal:
            e = postal.end()
        else:
            e = s + len(re.match(r"[^,;\n]*", text[s:limit]).group())
            nxt = ADDR_NEXT_RX.match(text, e, limit)
            while nxt:
                e = nxt.end()
                nxt = ADDR_NEXT_RX.match(text, e, limit)
        e = len(text[:e].rstrip(" ,.\u00a0\u202f"))
        if e > s:
            out.append((s, e))
    return out


def _trim(text: str, s: int, e: int, vocab: Set[str]) -> Span:
    """Nom de société sans les mots du vocabulaire en tête ; vide s'il n'a que des mots connus ou vides."""
    words = list(WORD_RX.finditer(text, s, e))
    if all(_known(w.group(), vocab) or texte.norm(w.group()) in _STOPWORDS for w in words):
        return e, e
    return next(w.start() for w in words if not _known(w.group(), vocab)), e


def _cells(text: str, vocab: Set[str]) -> List[Tuple[bool, Optional[Span]]]:
    """Colonnes d'une ligne de signature : (légende ?, nom seul de la colonne)."""
    out = []
    for c in CELL_RX.finditer(text):
        s, cell = c.start(), c.group()
        lead = CAPTION_LEAD_RX.match(cell)
        role_lead = bool(lead) and bool(_role(lead.group(1), set()))
        if role_lead:
            s += lead.end()
        m = LINE_NAME_RX.match(text, s, c.end())
        name = m.span(1) if m and not any(_known(w, vocab) for w in _tokens(m.group(1))) else None
        caption = bool(SIG_CAPTION_RX.fullmatch(cell)) or (role_lead and (s == c.end() or name is not None))
        out.append((caption, name))
    return out


def _names(text: str, vocab: Set[str], bare: bool, skip: List[Span]) -> List[Cand]:
    """Noms de personnes et de sociétés, sans chevauchement (le motif le plus à gauche puis le plus long)."""
    cands: List[Cand] = []
    for m in CIVIL_RX.finditer(text):
        if m.group("lead") and all(_known(w, vocab) for w in _tokens(m.group("name"))):
            continue  # « Maître d'Œuvre »
        if m.group("civ") == "M" and NUMBER_BEFORE_RX.search(text, max(0, m.start() - 12), m.start()):
            continue  # « 2 M DE HAUTEUR »
        cands.append((m.start(), m.end(), m.start(), m.end(), "PERSONNE"))
    for m in ALIAS_RX.finditer(text):
        if not all(_known(w, vocab) for w in _tokens(m.group("name"))):   # pas « la dite Société »
            cands.append((m.start("name"), m.end(), m.start(), m.end(), "ALIAS"))
    pre: Set[int] = set()
    for m in CO_PRE_RX.finditer(text):
        s, e = _trim(text, *m.span(1), vocab)
        if s < e:
            cands.append((s, e, m.start(), m.end(), "SOCIETE"))
            pre.add(m.start())
    for m in CO_POST_RX.finditer(text):
        s, e = _trim(text, *m.span(1), vocab)
        if s < e and m.start("form") not in pre:   # « ASSIGNATION DE LA SARL X » : le nom suit la forme
            cands.append((s, e, m.start(), m.end(), "SOCIETE"))
    for m in BARE_RX.finditer(text):
        if (bare or BORN_RX.match(text, m.end())) and not any(_known(w, vocab) for w in _tokens(m.group())):
            cands.append((m.start(), m.end(), m.start(), m.end(), "PERSONNE"))
    if bare:
        cands += [span + span + ("PERSONNE",) for _, span in _cells(text, vocab) if span]
    out: List[Cand] = []
    for c in sorted(cands, key=lambda c: (c[2], c[2] - c[3])):
        if (not out or c[2] >= out[-1][3]) and not any(a < c[3] and c[2] < b for a, b in skip):
            out.append(c)
    return out


class _Comparution:
    """État du bloc de comparution : parties numérotées, groupe courant, représentant attendu."""

    def __init__(self, vocab: Set[str]) -> None:
        self.vocab = vocab
        self.records: List[list] = []   # [bloc, début, fin, type, rôle, partie]
        self.parties = 0
        self.reset()

    def reset(self) -> None:
        self.group: List[list] = []     # parties nommées depuis le dernier « Et » / « d'une part »
        self.rep_at: Optional[int] = None   # position absolue de « représenté par » ou du dernier représentant
        self.prefix: Optional[str] = None   # rôle annoncé avant le nom (« LE SALARIÉ : »)
        self.last: Optional[list] = None    # dernière personne nommée, à qui se rattache « née MARTIN »

    def feed(self, bi: int, base: int, origin: int, text: str) -> None:
        """Lit un segment de comparution ; origin est sa position absolue dans le document."""
        roles, addresses = _roles(text), _addresses(text)
        self.records += [[bi, base + s, base + e, "ADRESSE", None, None] for s, e in addresses]
        skip = [(r[0], r[1]) for r in roles] + addresses
        events = [(c[2], "name", c) for c in _names(text, self.vocab, True, skip)]
        events += [(m.start(), "sep", None) for m in SEP_RX.finditer(text)]
        events += [(m.end(), "rep", None) for m in REP_RX.finditer(text)]
        events += [(r[0], "role", r) for r in roles]
        events += [(m.start(), "prefix", m.group(1)) for m in PREFIX_ROLE_RX.finditer(text)]
        for pos, what, data in sorted(events, key=lambda ev: ev[0]):
            if what == "sep":
                self.reset()
            elif what == "rep":
                self.rep_at = origin + pos
            elif what == "prefix":
                self.prefix = _role(data, set()) or None
            elif what == "name":
                self._name(bi, base, origin, data)
            else:
                self._role(bi, base, text, data)

    def _name(self, bi: int, base: int, origin: int, cand: Cand) -> None:
        s, e, xs, _, kind = cand
        party = self.group[-1][5] if self.group else None
        last = self.last
        if kind == "ALIAS":   # née MARTIN, épouse LEROY : même personne, même partie, même rôle
            rec = [bi, base + s, base + e, "PERSONNE", last[4] if last else None, last[5] if last else None]
            if last and last[4] == "REPRESENTANT":
                self.rep_at = origin + e
            else:
                self.group.append(rec)
        elif self.rep_at is not None and origin + xs - self.rep_at <= _REP_REACH:
            rec = [bi, base + s, base + e, kind, "REPRESENTANT", party]
            self.rep_at = origin + e   # un second représentant peut suivre (« et Mme Y »)
        else:
            rec = [bi, base + s, base + e, kind, self.prefix, self.parties]
            self.parties += 1
            self.group.append(rec)
            self.rep_at = None
        self.records.append(rec)
        self.last = rec

    def _role(self, bi: int, base: int, text: str, data: Tuple[int, int, int, int]) -> None:
        ts, te = data[2], data[3]
        role = _role(text[ts:te], self.vocab)
        if role is None:   # terme défini à allure de nom propre : entité à masquer (6.6)
            last = self.group[-1] if self.group else None
            self.records.append([bi, base + ts, base + te, last[3] if last else "SOCIETE",
                                 None, last[5] if last else None])
        elif role:
            for rec in self.group:
                if rec[4] is None:
                    rec[4] = role
        self.rep_at = None


def _outside(bi: int, base: int, text: str, vocab: Set[str], sig: bool) -> List[Mention]:
    """Mentions hors comparution : noms, adresses, termes définis à allure de nom propre, « Fait à »."""
    roles, addresses = _roles(text), _addresses(text)
    skip = [(r[0], r[1]) for r in roles] + addresses
    out = [Mention(bi, base + s, base + e, "PERSONNE" if kind == "ALIAS" else kind, "structure")
           for s, e, _, _, kind in _names(text, vocab, sig, skip)]
    out += [Mention(bi, base + s, base + e, "ADRESSE", "structure") for s, e in addresses]
    out += [Mention(bi, base + ts, base + te, "SOCIETE", "structure")
            for _, _, ts, te in roles if _role(text[ts:te], vocab) is None]
    out += [Mention(bi, base + m.start(1), base + m.end(1), "COMMUNE", "structure") for m in FAIT_RX.finditer(text)]
    return out


def _opens(line: str, vocab: Set[str]) -> bool:
    """Début de comparution : « Entre les soussignés », ou « Entre » suivi d'un vrai nom de partie."""
    if START_RX.match(line):
        return True
    m = START_NAME_RX.match(line)
    return bool(m) and any(c[2] == m.start("key") for c in _names(line, vocab, False, []))


def find(blocks: List[Block], vocab: Set[str]) -> List[Mention]:
    """Mentions de la couche structure (source « structure »), sans résoudre les chevauchements."""
    comp = _Comparution(vocab)
    out: List[Mention] = []
    in_comp = sig = False
    origin = 0   # position absolue du bloc, pour mesurer une distance d'un bloc à l'autre
    for bi, block in enumerate(blocks):
        for lm in re.finditer(r"[^\n]+", block.text):
            line, base, cut = lm.group(), lm.start(), 0
            if not in_comp and _opens(line, vocab):
                in_comp, sig = True, False
                comp.reset()
            if in_comp and SIGNED_RX.search(line):
                in_comp = False
            if in_comp:
                end = END_RX.search(line)
                cut = end.start() if end else len(line)
                comp.feed(bi, base, origin + base, line[:cut])
                in_comp = end is None
            if in_comp:
                continue
            if HEADING_RX.match(line):
                sig = False
            cells = _cells(line, vocab)
            if SIGNED_RX.search(line) or (cells and all(caption for caption, _ in cells)):
                sig = True
            out += _outside(bi, base + cut, line[cut:], vocab, sig)
        origin += len(block.text) + 1
    out += [Mention(b, s, e, k, "structure", r, p) for b, s, e, k, r, p in comp.records]
    return sorted(out, key=lambda m: (m.block, m.start, m.end))


def relabel_signature_images(blocks: List[Block]) -> List[Block]:
    """[IMAGE] devient [SIGNATURE] à partir du premier bloc dont une ligne commence par « Fait à »,
    « Lu et approuvé » ou « Signature(s) »."""
    out, signed = [], False
    for b in blocks:
        signed = signed or bool(SIGNED_RX.search(b.text))
        out.append(replace(b, text=b.text.replace("[IMAGE]", "[SIGNATURE]")) if signed else b)
    return out
