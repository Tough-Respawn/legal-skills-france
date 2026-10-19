"""Chaîne complète d'un contrat : extraction, inspection, détection, entités, masquage, seconde passe.

Écrit dans `coffre/<id>/` : `masque.md` (version en préparation, marqueur `valide_humain` daté du jour),
`rapport.md` (valeurs réelles, jamais publié), `ajustements.txt` (décisions relues à chaque passage),
`correspondance.json` (placeholder vers valeur, pour la réidentification) et `etat.json`. `etat.json` est
écrit d'abord avec `pending` et `ouverts` à `null` (un passage interrompu ne laisse jamais un état validable),
puis complété à la fin : `pending` (lignes `?` ou placeholder inconnu), `ouverts` (alertes et ambiguïtés
encore ouvertes), `sha_masque` (corps de `masque.md` après le marqueur) et `sha_ajustements`. Tout le passage
tourne sous `sortie.quiet()` : rien n'est affiché ici.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import tempfile
from dataclasses import dataclass, replace
from pathlib import Path
from typing import List

from . import ajustements, controle, extraction, inspection, masquage, nonet, rendu, sortie
from .coffre import Vault, atomic_write
from .detection import ner, regles, structure
from .entites import Ranks, ambiguity_placeholder, build
from .modele import Alert, Ambiguity, Block, Decisions, Entity, Extracted, Finding

KNOWN_VALUE = "valeur_connue"


@dataclass
class Result:
    extracted: Extracted
    entities: List[Entity]
    ambiguities: List[Ambiguity]
    alerts: List[Alert]
    masked: List[Block]
    pending: int


def body_hash(data: bytes) -> str:
    """Empreinte du corps de `masque.md`, marqueur (première ligne, redaté à la validation) exclu."""
    return hashlib.sha256(data.split(b"\n", 1)[1] if b"\n" in data else b"").hexdigest()


def run(original: Path, vault: Vault, cid: str) -> Result:
    with sortie.quiet():
        return _run(original, vault, cid)


def _run(original: Path, vault: Vault, cid: str) -> Result:
    folder = vault.contract_dir(cid)
    adj = folder / "ajustements.txt"
    state = vault.read_state(cid)
    state.setdefault("destination", str(Path.cwd().resolve()))
    state.update({"original_name_hidden": True, "pending": None, "ouverts": None})
    vault.write_state(cid, state)
    decisions = ajustements.read(adj) if adj.exists() else Decisions()
    try:
        with tempfile.TemporaryDirectory(dir=str(folder)) as work:
            extracted = extraction.extract(original, Path(work))
    except nonet.NetworkBlocked:
        raise
    except OSError as exc:   # original illisible (droits, verrou) : fichier illisible, pas une erreur interne
        raise extraction.Unreadable("Fichier original illisible (%s)." % type(exc).__name__) from exc
    extracted = inspection.clean(extracted)
    blocks = structure.relabel_signature_images(extracted.blocks)
    findings = list(extracted.findings) + inspection.ai_directed(blocks)
    vocab = structure.load_vocab()
    mentions = regles.find(blocks) + structure.find(blocks, vocab)
    if ner.model_installed():
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
    # Une valeur connue encore visible n'est jamais exemptée (spec 6.6) : « garder » y est ignoré, seule
    # une ligne « masquer » la règle.
    all_alerts = controle.check(masked, entities, replace(decisions, keep=set()), vocab, original=blocks)
    ranks = Ranks(masked)
    keys = {a.id: ranks.key(a.block, a.start, a.end) for a in all_alerts}
    known_keys = {keys[a.id] for a in all_alerts if a.reason == KNOWN_VALUE}
    decisions = replace(decisions, keep=decisions.keep - known_keys)
    alerts = [a for a in all_alerts if keys[a.id] not in decisions.keep]
    ranks = Ranks(blocks)
    resolved = [m for e in entities for m in e.mentions if ranks.key(m.block, m.start, m.end) in decisions.resolve]
    # ponytail: une ambiguïté tranchée est numérotée après les ouvertes (son numéro peut changer d'un passage
    # à l'autre) ; sa clé, elle, ne bouge pas.
    all_ambiguities = ambiguities + [Ambiguity("M%d" % (len(ambiguities) + i), m, ())
                                     for i, m in enumerate(sorted(resolved, key=lambda m: (m.block, m.start)), 1)]

    date = datetime.date.today().isoformat()
    masque = rendu.masked_document(cid, masked, findings, residual, date).encode("utf-8")
    atomic_write(folder / "masque.md", masque)
    atomic_write(folder / "rapport.md",
                 rendu.local_report(cid, extracted, entities, ambiguities, alerts, residual).encode("utf-8"))
    # Une commune gardée n'est plus une entité : sa ligne « C<n> garder » doit survivre à la réécriture.
    communes = [e for e in entities if e.kind == "COMMUNE"] + [Entity("COMMUNE", None, "", k, []) for k in kept]
    ajustements.write(adj, all_alerts, all_ambiguities, communes, decisions, cid=cid, blocks=blocks, masked=masked)
    table = {e.placeholder: e.canonical for e in entities}
    table.update((ambiguity_placeholder(a), blocks[a.mention.block].text[a.mention.start:a.mention.end])
                 for a in ambiguities)
    atomic_write(folder / "correspondance.json", json.dumps(table, ensure_ascii=False, indent=2).encode("utf-8"))
    pending = ajustements.pending(adj, {e.placeholder for e in entities})
    state = vault.read_state(cid)
    state.update({"pending": pending, "ouverts": len(alerts) + len(ambiguities), "date": date,
                  "sha_masque": body_hash(masque),
                  "sha_ajustements": hashlib.sha256(adj.read_bytes()).hexdigest()})
    vault.write_state(cid, state)
    return Result(extracted, entities, ambiguities, alerts, masked, pending)
