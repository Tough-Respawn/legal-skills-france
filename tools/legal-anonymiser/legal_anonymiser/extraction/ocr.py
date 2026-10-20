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
                # selon les versions, la liste sort sur stdout ou sur stderr
                text = (out.stdout + b"\n" + out.stderr).decode("utf-8", "replace")
                ok = _LANG in text.split()
            except (OSError, subprocess.SubprocessError):
                ok = False
        _cache["ok"] = ok
    return _cache["ok"]


def require() -> str:
    """Chemin du binaire, ou MissingDependency avec le message adapté à la cause."""
    binary = _binary()
    if binary is None:
        raise MissingDependency(_HINT)
    if not available():
        raise MissingDependency("La langue fra de Tesseract est introuvable : l'installer, "
                                "puis définir TESSDATA_PREFIX vers son dossier si besoin.")
    return binary


def image_to_text(image: Path) -> str:
    """Texte reconnu dans une image ; la sortie d'erreur n'est jamais relayée."""
    binary = require()
    try:
        done = subprocess.run([binary, str(image), "stdout", "-l", _LANG],
                              capture_output=True, check=True, timeout=_TIMEOUT)
    except (OSError, subprocess.SubprocessError) as exc:
        raise Unreadable("La reconnaissance de texte a échoué.") from exc
    # Tesseract Windows écrit \r\n : normalisé ici, à la source, pour que la détection ne voie que \n.
    return done.stdout.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n").strip()



def page_text(page: Any, workdir: Path) -> str:
    """OCR des images d'une page pypdf ; images temporaires sous workdir/tmp, supprimées."""
    tmp = Path(workdir) / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    folder = Path(tempfile.mkdtemp(dir=str(tmp)))
    try:
        targets = []
        try:
            for i, img in enumerate(page.images):
                pil = img.image
                if pil.mode not in ("L", "RGB"):
                    pil = pil.convert("RGB")
                target = folder / ("%d.png" % i)
                pil.save(str(target))
                targets.append(target)
        except Exception as exc:  # JPX, CCITT, filtres rares : message générique
            raise Unreadable("Image du PDF illisible.") from exc
        parts = [image_to_text(t) for t in targets]
        return "\n".join(p for p in parts if p)
    finally:
        shutil.rmtree(str(folder), ignore_errors=True)
        try:
            tmp.rmdir()  # seulement si vide
        except OSError:
            pass
