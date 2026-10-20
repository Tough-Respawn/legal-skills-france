"""Détection par règles : formes structurées (identifiants, contacts, adresses).

On masque sur la forme ; la clé de contrôle sert seulement à typer (SIREN,
SIRET, NIR, IBAN), jamais à exempter : une forme sans clé valide reste masquée
sous NUMERO. Les chevauchements entre règles ne sont pas résolus ici.
"""
from __future__ import annotations

import re
from typing import Callable, List, Optional, Tuple

from ..modele import Block, Mention

SP = r"[ \u00a0\u202f]"
W = r"[A-ZÀ-Ü][\w'-]*"
NAME = W + r"(?: (?:(?:sur|en|de|la|le|sous|lès) )?" + W + r"){0,3}"
MONTHS = "janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre"
BIRTH = r"(?i:n[ée]e? le)\s+(\d{1,2}(?i:er)?\s+(?i:%s)\s+\d{4}|\d{2}/\d{2}/\d{4})" % MONTHS   # capitales comprises ; \s : saut de ligne d'un PDF
# Lieu de naissance : un mot, composé par trait d'union ou apostrophe (Aix-en-Provence, L'Isle-Adam), après
# « Saint » ou un article au plus, suivi au plus de « sur|sous|lès|en » et d'un mot (Boulogne sur Mer) ;
# « À LYON DE NATIONALITÉ FRANÇAISE » donne LYON.
BIRTH_PLACE = r"(?:(?:La|Le|Les|LA|LE|LES) |(?i:saint|sainte) )?" + W + r"(?: (?i:sur|sous|lès|en) " + W + ")?"
NOT_AMOUNT = r"(?!\s?(?:€|euros?|EUR|%))"
STREET_WORD = (r"(?i:rue|avenue|av\.|boulevard|bd|place|chemin|allée|impasse|route|quai|cours|square|"
               r"passage|voie)(?=\W)")
# Queue de rue : 60 caractères max, arrêt avant , ; saut de ligne ou un mot de liaison.
STREET_TAIL = (r"[^,\n;]{3}(?:(?!" + SP + r"(?:est|sera|sont|et|ou|pour|qui|dont|à|au|aux|en)\b)[^,\n;]){0,57}")
POSTCODE = r"(?:,? ?\d{5} ?" + NAME + ")?"
STREET = (r"(?<!\d)\d{1,4}(?: ?(?i:bis|ter|quater))?,? " + STREET_WORD + STREET_TAIL + POSTCODE)
STREET_CTX = (r"(?i:\b(?:demeurant|domicilié(?:e)?|sis(?:e)?|situé(?:e)?|siège|adresse|habitant))[^\n.;]{0,25}?"
              r"\b(" + STREET_WORD + STREET_TAIL + POSTCODE + ")")
NUM_PREFIX = r"(?:(?:n°|numéro|no)\.? ?)?"
TRIGGERS = r"(?i:contrat|dossier|client|r[ée]f[ée]rence|r[ée]f\.|police|compte|adh[ée]rent|lot|parcelle)"
# Nom de bâtiment, résidence, lieu-dit : ni forme sociale ni préposition en capitales (« GRAND EST BÂTIMENT SAS »,
# « BÂTIMENT POUR TROIS MOIS »).
_NOT_IN_PLACE = (r"(?!(?:SAS|SASU|SARL|EURL|SA|SCI|SNC|À|AU|AUX|EN|PAR|POUR|SUR|SOUS|DANS|AVEC|SANS|CHEZ|DEVANT"
                 r"|CONTRE|ENTRE|ENVERS|SELON|VERS|APRÈS|AVANT|DONT|QUI|QUE|ET|OU)(?![\w'-]))")
PLACE_NAME = _NOT_IN_PLACE + W + r"(?: (?:(?:sur|en|de|la|le|sous|lès) )?" + _NOT_IN_PLACE + W + r"){0,3}"


def _luhn_ok(digits: str) -> bool:
    d = re.sub(r"\D", "", digits)
    tot = sum(sum(divmod(int(c) * (2 if i % 2 else 1), 10)) for i, c in enumerate(reversed(d)))
    return tot % 10 == 0


def _iban_ok(text: str) -> bool:
    s = re.sub(r"\s", "", text).upper()
    return int("".join(str(int(c, 36)) for c in s[4:] + s[:4])) % 97 == 1


def _nir_ok(text: str) -> bool:
    s = re.sub(r"\s", "", text).upper().replace("2A", "19").replace("2B", "18")
    return len(s) == 15 and s.isdigit() and 97 - int(s[:13]) % 97 == int(s[13:])


def _typed(kind: str, ok: Callable[[str], bool]) -> Callable[[str], str]:
    return lambda t: kind if ok(t) else "NUMERO"


Rule = Tuple[str, "re.Pattern[str]", int, Optional[Callable[[str], str]]]


def _r(kind: str, pattern: str, group: int = 0, typer: Optional[Callable[[str], str]] = None) -> Rule:
    return (kind, re.compile(pattern), group, typer)


