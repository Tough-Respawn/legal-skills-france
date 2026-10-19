"""Extraction du texte : aiguillage par extension."""
from __future__ import annotations

from pathlib import Path

from ..modele import Extracted


class UnsupportedFormat(Exception):
    """Extension non prise en charge."""


class Unreadable(Exception):
    """Fichier corrompu ou illisible."""


class MissingDependency(Exception):
    """Dépendance optionnelle absente."""


def _docx(path: Path, workdir: Path) -> Extracted:
    from . import docx
    return docx.extract_docx(path)


# Les tâches 4 et 5 ajoutent .pdf et les images ici.
_DISPATCH = {".docx": _docx}


def extract(path: Path, workdir: Path) -> Extracted:
    """Extrait blocs, métadonnées et constats ; workdir sert aux images temporaires de l'OCR."""
    handler = _DISPATCH.get(Path(path).suffix.lower())
    if handler is None:
        raise UnsupportedFormat("Format non pris en charge : %s" % Path(path).suffix)
    return handler(Path(path), Path(workdir))
