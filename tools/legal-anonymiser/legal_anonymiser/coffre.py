"""Coffre local : texte masqué, table de correspondance, registre et état.

Tout reste sur le poste. Bibliothèque standard uniquement.
"""
from __future__ import annotations

import json
import os
import secrets
import sys
import tempfile
from pathlib import Path
from typing import Optional

_POSIX = sys.platform != "win32"


def _chmod(path: Path, mode: int) -> None:
    # ponytail: sous Windows aucun contrôle d'ACL en v1 (icacls serait un
    # sous-processus interdit); l'isolation repose sur le profil utilisateur.
    if _POSIX:
        os.chmod(path, mode)


def atomic_write(path: Path, data: bytes) -> None:
    """Écrit les octets `data` via un fichier temporaire voisin (droits 0600) puis `os.replace`."""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        _chmod(Path(tmp), 0o600)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def _atomic_write_json(path: Path, data: dict) -> None:
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))


class RegistryCorrupted(Exception):
    """Registre ou état illisible : le fichier est corrompu ou incomplet."""


def _read_json(path: Path, label: str) -> dict:
    try:
        data = json.loads(path.read_text("utf-8"))
    except ValueError:
        raise RegistryCorrupted(
            "Fichier du coffre corrompu : %s. Restaurez-le ou supprimez-le." % label
        ) from None
    if not isinstance(data, dict):
        raise RegistryCorrupted("Fichier du coffre corrompu : %s." % label)
    return data


class Vault:
    """Coffre local : dossier racine, registre des originaux et des publiés."""

    def __init__(self, root: Optional[Path] = None) -> None:
        if root is None:
            env = os.environ.get("LEGAL_FRANCE_COFFRE")
            root = Path(env) if env else Path.home() / ".legal-france" / "coffre"
        self.root = Path(root).resolve()

    @property
    def _registry_path(self) -> Path:
        return self.root / "registre.json"

    def ensure(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        _chmod(self.root, 0o700)

    def _load(self) -> dict:
        try:
            reg = _read_json(self._registry_path, "coffre/registre.json")
        except FileNotFoundError:
            return {"version": 1, "originaux": {}, "publies": {}}
        if not isinstance(reg.get("originaux"), dict) or not isinstance(reg.get("publies"), dict):
            raise RegistryCorrupted("Fichier du coffre incomplet : coffre/registre.json.")
        return reg

    def _save(self, reg: dict) -> None:
        self.ensure()
        _atomic_write_json(self._registry_path, reg)

    def contract_dir(self, cid: str) -> Path:
        d = self.root / cid
        d.mkdir(parents=True, exist_ok=True)
        _chmod(d, 0o700)
        return d

    def id_for_original(self, original: Path) -> str:
        """Identifiant neutre stable pour le chemin résolu de l'original."""
        resolved = Path(original).resolve()
        # ponytail: charger/modifier/enregistrer sans verrou, CLI mono-utilisateur;
        # verrou de fichier si plusieurs processus partagent un coffre.
        reg = self._load()
        entry = reg["originaux"].get(str(resolved))
        if entry:
            return entry["id"]
        used = {e["id"] for e in reg["originaux"].values()}
        cid = secrets.token_hex(3)
        while cid in used:
            cid = secrets.token_hex(3)
        reg["originaux"][str(resolved)] = {"id": cid, "nom": resolved.name}
        self._save(reg)
        return cid

    def register_published(self, sha256: str, cid: str, date: str) -> None:
        reg = self._load()
        reg["publies"][sha256] = {"id": cid, "date": date}
        self._save(reg)

    def lookup_published(self, sha256: str) -> Optional[str]:
        entry = self._load()["publies"].get(sha256)
        return entry["id"] if entry else None

    def known_ids(self) -> set:
        return {e["id"] for e in self._load()["originaux"].values()}

    def original_for(self, cid: str) -> Optional[Path]:
        """Chemin de l'original enregistré sous cet identifiant, ou None."""
        return next((Path(p) for p, e in self._load()["originaux"].items() if e["id"] == cid), None)

    def read_state(self, cid: str) -> dict:
        try:
            return _read_json(self.root / cid / "etat.json", "coffre/<id>/etat.json")
        except FileNotFoundError:
            return {}

    def write_state(self, cid: str, state: dict) -> None:
        _atomic_write_json(self.contract_dir(cid) / "etat.json", state)


def original_inside(original: Path, cwd: Path) -> bool:
    """Vrai si le chemin résolu de l'original est dans le dossier courant résolu."""
    try:
        Path(original).resolve().relative_to(Path(cwd).resolve())
        return True
    except ValueError:
        return False
