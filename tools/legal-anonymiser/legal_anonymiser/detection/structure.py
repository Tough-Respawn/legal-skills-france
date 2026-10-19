"""Détection par la structure du contrat : comparution, rôles définis, signatures.

Le bloc de comparution (« Entre les soussignés » jusqu'à « Il a été convenu »)
est lu ligne à ligne et découpé en parties : chaque nom de partie reçoit un
index `party`, le rôle défini par « ci-après » (ou annoncé par « LE SALARIÉ : »),
ses représentants et ses noms de naissance ou d'usage. Partout : civilité suivie
d'un nom, société désignée par sa forme (noms.py), adresse après « demeurant »,
« dont le siège est »… Après « Fait à », « Lu et approuvé » ou « Signature » en
début de ligne, ou « Fait à <Lieu> » après une fin de phrase (lieu qui ne commence
ni par un article ni par une préposition et n'est pas fait que de mots connus) :
noms des blocs de signature (colonnes comprises) et commune de « Fait à ». Les
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
from .noms import (ART_WORDS, CIVILITY, COMPANY, FORMS, ROLE_WORDS, UP, WORD_RX, Cand, Span,  # noqa: F401
                   cells, known, names, role, stem)
from .regles import NAME as PLACE, SP

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
# Arrêt sur « , Et Mme Y », ou « ET » devant une civilité ou une forme sociale même sans virgule ;
# jamais dans « RUE PIERRE ET MARIE CURIE ».
ADDR_STOP_RX = re.compile(r"[;\n]|,?" + SP + r"*\b(?i:née?s?\b|représenté|ci-après|ci-dessous|immatricul"
                          r"|d['’](?:une|autre)" + SP + r"+part|de" + SP + r"+nationalité|agissant|en" + SP
                          + r"+qualité)|," + SP + r"*(?:Et|ET)\b|" + SP + r"+(?:Et|ET|et)" + SP + r"+(?="
                          + CIVILITY + "|" + FORMS + r"\b)")
ADDR_NEXT_RX = re.compile(r"," + SP + r"*[" + UP + r"0-9][^,;\n]*")
_ADDR_REACH = 120

START_RX = re.compile(r"\s*(?i:entre)(?:(?i:\s+les\s+(?:parties\s+)?soussign|\s+d['’](?:une|autre)\s+part)"
                      r"|\s*[:,]|\s*$)")
# « Entre la société X », « ENTRE LA SARL X », « Entre M. X » : ouvre seulement si un nom suit (_opens).
START_NAME_RX = re.compile(r"\s*(?i:entre)" + SP + r"+")
ARTICLE_GAP_RX = re.compile(r"(?i:(?:la|le|les)" + SP + r"+|l['’])?")
END_RX = re.compile(
    r"(?:^|(?<=[.:;]))\s*(?i:il\s+(?:a\s+été|est)\s+(?:préalablement\s+)?(?:convenu|arrêté|exposé)"
    r"|préambule|ceci\s+exposé|exposé\b|art(?:icle|\.)\s*(?:1(?!\d)|1er|premier|i\b))")
# Marqueur de signature en début de ligne (« Fait à la demande » exclu), jamais cité dans une clause
# (« lu et approuvé » entre guillemets) ; « Fait à <Lieu> » après une fin de phrase passe par _signed.
SIGNED_RX = re.compile(r"(?m)^[\W_]*(?i:fait" + SP + r"+à\b(?!" + SP + r"+" + ART_WORDS + r"\b)"
                       r"|lu\s+et\s+approuvé|signatures?\b)")
FAIT_MID_RX = re.compile(r"(?<=[.!?])" + SP + r"*(?:Fait|FAIT)" + SP + r"+(?:à|À)" + SP + r"+(" + PLACE + ")")
HEADING_RX = re.compile(r"\s*(?:ANNEXE|Annexe|ARTICLE|Article|TITRE|Titre|CHAPITRE|Chapitre)\b")
FAIT_RX = re.compile(r"\b(?:Fait|FAIT)" + SP + r"+(?:à|À)" + SP + r"+(" + PLACE + ")")
_PLACE_STOP = {"le", "la", "les", "un", "une", "de", "du", "des", "a", "au", "aux", "en", "par", "pour", "sur"}


def load_vocab() -> Set[str]:
    """Vocabulaire livré (data/vocabulaire.txt), en formes texte.norm, sans les commentaires."""
    raw = (resources.files("legal_anonymiser") / "data" / "vocabulaire.txt").read_text(encoding="utf-8")
    return {texte.norm(line) for line in raw.splitlines() if line.strip() and not line.lstrip().startswith("#")}


def _place(name: str, vocab: Set[str]) -> bool:
    """Lieu plausible après « Fait à » : ni article ni préposition en tête (« LA DEMANDE DU BAILLEUR »),
    pas seulement des mots connus (« TITRE »)."""
    words = WORD_RX.findall(name)
    return bool(words) and stem(words[0]) not in _PLACE_STOP and not all(known(w, vocab) for w in words)


def _signed(text: str, vocab: Set[str]) -> bool:
    """Vrai si une ligne ouvre la zone de signature (début de ligne, ou « Fait à <Lieu> » après une phrase)."""
    return bool(SIGNED_RX.search(text)) or any(_place(m.group(1), vocab) for m in FAIT_MID_RX.finditer(text))


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
        events = [(c[2], "name", c) for c in names(text, self.vocab, True, skip)]
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
                self.prefix = role(data, set()) or None
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
        found = role(text[ts:te], self.vocab)
        if found is None:   # terme défini à allure de nom propre : entité à masquer (6.6)
            last = self.group[-1] if self.group else None
            self.records.append([bi, base + ts, base + te, last[3] if last else "SOCIETE",
                                 None, last[5] if last else None])
        elif found:
            for rec in self.group:
                if rec[4] is None:
                    rec[4] = found
        self.rep_at = None


def _outside(bi: int, base: int, text: str, vocab: Set[str], sig: bool) -> List[Mention]:
    """Mentions hors comparution : noms, adresses, termes définis à allure de nom propre, « Fait à »."""
    roles, addresses = _roles(text), _addresses(text)
    skip = [(r[0], r[1]) for r in roles] + addresses
    out = [Mention(bi, base + s, base + e, "PERSONNE" if kind == "ALIAS" else kind, "structure")
           for s, e, _, _, kind in names(text, vocab, sig, skip)]
    out += [Mention(bi, base + s, base + e, "ADRESSE", "structure") for s, e in addresses]
    out += [Mention(bi, base + ts, base + te, "SOCIETE", "structure")
            for _, _, ts, te in roles if role(text[ts:te], vocab) is None]
    out += [Mention(bi, base + m.start(1), base + m.end(1), "COMMUNE", "structure")
            for m in FAIT_RX.finditer(text) if _place(m.group(1), vocab)]
    return out


def _opens(line: str, vocab: Set[str]) -> bool:
    """Début de comparution : « Entre les soussignés », ou « Entre » suivi (après un article au plus)
    d'un vrai nom de partie, en minuscules comme en capitales."""
    if START_RX.match(line):
        return True
    m = START_NAME_RX.match(line)
    first = next((c for c in names(line, vocab, False, []) if c[2] >= m.end()), None) if m else None
    return bool(first) and bool(ARTICLE_GAP_RX.fullmatch(line, m.end(), first[2]))


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
            if in_comp and _signed(line, vocab):
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
            columns = cells(line, vocab)
            if _signed(line, vocab) or (columns and all(caption for caption, _ in columns)):
                sig = True
            out += _outside(bi, base + cut, line[cut:], vocab, sig)
        origin += len(block.text) + 1
    out += [Mention(b, s, e, k, "structure", r, p) for b, s, e, k, r, p in comp.records]
    return sorted(out, key=lambda m: (m.block, m.start, m.end))


def relabel_signature_images(blocks: List[Block]) -> List[Block]:
    """[IMAGE] devient [SIGNATURE] à partir du premier bloc dont une ligne commence par « Fait à »,
    « Lu et approuvé » ou « Signature(s) », ou qui contient « Fait à <Lieu> » après une fin de phrase."""
    vocab = load_vocab()
    out, signed = [], False
    for b in blocks:
        signed = signed or _signed(b.text, vocab)
        out.append(replace(b, text=b.text.replace("[IMAGE]", "[SIGNATURE]")) if signed else b)
    return out
