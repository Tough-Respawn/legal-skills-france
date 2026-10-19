"""Entités et placeholders : chevauchements, regroupement, propagation, ambiguïtés, décisions.

1. Chevauchements, bloc par bloc : la mention la plus longue l'emporte ; à égalité,
   regle > structure > ner > propagation. Un gagnant sans partie (nom de la NER) reprend le
   type, le rôle et la partie de la mention de comparution qu'il contient ; s'il en couvre deux,
   il est écarté et les parties restent distinctes. Avant tout, un nom en capitales de la structure
   ou de la NER s'arrête avant son premier verbe courant (noms.CAPS_VERBS : « AWA SIGNE » → « AWA »).
2. Regroupement : une partie de la comparution (même `party`) forme une entité, chacun de ses
   représentants une autre (« née X » rejoint le représentant qui précède). Les identifiants
   (adresse, commune, e-mail…) des règles et de la structure sont groupés par forme normalisée ;
   une commune et un lieu de naissance de même nom font une seule entité COMMUNE.
   Les autres noms, du plus long au plus court, rejoignent l'entité unique qui porte leur forme
   (forme complète, ou nom seul pour une mention réduite au nom) ; portée par plusieurs entités
   (homonymes, époux), la forme rend la mention ambiguë ; portée par aucune, un nom en capitales
   sur-capturé (« N'DIAYE LE LOGEMENT ») est rogné à la plus longue forme connue qui l'ouvre et
   rattaché sans en tirer de formes, si cette forme fait deux mots ou si le mot qui la suit est un
   verbe courant, un mot-outil (noms.FUNCTION_WORDS, liste fixe), un mot connu ou sans majuscule ;
   sinon il crée une entité (« MADAME AWA DUPONT »), dont seules les formes du début, avant le
   premier verbe, mot-outil hors liaison de nom ou mot connu, sont inscrites (propagation.head),
   jamais un verbe, un mot-outil ou un mot du vocabulaire seul. Un nom de la structure ne rejoint
   qu'une entité de même type (« M. Dupont » jamais « SCI Dupont ») ; un nom de la NER, dont le
   type est peu fiable, rejoint toute entité de même forme (son type cède alors).
3. Propagation : chaque forme d'entité (propagation.forms) est cherchée dans tous les blocs, sans
   casse ni accents, bornes de mot comprises (une élision ne borne pas : « d'Élodie »), hors des
   étendues déjà prises, la plus longue d'abord ; un nom de la NER contenu dans l'occurrence ou
   qui la chevauche lui cède la place ; le reste d'un chevauchement n'est gardé que s'il fait deux
   mots capitalisés hors vocabulaire ; l'entité touchée recalcule alors ses formes sur ce qui lui
   reste (vidée, elle n'en a plus et n'est candidate d'aucune ambiguïté). Une forme d'un
   seul mot n'est prise que si l'occurrence porte une majuscule (« Claire », pas « claire »).
4. Placeholders : `[<ROLE>_<n>]` si un rôle est défini, sinon `[<TYPE>_<n>]`, numérotés par
   étiquette dans l'ordre de première apparition ; les décisions ne changent jamais ces numéros.
   Une ambiguïté non tranchée `M<n>` se masque en `[AMBIGU_<n>]`.
5. Décisions : `resolve` rattache une occurrence (clé `occurrence_key`) à un placeholder ou à
   une nouvelle entité (« nouveau ») ; `unmask` retire des entités ; une commune « garder » (clé :
   texte.norm de sa forme canonique) est retirée ; `mask_more` crée une entité AUTRE par texte, sur
   chaque occurrence encore libre, sans casse ni accents, bornes de mot comprises.
"""
from __future__ import annotations

import re
from dataclasses import replace
from typing import Dict, List, Optional, Sequence, Tuple

from . import texte
from .detection.noms import before_verb, caps_verb, function_word, known
from .detection.structure import load_vocab
from .modele import Ambiguity, Block, Decisions, Entity, Mention
from .propagation import WORD_RX, Key, folded, forms, head, name_part, name_words, pattern, span, strip_civility

PRIORITY = {"regle": 0, "structure": 1, "ner": 2, "propagation": 3}
NAMED = ("PERSONNE", "SOCIETE")
ALIAS_BEFORE_RX = re.compile(r"(?i:née|nee|épouse|epouse|veuve|divorcée|divorcee|dite?)[   ]+$")
_ALPHA_RX = re.compile(r"[^\W\d_]+(?:['-][^\W\d_]+)*")
NEW = "nouveau"


def occurrence_key(block: Block, start: int, end: int) -> Key:
    """Clé d'une occurrence : (location, texte normalisé, rang de ce texte dans le bloc, à partir de 1)."""
    form = texte.norm(block.text[start:end])
    if not form:
        return block.location, form, 1
    text, pos = folded(block.text)
    return block.location, form, 1 + sum(1 for m in pattern(form).finditer(text) if pos[m.start()] < start)