# Un seul séparateur : espace, insécable ou saut de ligne (le CRLF de l'OCR est normalisé à la source), jamais une
# tabulation : un IBAN ou un SIREN coupé par une ligne reste reconnu, une colonne de montants « 850\t120\t970 » non.
S = r"(?:" + SP + r"|\n)?"
_MAX_BREAKS = 1   # au-delà, une suite de nombres typée (SIREN, SIRET, NIR, IBAN) est une colonne, pas un numéro
RULES: List[Rule] = [
    _r("TVA", r"\bFR" + S + r"\d{2}" + S + r"\d{3}" + S + r"\d{3}" + S + r"\d{3}\b"),
    _r("IBAN", r"(?i:\bFR\d{2}(?:" + S + r"[A-Z0-9]{4}){5}" + S + r"[A-Z0-9]{3}\b)", 0, _typed("IBAN", _iban_ok)),
    _r("IBAN", r"\b[A-Z]{2}\d{2}(?:" + S + r"[A-Z0-9]{4}){3,7}" + S + r"[A-Z0-9]{1,4}\b", 0, _typed("IBAN", _iban_ok)),
    _r("BIC", r"(?i:BIC|SWIFT)\W{0,10}([A-Z]{6}[A-Z0-9]{2}(?:[A-Z0-9]{3})?)\b", 1),
    _r("NIR", r"\b[12]" + S + r"\d{2}" + S + r"(?:0[1-9]|1[0-2]|2[0-9]|[3-9]\d)" + S + r"(?:\d{2}|2A|2B)" + S
       + r"\d{3}" + S + r"\d{3}" + S + r"\d{2}\b", 0, _typed("NIR", _nir_ok)),
    _r("SIRET", r"(?<!\d)\d{3}" + S + r"\d{3}" + S + r"\d{3}" + S + r"\d{5}(?!\d)" + NOT_AMOUNT,
       0, _typed("SIRET", _luhn_ok)),
    _r("SIREN", r"(?<!\d)\d{3}" + S + r"\d{3}" + S + r"\d{3}(?!\d)" + NOT_AMOUNT, 0, _typed("SIREN", _luhn_ok)),
    _r("RCS", r"RCS (?:(?i:de) |(?i:d)['’])?" + NAME + S + r"\d{3}" + S + r"\d{3}" + S + r"\d{3}"),
    _r("CAPITAL", r"(?i:capital (?:social )?de) (\d[\d \u00a0\u202f.]* ?(?:€|(?i:euros?|eur)\b))", 1),
    _r("EMAIL", r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}"),
    _r("URL", r"https?://\S*[^\s.,;:)\]]"),
    _r("URL", r"(?<![/@\w.])www\.\S*[^\s.,;:)\]]"),
    _r("TELEPHONE", r"(?<![\w+])(?:\+33|0033)" + S + r"[1-9](?:[ \u00a0\u202f.-]?\d{2}){4}(?!\d)"),
    _r("TELEPHONE", r"(?<![\w+])0[1-9](?:[ \u00a0\u202f.-]?\d{2}){4}(?!\d)"),
    _r("TELEPHONE", r"(?<![\w+])\+\d{1,3}(?:" + S + r"\d){8,12}(?!\d)"),
    _r("ADRESSE", STREET),
    _r("ADRESSE", STREET_CTX, 1),
    _r("ADRESSE", r"\bBP" + S + r"\d{1,5}\b"),
    _r("ADRESSE", r"\b(?i:appartement|appt\.?|bât(?:iment)?\.?|étage|esc(?:alier)?\.?)" + SP + r"(?=[A-Z]\b|\d)\w{1,6}"),
    _r("ADRESSE", r"(?i:lieu-dit|résidence|bâtiment) (" + PLACE_NAME + ")", 1),
    _r("COMMUNE", r"(?<!\d)\d{5} (" + NAME + ")", 1),
    _r("DATE_NAISSANCE", BIRTH, 1),
    _r("LIEU", BIRTH + r" (?i:à) (" + BIRTH_PLACE + ")", 2),
    _r("IMMATRICULATION", r"\b[A-Z]{2}-\d{3}-[A-Z]{2}\b"),
    _r("IMMATRICULATION", r"\b\d{1,4} (?!(?:EUR|USD|UE|TTC|HT)\b)[A-Z]{2,3} \d{2,3}\b"),
    _r("PIECE_IDENTITE", r"(?i:passeport|CNI|carte (?:nationale )?d'identité|titre de séjour|permis(?: de conduire)?)"
       r" ?" + NUM_PREFIX + r"((?=[A-Z0-9]*\d)[A-Z0-9]{6,12})\b", 1),
    _r("NUMERO", r"(?i:cadastr[ée]e? section|section cadastrale) ([A-Z]{1,2}(?: ?" + NUM_PREFIX + r"\d+)?)", 1),
    # Un numéro contient au moins un chiffre : « CONTRAT DE LOCATION », « LE CLIENT PAIE » ne masquent rien.
    _r("NUMERO", r"\b" + TRIGGERS + " " + NUM_PREFIX + r"((?=[A-Z0-9\-/_.]*\d)[A-Z0-9][A-Z0-9\-/_.]*[A-Z0-9])", 1),
]

# Les règles à clé numérique ignorent les références d'articles (art. L. 1234-5).
ARTICLE_BEFORE = re.compile(r"art(?:icles?)?\.? ?[LRD]?\.? ?$", re.I)


def find(blocks: List[Block]) -> List[Mention]:
    """Retourne toutes les mentions par règles (source « regle »), sans résoudre les chevauchements."""
    out: List[Mention] = []
    for i, block in enumerate(blocks):
        text = block.text
        seen = set()
        addresses = []
        for kind, rx, group, typer in RULES:
            for m in rx.finditer(text):
                s, e = m.span(group)
                if s < 0 or (s, e) in seen:
                    continue
                if typer and (ARTICLE_BEFORE.search(text[:s]) or m.group(group).count("\n") > _MAX_BREAKS):
                    continue   # référence d'article, ou colonne de montants « 850\n120\n970 »
                if kind == "COMMUNE" and any(a <= s and e <= b for a, b in addresses):
                    continue
                seen.add((s, e))
                if kind == "ADRESSE":
                    addresses.append((s, e))
                out.append(Mention(i, s, e, typer(m.group(group)) if typer else kind, "regle"))
    return out
