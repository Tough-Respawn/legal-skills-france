"""Détection par la structure du contrat : comparution, rôles définis, signatures.

Le bloc de comparution (« Entre les soussignés » jusqu'à « Il a été convenu »)
est lu ligne à ligne et découpé en parties : chaque nom de partie reçoit un
index `party`, le rôle défini par « ci-après » et ses représentants. Hors
comparution : civilité suivie d'un nom, société désignée par sa forme, noms des
blocs de signature et commune de « Fait à ». Les adresses relèvent des règles
(regles.py) ; les chevauchements ne sont pas résolus ici.

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
})
_FEMININE = {"BAILLERESSE": "BAILLEUR", "VENDERESSE": "VENDEUR", "ACHETEUSE": "ACHETEUR",
             "PRETEUSE": "PRETEUR", "EMPRUNTEUSE": "EMPRUNTEUR"}
_COLLECTIVE = {"PARTIE", "PARTIES"}  # « ci-après ensemble les Parties » : pas un rôle

UP = "A-ZÀ-ÖØ-ÞŒ"
LOW = "a-zß-öø-ÿœ"
CIVILITY = (r"(?:(?:M|MM)\.|(?:Mr|Mme|Mmes|Mlle|Dr)\.?|Monsieur|Madame|Mademoiselle|"
            r"MONSIEUR|MADAME|MADEMOISELLE|Me|Maître|MAÎTRE|Docteur)")
# Mot capitalisé (Jean-Pierre, N'Diaye, DUPONT) qui n'est ni « Et » ni une civilité.
CAP = (r"(?!(?:Et|ET|Ou|OU)\b)(?!" + CIVILITY + "(?:" + SP + r"|$))"
       r"[" + UP + r"][^\W\d_]*(?:['’-][^\W\d_]+)*")
JOIN_P = SP + r"(?:(?:de|du|des|le|la|van|von)" + SP + r"){0,2}(?:[dl]['’])?"
JOIN_C = SP + r"(?:(?:de|du|des|la|le|les|et|&|au|aux|en|sur)" + SP + r")?(?:[dl]['’])?"
FORMS = r"(?:SAS|SASU|SARL|EURL|SA|SCI|SNC|SCP|SELARL|SELAS|SCM|GIE|SCEA|EARL|SCOP)"
PERSON = CAP + r"(?:" + JOIN_P + CAP + r"){0,3}"
CO_CAP = r"(?!" + FORMS + r"\b)" + CAP  # la forme sociale reste hors du nom
COMPANY = CO_CAP + r"(?:" + JOIN_C + CO_CAP + r"){0,5}"
ALLCAPS = r"[" + UP + r"](?:[" + UP + r"]|['’-][" + UP + r"])+"
FIRST = r"[" + UP + r"][" + LOW + r"]+(?:['’-][" + UP + r"]?[" + LOW + r"]+)*"

CIVIL_RX = re.compile(r"(?<![\w.])" + CIVILITY + SP + r"+" + PERSON)
CO_PRE_RX = re.compile(
    r"(?<!\w)(?:(?:[Ll]a|LA)" + SP + r"+(?:société|Société|SOCIÉTÉ)|[Ll]['’](?:association|Association)"
    r"|Société|SOCIÉTÉ|Sté|Ets\.?|Établissements|Etablissements|Association|" + FORMS + r"\b)"
    + SP + r"+(" + COMPANY + ")")
CO_POST_RX = re.compile(r"(?<![\w'’-])(" + COMPANY + ")" + SP + r"+" + FORMS + r"\b")
# Nom sans civilité : DUPONT Jean, Jean DUPONT ; seulement en contexte (comparution, signature, né le).
BARE_RX = re.compile(
    r"(?<![\w'’-])(?:" + ALLCAPS + r"(?:" + SP + ALLCAPS + r")?(?:" + SP + FIRST + r"){1,2}"
    r"|" + FIRST + r"(?:" + SP + FIRST + r")?(?:" + SP + ALLCAPS + r"){1,2})(?![\w'’-])")
BORN_RX = re.compile(r"\s*,?\s*n[ée]e?" + SP + r"+le\b")
LINE_NAME_RX = re.compile(r"^" + SP + r"*(" + CAP + r"(?:" + JOIN_P + CAP + r"){1,3})" + SP
                          + r"*(?:[,(–-].*)?$")

ART = r"(?:(?:le|la|les|un|une|Le|La|Les|Un|Une)" + SP + r"+|[lL]['’])"
ROLE_RX = re.compile(
    r"(?i:ci[-‐‑\s]?après)" + SP + r"*,?"
    r"(?:" + SP + r"+(?i:dénommée?s?|désignée?s?|nommée?s?|appelée?s?))?"
    r"(?:" + SP + r"+(?i:ensemble|collectivement|individuellement))?"
    + SP + r"*[,:]?" + SP + r"*" + ART + r"?"
    r"(?:[«\"“]" + SP + r"*(?P<q>[^»\"”\n]{1,60}?)" + SP + r"*[»\"”]"
    r"|(?P<u>" + ART + r"[^\W\d_]+(?:-[^\W\d_]+)*|" + COMPANY + r"))")
ARTICLE_RX = re.compile(r"(?i:(?:le|la|les|un|une)\s+|l['’]\s*)")
REP_RX = re.compile(r"(?i:représenté(?:e|s|es)?)" + SP + r"+(?i:par)\b")
SEP_RX = re.compile(r"(?i:\bd['’](?:une|autre)" + SP + r"+part\b)|(?:^|(?<=[,;.:]))\s*(?:Et|ET)\b")
_REP_REACH = 80  # caractères max entre « représenté par » et le nom du représentant

START_RX = re.compile(r"\s*(?:ENTRE\b|(?i:entre)(?:\s+les\s+soussign|\s+d['’](?:une|autre)\s+part"
                      r"|\s*[:,]|\s*$))")
END_RX = re.compile(
    r"(?:^|(?<=[.:;]))\s*(?i:il\s+(?:a\s+été|est)\s+(?:préalablement\s+)?(?:convenu|arrêté|exposé)"
    r"|préambule|ceci\s+exposé|exposé\b|art(?:icle|\.)\s*(?:1(?!\d)|1er|premier|i\b))")
SIGNED_RX = re.compile(r"\bFait" + SP + r"+à\b|(?i:\blu\s+et\s+approuvé)")
CAPTION_RX = re.compile(r"\s*(?i:signatures?(?:\s+des\s+parties)?|pour\s+[^.]{1,60}|(?:le|la|l['’]|les)"
                        r"\s*([^\W\d_]+))\s*:?\s*$")
HEADING_RX = re.compile(r"\s*(?:ANNEXE|Annexe|ARTICLE|Article|TITRE|Titre|CHAPITRE|Chapitre)\b")
FAIT_RX = re.compile(r"\bFait" + SP + r"+à" + SP + r"+(" + PLACE + ")")
WORD_RX = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*")

Cand = Tuple[int, int, int, int, str]  # début, fin, étendue (début, fin) du motif, type


def load_vocab() -> Set[str]:
    """Vocabulaire livré (data/vocabulaire.txt), en formes texte.norm, sans les commentaires."""
    raw = (resources.files("legal_anonymiser") / "data" / "vocabulaire.txt").read_text(encoding="utf-8")
    return {texte.norm(line) for line in raw.splitlines() if line.strip() and not line.lstrip().startswith("#")}


def _known(word: str, vocab: Set[str]) -> bool:
    n = texte.norm(word).replace("’", "'")
    return n in vocab or n.upper() in ROLE_WORDS


def _role(term: str, vocab: Set[str]) -> Optional[str]:
    """Rôle canonique d'un terme défini ; "" s'il est à ignorer ; None s'il ressemble à un nom propre."""
    key = re.sub(r"[^A-Z0-9]+", "_", texte.norm(term).upper()).strip("_")
    key = _FEMININE.get(key, key)
    for cand in (key, key[:-1], key[:-2]):  # pluriel, féminin : SALARIEES -> SALARIE
        if cand in ROLE_WORDS:
            return cand
    if not all(_known(w, vocab) for w in WORD_RX.findall(term)):
        return None
    return "" if key in _COLLECTIVE else key