def ambiguity_placeholder(a: Ambiguity) -> str:
    """Placeholder provisoire d'une ambiguïté M<n> : [AMBIGU_<n>]."""
    return "[AMBIGU_%s]" % a.id[1:]


def _overlaps(mentions: Sequence[Mention]) -> List[Mention]:
    """Mentions sans chevauchement, dans l'ordre du document. Un nom sans partie qui couvre deux mentions
    de comparution (« M. Jean Kerbrat et Mme Marie Kerbrat » lu d'un bloc par la NER) est écarté."""
    # ponytail: un perdant qui déborde du gagnant laisse son reste visible ; la seconde passe (tâche 10) le relit
    parties = [m for m in mentions if m.party is not None]
    mentions = [m for m in mentions if m.party is not None or m.kind not in NAMED or sum(
        1 for p in parties if p.block == m.block and m.start <= p.start and p.end <= m.end) < 2]
    kept: Dict[int, List[Mention]] = {}
    for m in sorted(mentions, key=lambda m: (m.start - m.end, PRIORITY.get(m.source, 9), m.block, m.start)):
        lst = kept.setdefault(m.block, [])
        hit = next((i for i, k in enumerate(lst) if k.start < m.end and m.start < k.end), None)
        if hit is None:
            lst.append(m)
            continue
        win = lst[hit]
        if (win.party is None and m.party is not None and win.kind in NAMED
                and win.start <= m.start and m.end <= win.end):
            lst[hit] = replace(win, kind=m.kind, role=m.role, party=m.party)
    return sorted((m for lst in kept.values() for m in lst), key=lambda m: (m.block, m.start))


