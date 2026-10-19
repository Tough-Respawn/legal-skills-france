"""Publication du texte masqué validé et vérification de provenance d'un fichier.

Publier est le seul moment où un fichier masqué quitte le coffre. Rien n'est affiché ici.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from .coffre import Vault, atomic_write
from .rendu import MARKER_RE


def publish(vault: Vault, cid: str, text: str, destination: Path) -> Path:
    """Écrit `destination/contrat-<id>.masque.md`, inscrit son empreinte au registre et dans l'état.

    Refuse (`ValueError`) un texte dont la première ligne n'est pas le marqueur `valide_humain` de
    ce contrat : publier autre chose est une erreur de programmation.
    """
    m = MARKER_RE.match(text.split("\n", 1)[0])
    if not m or m.group("statut") != "valide_humain" or m.group("id") != cid:
        raise ValueError("Publication refusée : la première ligne n'est pas le marqueur valide_humain de ce contrat.")
    data = text.encode("utf-8")
    sha = hashlib.sha256(data).hexdigest()
    date = m.group("date")
    target = Path(destination) / ("contrat-%s.masque.md" % cid)
    # Registre d'abord : un fichier publié a toujours son empreinte inscrite.
    vault.register_published(sha, cid, date)
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
