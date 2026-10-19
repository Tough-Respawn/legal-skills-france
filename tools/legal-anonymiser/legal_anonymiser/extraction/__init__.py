"""Extraction du texte : aiguillage par extension."""
from __future__ import annotations

from pathlib import Path

from ..modele import Block, Extracted, Finding


class UnsupportedFormat(Exception):
    """Extension non prise en charge."""


class Unreadable(Exception):
    """Fichier corrompu ou illisible."""


class MissingDependency(Exception):
    """Dépendance optionnelle absente."""


def _docx(path: Path, workdir: Path) -> Extracted:
    from . import docx
    return docx.extract_docx(path)


def _pdf(path: Path, workdir: Path) -> Extracted:
    from . import pdf
    return pdf.extract_pdf(path, workdir)


def _image(path: Path, workdir: Path) -> Extracted:
    from . import ocr
    ocr.require()
    text = ocr.image_to_text(path)
    if not text:
        return Extracted([], {}, [Finding("attention", "ocr_vide", "image 1")], True)
    return Extracted([Block(text, "image 1", "corps")], {},
                     [Finding("info", "texte_ocr", "image 1", "ocr_local")], True)


_DISPATCH = {".docx": _docx, ".pdf": _pdf, ".jpg": _image, ".jpeg": _image, ".png": _image}
SUPPORTED = frozenset(_DISPATCH)


def supported(path: Path) -> bool:
    """Vrai si l'extension est prise en charge (contrôle avant tout enregistrement au coffre)."""
    return Path(path).suffix.lower() in SUPPORTED


def extract(path: Path, workdir: Path) -> Extracted:
    """Extrait blocs, métadonnées et constats ; workdir sert aux images temporaires de l'OCR."""
    handler = _DISPATCH.get(Path(path).suffix.lower())
    if handler is None:
        raise UnsupportedFormat("Format non pris en charge : %s" % Path(path).suffix)
    return handler(Path(path), Path(workdir))