def _roles(text: str) -> List[Tuple[int, int, int, int]]:
    """Définitions « ci-après » : (début, fin du motif, début, fin du terme sans article)."""
    out = []
    for m in ROLE_RX.finditer(text):
        g = "q" if m.group("q") else "u"
        s, e = m.span(g)
        a = ARTICLE_RX.match(text, s)
        out.append((m.start(), m.end(), a.end() if a and a.end() < e else s, e))
    return out


def _trim(text: str, s: int, e: int, vocab: Set[str]) -> Tuple[int, int]:
    """Retire les mots du vocabulaire en tête d'un nom de société (Société Civile Immobilière X)."""
    for w in WORD_RX.finditer(text, s, e):
        if not _known(w.group(), vocab):
            return w.start(), e
    return e, e


def _names(text: str, vocab: Set[str], bare: bool, skip: List[Tuple[int, int]]) -> List[Cand]:
    """Noms de personnes et de sociétés, sans chevauchement (le motif le plus à gauche puis le plus long)."""
    cands: List[Cand] = [(m.start(), m.end(), m.start(), m.end(), "PERSONNE") for m in CIVIL_RX.finditer(text)]
    for rx in (CO_PRE_RX, CO_POST_RX):
        for m in rx.finditer(text):
            s, e = _trim(text, *m.span(1), vocab)
            if s < e:
                cands.append((s, e, m.start(), m.end(), "SOCIETE"))
    for m in BARE_RX.finditer(text):
        if (bare or BORN_RX.match(text, m.end())) and not any(_known(w, vocab) for w in WORD_RX.findall(m.group())):
            cands.append((m.start(), m.end(), m.start(), m.end(), "PERSONNE"))
    line = LINE_NAME_RX.match(text) if bare else None
    if line and not any(_known(w, vocab) for w in WORD_RX.findall(line.group(1))):
        cands.append((line.start(1), line.end(1), line.start(1), line.end(1), "PERSONNE"))
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
        self.group: List[list] = []     # parties nommées depuis le dernier « Et » / « d'une part »
        self.rep_at: Optional[int] = None

    def reset(self) -> None:
        self.group, self.rep_at = [], None

    def feed(self, bi: int, base: int, text: str) -> None:
        roles = _roles(text)
        events = [(c[2], "name", c) for c in _names(text, self.vocab, True, [(r[0], r[1]) for r in roles])]
        events += [(m.start(), "sep", None) for m in SEP_RX.finditer(text)]
        events += [(m.end(), "rep", None) for m in REP_RX.finditer(text)]
        events += [(r[0], "role", r) for r in roles]
        for pos, what, data in sorted(events, key=lambda ev: ev[0]):
            if what == "sep":
                self.reset()
            elif what == "rep":
                self.rep_at = pos
            elif what == "name":
                s, e, _, _, kind = data
                if self.rep_at is not None and pos - self.rep_at <= _REP_REACH:
                    party = self.group[-1][5] if self.group else None
                    self.records.append([bi, base + s, base + e, kind, "REPRESENTANT", party])
                else:
                    rec = [bi, base + s, base + e, kind, None, self.parties]
                    self.parties += 1
                    self.group.append(rec)
                    self.records.append(rec)
                self.rep_at = None
            else:
                ts, te = data[2], data[3]
                role = _role(text[ts:te], self.vocab)
                if role is None:
                    last = self.group[-1] if self.group else None
                    self.records.append([bi, base + ts, base + te, last[3] if last else "SOCIETE",
                                         None, last[5] if last else None])
                elif role:
                    for rec in self.group:
                        if rec[4] is None:
                            rec[4] = role
                self.rep_at = None


