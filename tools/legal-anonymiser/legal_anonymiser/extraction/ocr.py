"""OCR local par Tesseract : seul sous-processus autorisé, aucun réseau."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Optional

from . import MissingDependency, Unreadable

_LANG = "fra"
_TIMEOUT = 300
_WINDOWS_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
_HINT = "Tesseract avec la langue fra est requis pour les scans."
_cache: dict = {}


def _binary() -> Optional[str]:
    """Binaire Tesseract : TESSERACT_CMD, PATH, puis l'emplacement Windows habituel."""
    for candidate in (os.environ.get("TESSERACT_CMD"), shutil.which("tesseract"), _WINDOWS_PATH):
        if candidate and Path(candidate).is_file():
            return candidate
    return None


def available() -> bool:
    """Binaire trouvé et langue fra listée (résultat gardé pour le processus)."""
    if "ok" not in _cache:
        ok = False
        binary = _binary()
        if binary:
            try:
                out = subprocess.run([binary, "--list-langs"], capture_output=True, timeout=60)
                ok = _LANG in out.stdout.decode("utf-8", "replace").split()
            except (OSError, subprocess.SubprocessError):
                ok = False
        _cache["ok"] = ok
    return _cache["ok"]


def require() -> None:
    if not available():
        raise MissingDependency(_HINT)


def image_to_text(image: Path) -> str:
    """Texte reconnu dans une image ; la sortie d'erreur n'est jamais relayée."""
    require()
    try:
        done = subprocess.run([_binary(), str(image), "stdout", "-l", _LANG],
                              capture_output=True, check=True, timeout=_TIMEOUT)
    except (OSError, subprocess.SubprocessError) as exc:
        raise Unreadable("La reconnaissance de texte a échoué.") from exc
    return done.stdout.decode("utf-8", "replace").strip()


def page_text(page: Any, workdir: Path) -> str:
    """OCR des images d'une page pypdf ; images temporaires sous workdir/tmp, supprimées."""
    tmp = Path(workdir) / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(dir=str(tmp)))
    try:
        parts = []
        for i, img in enumerate(page.images):
            try:
                pil = img.image
                if pil.mode not in ("L", "RGB"):
                    pil = pil.convert("RGB")
                target = folder / ("%d.png" % i)
                pil.save(str(target))
            except Exception as exc:  # image non décodable (Pillow, filtres rares)
                raise Unreadable("Image du PDF illisible.") from exc
            parts.append(image_to_text(target))
        return "\n".join(p for p in parts if p)
    finally:
        shutil.rmtree(str(folder), ignore_errors=True)
        try:
            tmp.rmdir()  # seulement si vide
        except OSError:
            pass
