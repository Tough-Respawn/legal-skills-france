"""Publication du texte masqué validé et vérification de provenance d'un fichier.

Publier est le seul moment où un fichier masqué quitte le coffre. Rien n'est affiché ici.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .coffre import Vault, atomic_write
from .rendu import MARKER_RE, body_hash


def publish(vault: Vault, cid: str, text: str, destination: Path) -> Path:
    """Écrit `destination/contrat-<id>.masque.md`, fige la table de correspondance du passage qui a écrit ce
    texte (`coffre/<id>/publications/<passage>.json`, jamais réécrite), inscrit son empreinte au registre et
    dans l'état.

    Refuse (`ValueError`), avant toute écriture, un identifiant qui n'est pas un id neutre connu du
    coffre (6 caractères hexadécimaux : ni `NUL`, ni `CON`, ni `../x`), un texte dont la première
    ligne n'est pas le marqueur `valide_humain` de ce contrat, dont le champ `corps` manque ou ne
    correspond pas au corps du texte, sans champ `passage`, ou dont la table figée de ce passage existe
    déjà avec un autre contenu : c'est une erreur de programmation. Deux passages au corps identique
    (seules des valeurs masquées changent) ont chacun leur table.
    """
    if not re.fullmatch(r"[0-9a-f]{6}", cid) or cid not in vault.known_ids():
        raise ValueError("Publication refusée : identifiant de contrat invalide ou inconnu du coffre.")
    m = MARKER_RE.match(text.split("\n", 1)[0])
    if not m or m.group("statut") != "valide_humain" or m.group("id") != cid:
        raise ValueError("Publication refusée : la première ligne n'est pas le marqueur valide_humain de ce contrat.")
    data = text.encode("utf-8")
    corps, passage = m.group("corps"), m.group("passage")
    if corps != body_hash(data)[:16] or not passage:
        raise ValueError("Publication refusée : le marqueur ne porte pas l'empreinte du corps de ce texte ou "
                         "l'identifiant de son passage.")
    sha = hashlib.sha256(data).hexdigest()
    date = m.group("date")
    target = Path(destination) / ("contrat-%s.masque.md" % cid)
    folder = vault.contract_dir(cid)
    table = (folder / "correspondance.json").read_bytes()
    snapshot = folder / "publications" / ("%s.json" % passage)
    if snapshot.exists() and snapshot.read_bytes() != table:
        raise ValueError("Publication refusée : la table figée de ce passage existe déjà avec un autre contenu.")
    # Table figée d'abord, puis registre : un fichier publié a toujours sa table et son empreinte inscrite.
    if not snapshot.exists():   # jamais réécrite : même passage, même table
        snapshot.parent.mkdir(mode=0o700, exist_ok=True)
        atomic_write(snapshot, table)
    vault.register_published(sha, cid, date, corps, passage)
    atomic_write(target, data)
    state = vault.read_state(cid)
    state.update({"publie": str(target.resolve()), "sha256": sha, "date": date})
    vault.write_state(cid, state)
    return target


def verify(vault: Vault, file: Path) -> str:
    """`publie` si l'empreinte est au registre ; `modifie` si le marqueur porte un id connu ; sinon `inconnu`."""
    try:
        data = Path(file).read_bytes()
    except OSError:
        return "inconnu"
    if vault.lookup_published(hashlib.sha256(data).hexdigest()) is not None:
        return "publie"
    first = data.split(b"\n", 1)[0].rstrip(b"\r").decode("utf-8", "replace").lstrip("﻿")
    m = MARKER_RE.match(first)
    return "modifie" if m and m.group("id") in vault.known_ids() else "inconnu"