class _Builder:
    def __init__(self, blocks: List[Block]) -> None:
        self.blocks = blocks
        self.vocab = load_vocab()
        self.ents: List[Entity] = []
        self.owners: Dict[str, List[int]] = {}    # forme normalisée → entités qui la portent
        self.pending: List[Tuple[Mention, List[int], str]] = []   # mention, propriétaires, forme en cause
        self.taken: Dict[int, List[Mention]] = {}   # mentions déjà posées, par bloc
        self.sources: Dict[Mention, str] = {}       # texte dont chaque mention a donné ses formes

    def text(self, m: Mention) -> str:
        return self.blocks[m.block].text[m.start:m.end]

    def take(self, m: Mention) -> None:
        self.taken.setdefault(m.block, []).append(m)

    def clash(self, bi: int, s: int, e: int) -> List[Mention]:
        return [k for k in self.taken.get(bi, ()) if k.start < e and s < k.end]

    def refresh(self, i: int) -> None:
        """Formes de l'entité recalculées sur ses mentions restantes (vidée : aucune forme)."""
        for lst in self.owners.values():
            if i in lst:
                lst.remove(i)
        for m in self.ents[i].mentions:
            if m in self.sources:
                self.register(i, self.sources[m])

    def drop(self, k: Mention, new: Optional[Mention] = None) -> None:
        """Retire une mention posée, ou la remplace par new ; l'entité touchée recalcule ses formes,
        vidée elle n'est pas numérotée."""
        self.taken[k.block].remove(k)
        source = self.sources.pop(k, None)
        if new:
            self.take(new)
            if source is not None:
                self.sources[new] = self.text(new)
        for i, e in enumerate(self.ents):
            if k in e.mentions:
                e.mentions[e.mentions.index(k):e.mentions.index(k) + 1] = [new] if new else []
                self.refresh(i)
        self.pending = [(new, p[1], p[2]) if p[0] == k else p for p in self.pending if p[0] != k or new]

    def cut(self, k: Mention, s: int, e: int) -> None:
        """Nom de la NER chevauché par une forme connue en [s, e) : son reste n'est gardé que s'il fait au
        moins deux mots capitalisés hors vocabulaire (« Jean Dupont »), sinon il est abandonné."""
        # ponytail: reste d'un mot abandonné (« SIGNENT » : sous-masquage possible d'un vrai nom), reste de deux mots
        # gardé (sur-masquage possible) ; la seconde passe (tâche 10) relit le texte laissé en clair
        rs, rend = (k.start, s) if k.start < s else (e, k.end)
        words = list(WORD_RX.finditer(self.blocks[k.block].text, rs, rend)) if rs < rend else []
        keep = len(words) >= 2 and all(w.group()[0].isupper() and not known(w.group(), self.vocab) for w in words)
        self.drop(k, replace(k, start=words[0].start(), end=words[-1].end()) if keep else None)

    def compatible(self, m: Mention, own: List[int]) -> List[int]:
        """Entités que la mention peut rejoindre : même type, ou tout type pour la NER (type peu fiable)."""
        return [i for i in own if m.source == "ner" or self.ents[i].kind == m.kind]

    def prefix(self, m: Mention, name: str) -> Optional[Tuple[Mention, List[int], str]]:
        """Plus longue forme connue qui ouvre un nom en capitales sur-capturé (« N'DIAYE LE LOGEMENT ») :
        mention rognée à cette forme, entités qui la portent, forme. Une forme d'un seul mot ne rogne que
        si le mot suivant est un verbe courant, un mot-outil, un mot du vocabulaire ou sans majuscule ;
        un autre mot capitalisé est un nom (« AWA DUPONT » n'est pas Awa N'Diaye : nouvelle entité)."""
        text, pos = folded(name)
        base = m.end - len(name)
        for f in sorted((f for f in self.owners if text.startswith(f + " ")), key=len, reverse=True):
            own = self.compatible(m, self.owners[f])
            if not own:
                continue
            end = span(name, pos, 0, len(f))[1]
            nxt = WORD_RX.search(name, end)
            word = nxt.group() if nxt else ""
            if (" " in f or not word or caps_verb(word) or function_word(word) or known(word, self.vocab)
                    or word[0].islower()):
                return replace(m, end=base + end), own, f
            return None
        return None

    def new(self, kind: str, role: Optional[str] = None) -> int:
        self.ents.append(Entity(kind, role, "", "", []))
        return len(self.ents) - 1

    def add(self, i: int, m: Mention, text: Optional[str] = None) -> None:
        """Rattache la mention et inscrit les formes de son texte (ou de text, s'il est donné)."""
        self.ents[i].mentions.append(m)
        self.sources[m] = text or self.text(m)
        self.register(i, self.sources[m])

    def register(self, i: int, text: str) -> None:
        for f in forms(self.ents[i].kind, text, self.vocab):
            lst = self.owners.setdefault(f, [])
            if i not in lst:
                lst.append(i)

    def group(self, kept: List[Mention]) -> None:
        """Parties et représentants, identifiants, puis les autres noms du plus long au plus court."""
        party: Dict[int, int] = {}
        last_rep: Dict[int, int] = {}
        by_form: Dict[str, int] = {}
        loose = []
        for m in kept:
            self.take(m)
            if m.party is not None and m.kind in NAMED:
                if m.role != "REPRESENTANT":
                    if m.party not in party:
                        party[m.party] = self.new(m.kind, m.role)
                    i = party[m.party]
                    self.ents[i].role = self.ents[i].role or m.role
                elif m.party in last_rep and ALIAS_BEFORE_RX.search(self.blocks[m.block].text, 0, m.start):
                    i = last_rep[m.party]
                else:
                    i = last_rep[m.party] = self.new(m.kind, "REPRESENTANT")
                self.add(i, m)
            elif m.kind not in NAMED and m.source != "ner":
                f = texte.norm(self.text(m))
                if f not in by_form:
                    by_form[f] = self.new(m.kind)
                elif m.kind == "COMMUNE" and self.ents[by_form[f]].kind == "LIEU":
                    self.ents[by_form[f]].kind = "COMMUNE"   # la commune reste arbitrable (garder)
                self.add(by_form[f], m)
            else:
                loose.append(m)
        loose.sort(key=lambda m: (-len(name_part(m.kind, self.text(m))), PRIORITY.get(m.source, 9), m.block, m.start))
        for m in loose:
            name = name_part(m.kind, self.text(m))
            words = name_words(name)
            form = texte.norm(name)
            if not self.owners.get(form) and len(words) == 1:
                form = texte.norm(words[0])   # « M. de La Fontaine »
            own = self.compatible(m, self.owners.get(form, []))
            cut = self.prefix(m, name) if not own and name.isupper() and len(words) > 1 else None
            if cut:   # rattachée sans en tirer de formes : « LOGEMENT » ne devient pas un nom
                self.taken[m.block].remove(m)
                m, own, form = cut
                self.take(m)
                if len(own) == 1:
                    self.ents[own[0]].mentions.append(m)
                    continue
            if len(own) > 1:
                self.pending.append((m, own, form))
            elif own:
                self.add(own[0], m)
            else:
                self.add(self.new(m.kind), m, head(name, self.vocab) if name.isupper() else None)

    def propagate(self) -> None:
        """Formes cherchées partout, la plus longue d'abord ; une forme alphabétique d'un seul mot
        doit porter une majuscule (« Claire », pas « claire »)."""
        folds = [folded(b.text) for b in self.blocks]
        for form in sorted(self.owners, key=lambda f: (-len(f), f)):
            own = self.owners[form]
            single = " " not in form and _ALPHA_RX.fullmatch(form) is not None
            for bi, (text, pos) in enumerate(folds):
                for hit in pattern(form).finditer(text) if form in text else ():
                    s, e = span(self.blocks[bi].text, pos, hit.start(), hit.end())
                    if not own:
                        break   # propriétaire vidé par drop
                    if single and self.blocks[bi].text[s:e].islower():
                        continue
                    clash = self.clash(bi, s, e)
                    if any(k.source != "ner" or (k.start <= s and e <= k.end) for k in clash):
                        continue   # déjà pris ; un nom de la NER contenu ou chevauchant cède à la forme connue
                    for k in clash:
                        self.cut(k, s, e)
                    first = self.ents[own[0]]
                    m = Mention(bi, s, e, first.kind, "propagation")
                    if len(own) == 1:
                        m = replace(m, role=first.role, party=_party(first))
                        first.mentions.append(m)
                    else:
                        self.pending.append((m, list(own), form))
                    self.take(m)

    def number(self) -> Dict[str, int]:
        """Placeholders par ordre de première apparition ; renvoie les compteurs par étiquette."""
        counters: Dict[str, int] = {}
        for e in sorted((e for e in self.ents if e.mentions), key=_first):
            self.label(e, counters)
        return counters

    def label(self, e: Entity, counters: Dict[str, int]) -> None:
        tag = e.role or e.kind
        counters[tag] = counters.get(tag, 0) + 1
        e.placeholder = "[%s_%d]" % (tag, counters[tag])

    def decide(self, decisions: Decisions, counters: Dict[str, int]) -> List[Ambiguity]:
        """Résolutions, retraits (unmask, communes gardées), puis ajouts libres (mask_more)."""
        by_ph = {e.placeholder: e for e in self.ents}
        ambs: List[Ambiguity] = []
        for m, own, form in sorted(self.pending, key=lambda p: (p[0].block, p[0].start)):
            live = [self.ents[i].placeholder for i in own if i in self.owners.get(form, ())]   # formes à jour
            target = live[0] if len(live) == 1 else decisions.resolve.get(
                occurrence_key(self.blocks[m.block], m.start, m.end))
            if target == NEW:
                e = Entity(m.kind, None, "", "", [])
                self.label(e, counters)
                self.ents.append(e)
                by_ph[e.placeholder] = e
                target = e.placeholder
            if target in by_ph:
                by_ph[target].mentions.append(m)
            else:
                ambs.append(Ambiguity("M%d" % (len(ambs) + 1), m, tuple(live)))
        self.ents = [e for e in self.ents if e.mentions and e.placeholder not in decisions.unmask and not (
            e.kind == "COMMUNE" and decisions.communes.get(texte.norm(self.canonical(e))) == "garder")]
        self.taken = {}
        for m in [m for e in self.ents for m in e.mentions] + [a.mention for a in ambs]:
            self.take(m)
        folds = [folded(b.text) for b in self.blocks]
        extra = []
        for value in sorted(decisions.mask_more):
            e, form = Entity("AUTRE", None, "", "", []), texte.norm(value)
            for bi, (text, pos) in enumerate(folds if form else ()):
                for hit in pattern(form).finditer(text) if form in text else ():
                    s, end = span(self.blocks[bi].text, pos, hit.start(), hit.end())
                    if not self.clash(bi, s, end):
                        m = Mention(bi, s, end, "AUTRE", "decision")
                        self.take(m)
                        e.mentions.append(m)
            if e.mentions:
                extra.append(e)
        for e in sorted(extra, key=_first):
            self.label(e, counters)
        self.ents += extra
        return ambs

    def canonical(self, e: Entity) -> str:
        texts = [self.text(m) for m in e.mentions]
        return max((strip_civility(t) for t in texts) if e.kind == "PERSONNE" else texts, key=len)


def _first(e: Entity) -> Tuple[int, int]:
    return min((m.block, m.start) for m in e.mentions)


def _party(e: Entity) -> Optional[int]:
    return next((m.party for m in e.mentions if m.party is not None), None)


def build(blocks: List[Block], mentions: List[Mention], decisions: Decisions) -> Tuple[List[Entity], List[Ambiguity]]:
    """Entités (placeholder, forme canonique, mentions) et ambiguïtés à arbitrer, dans l'ordre du document."""
    b = _Builder(blocks)
    # En capitales, un nom de la structure ou de la NER s'arrête avant son premier verbe (« AWA SIGNE »).
    mentions = [replace(m, end=before_verb(blocks[m.block].text, m.start, m.end))
                if m.kind in NAMED and m.source in ("ner", "structure") else m for m in mentions]
    b.group(_overlaps([m for m in mentions if m.end > m.start]))
    b.propagate()
    ambs = b.decide(decisions, b.number())
    for e in b.ents:
        e.mentions.sort(key=lambda m: (m.block, m.start))
        e.canonical = b.canonical(e)
    return sorted(b.ents, key=_first), ambs
