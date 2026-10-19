"""Chaîne complète d'un contrat : extraction, inspection, détection, entités, masquage, seconde passe.

Écrit dans `coffre/<id>/` : `masque.md` (version en préparation, marqueur `valide_humain` daté du jour),
`rapport.md` (valeurs réelles, jamais publié), `ajustements.txt` (décisions relues à chaque passage),
`correspondance.json` (placeholder vers valeur, pour la réidentification) et `etat.json`. Rien n'est
affiché ici.
"""
from __future__ import annotations

import datetime
import json
import tempfile
from dataclasses import dataclass, replace
from pathlib import Path
from typing import List

from . import ajustements, controle, extraction, inspection, masquage, rendu, sortie
from .coffre import Vault, atomic_write
from .detection import ner, regles, structure
from .entites import Ranks, ambiguity_placeholder, build
from .modele import Alert, Ambiguity, Block, Decisions, Entity, Extracted, Finding


@dataclass
class Result:
    extracted: Extracted
    entities: List[Entity]
    ambiguities: List[Ambiguity]
    alerts: List[Alert]
    masked: List[Block]
    pending: int


def run(original: Path, vault: Vault, cid: str) -> Result:
    folder = vault.contract_dir(cid)
    adj = folder / "ajustements.txt"
    decisions = ajustements.read(adj) if adj.exists() else Decisions()
    with tempfile.TemporaryDirectory(dir=str(folder)) as work, sortie.quiet():
        extracted = inspection.clean(extraction.extract(original, Path(work)))
    blocks = structure.relabel_signature_images(extracted.blocks)
    findings = list(extracted.findings) + inspection.ai_directed(blocks)
    vocab = structure.load_vocab()
    mentions = regles.find(blocks) + structure.find(blocks, vocab)
    if ner.model_installed():
        with sortie.quiet():
            mentions += ner.find(blocks, vocab)
    else:
        findings.append(Finding("attention", "ner_absente", "document"))
    entities, ambiguities = build(blocks, mentions, decisions)
    extracted = Extracted(blocks, extracted.metadata, findings, extracted.ocr)
    findings += inspection.metadata_findings(extracted, entities)
    masked = masquage.apply(blocks, entities, ambiguities)
    kept = sorted(k for k, choice in decisions.communes.items() if choice == "garder")
    residual = rendu.residual(masked, kept)
    # Les décisions prises doivent survivre à la réécriture du fichier d'ajustements : les alertes gardées
    # sont relues sans exemption (write les marque « garder »), les ambiguïtés tranchées sont retrouvées sur
    # les mentions rattachées. Seules les alertes et ambiguïtés ouvertes vont au rapport et au résultat.
    all_alerts = controle.check(masked, entities, replace(decisions, keep=set()), vocab, original=blocks)
    ranks = Ranks(masked)
    alerts = [a for a in all_alerts if ranks.key(a.block, a.start, a.end) not in decisions.keep]
    ranks = Ranks(blocks)
    resolved = [m for e in entities for m in e.mentions if ranks.key(m.block, m.start, m.end) in decisions.resolve]
    # ponytail: une ambiguïté tranchée est numérotée après les ouvertes (son numéro peut changer d'un passage
    # à l'autre) ; sa clé, elle, ne bouge pas.
    all_ambiguities = ambiguities + [Ambiguity("M%d" % (len(ambiguities) + i), m, ())
                                     for i, m in enumerate(sorted(resolved, key=lambda m: (m.block, m.start)), 1)]

    date = datetime.date.today().isoformat()
    atomic_write(folder / "masque.md", rendu.masked_document(cid, masked, findings, residual, date).encode("utf-8"))
    atomic_write(folder / "rapport.md",
                 rendu.local_report(cid, extracted, entities, ambiguities, alerts, residual).encode("utf-8"))
    # Une commune gardée n'est plus une entité : sa ligne « C<n> garder » doit survivre à la réécriture.
    communes = [e for e in entities if e.kind == "COMMUNE"] + [Entity("COMMUNE", None, "", k, []) for k in kept]
    ajustements.write(adj, all_alerts, all_ambiguities, communes, decisions, cid=cid, blocks=blocks, masked=masked)
    table = {e.placeholder: e.canonical for e in entities}
    table.update((ambiguity_placeholder(a), blocks[a.mention.block].text[a.mention.start:a.mention.end])
                 for a in ambiguities)
    atomic_write(folder / "correspondance.json", json.dumps(table, ensure_ascii=False, indent=2).encode("utf-8"))
    pending = ajustements.pending(adj)
    state = vault.read_state(cid)
    state.setdefault("destination", str(Path.cwd().resolve()))
    state.update({"original_name_hidden": True, "pending": pending, "date": date})
    vault.write_state(cid, state)
    return Result(extracted, entities, ambiguities, alerts, masked, pending)