def _outside(bi: int, base: int, text: str, vocab: Set[str], sig: bool) -> List[Mention]:
    """Mentions hors comparution : noms, termes définis à allure de nom propre, « Fait à »."""
    roles = _roles(text)
    out = [Mention(bi, base + s, base + e, kind, "structure")
           for s, e, _, _, kind in _names(text, vocab, sig, [(r[0], r[1]) for r in roles])]
    out += [Mention(bi, base + ts, base + te, "SOCIETE", "structure")
            for _, _, ts, te in roles if _role(text[ts:te], vocab) is None]
    out += [Mention(bi, base + m.start(1), base + m.end(1), "COMMUNE", "structure") for m in FAIT_RX.finditer(text)]
    return out


def _caption(line: str) -> bool:
    """Ligne seule de bloc de signature : « Signature », « Pour la société X », « Le Bailleur »."""
    m = CAPTION_RX.match(line)
    return bool(m) and (m.group(1) is None or _role(m.group(1), set()) not in (None, ""))


def find(blocks: List[Block], vocab: Set[str]) -> List[Mention]:
    """Mentions de la couche structure (source « structure »), sans résoudre les chevauchements."""
    comp = _Comparution(vocab)
    out: List[Mention] = []
    in_comp = sig = False
    for bi, block in enumerate(blocks):
        for lm in re.finditer(r"[^\n]+", block.text):
            line, base, cut = lm.group(), lm.start(), 0
            if not in_comp and START_RX.match(line):
                in_comp, sig = True, False
                comp.reset()
            if in_comp and SIGNED_RX.search(line):
                in_comp = False
            if in_comp:
                end = END_RX.search(line)
                cut = end.start() if end else len(line)
                comp.feed(bi, base, line[:cut])
                in_comp = end is None
            if in_comp:
                continue
            if HEADING_RX.match(line):
                sig = False
            if SIGNED_RX.search(line) or _caption(line):
                sig = True
            out += _outside(bi, base + cut, line[cut:], vocab, sig)
    out += [Mention(b, s, e, k, "structure", r, p) for b, s, e, k, r, p in comp.records]
    return sorted(out, key=lambda m: (m.block, m.start, m.end))


def relabel_signature_images(blocks: List[Block]) -> List[Block]:
    """[IMAGE] devient [SIGNATURE] dans le premier bloc contenant « Fait à » ou « Lu et approuvé » et après."""
    out, signed = [], False
    for b in blocks:
        signed = signed or bool(SIGNED_RX.search(b.text))
        out.append(replace(b, text=b.text.replace("[IMAGE]", "[SIGNATURE]")) if signed else b)
    return out
