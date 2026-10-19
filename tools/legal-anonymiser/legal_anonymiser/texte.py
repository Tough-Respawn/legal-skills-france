"""Normalisation de texte et detection de pieges Unicode."""
import re
import unicodedata
from typing import Dict, Tuple

# Lettres cyrilliques et grecques visuellement latines.
CONFUSABLES: Dict[str, str] = {
    **dict(zip("аеорсухіј", "aeopcyxij")),
    **dict(zip("АВЕКМНОРСТХ", "ABEKMHOPCTX")),
    **dict(zip("ορν", "opv")),
    **dict(zip("ΑΒΕΖΗΙΚΜΝΟΡΤΥΧ", "ABEZHIKMNOPTYX")),
}

_ZERO_WIDTH = re.compile("[​-‍⁠﻿]")
_BIDI = re.compile("[‪-‮⁦-⁩]")
_TABLE = str.maketrans(CONFUSABLES)


def norm(s: str) -> str:
    """Minuscules, sans accents, confusables ramenes au latin, espaces fusionnes."""
    s = unicodedata.normalize("NFKD", s.translate(_TABLE))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.casefold()).strip()


def strip_traps(s: str) -> Tuple[str, int, int]:
    """Retire largeur zero et controles bidi : (texte, nb largeur zero, nb bidi)."""
    s, zw = _ZERO_WIDTH.subn("", s)
    s, bidi = _BIDI.subn("", s)
    return s, zw, bidi


def mixed_script(word: str) -> bool:
    """Vrai si le mot melange lettres latines et cyrilliques/grecques."""
    scripts = {
        unicodedata.name(c, "").split(" ", 1)[0]
        for c in word
        if c.isalpha()
    }
    return "LATIN" in scripts and bool(scripts & {"CYRILLIC", "GREEK"})
