"""Extraction et inspection d'un DOCX (bibliothèque standard uniquement)."""
from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

from ..modele import Block, Extracted, Finding
from . import Unreadable

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_MC = "{http://schemas.openxmlformats.org/markup-compatibility/2006}"
_O = "{urn:schemas-microsoft-com:office:office}"
_CORE = {
    "{http://purl.org/dc/elements/1.1/}creator": "auteur",
    "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}lastModifiedBy": "modifie_par",
    "{http://purl.org/dc/terms/}created": "cree",
    "{http://purl.org/dc/terms/}modified": "modifie",
}
_MACRO_TYPE = "application/vnd.ms-word.document.macroEnabled.main+xml"
_EXTERNAL_TYPES = ("hyperlink", "image", "oleObject")
_PHASE_SECTION = {"ins": "insertion", "del": "suppression"}
_PHASE_OF = {_W + "ins": "ins", _W + "moveTo": "ins", _W + "del": "del", _W + "moveFrom": "del"}
_TRANSPARENT = tuple(_W + t for t in ("hyperlink", "smartTag", "sdt", "sdtContent", "customXml",
                                      "dir", "bdo"))
_SKIPPED_NOTES = ("separator", "continuationSeparator")
_MAX_PART = 64 * 1024 * 1024


def _toggle_on(el: Optional[ET.Element]) -> bool:
    """Vrai si une bascule (w:vanish...) est présente et non désactivée."""
    return el is not None and el.get(_W + "val", "true").lower() not in ("0", "false", "off")


def _run_flags(run: ET.Element) -> List[Tuple[str, str]]:
    """Codes de constat d'un run : texte caché, blanc ou minuscule."""
    pr = run.find(_W + "rPr")
    if pr is None:
        return []
    flags = []
    if _toggle_on(pr.find(_W + "vanish")) or _toggle_on(pr.find(_W + "specVanish")):
        flags.append("texte_cache")
    color = pr.find(_W + "color")
    if color is not None and color.get(_W + "val", "").upper() == "FFFFFF":
        flags.append("texte_blanc")
    sz = pr.find(_W + "sz")
    if sz is not None and sz.get(_W + "val", "").isdigit() and int(sz.get(_W + "val")) <= 10:
        flags.append("texte_minuscule")
    return flags


def _run_text(run: ET.Element, marker: str) -> str:
    out = []
    for el in run:
        if el.tag in (_W + "t", _W + "delText"):
            out.append(el.text or "")
        elif el.tag == _W + "tab":
            out.append("\t")
        elif el.tag in (_W + "br", _W + "cr"):
            out.append("\n")
        elif el.tag == _W + "noBreakHyphen":
            out.append("-")
        elif el.tag in (_W + "drawing", _W + "pict") or (
                el.tag == _MC + "AlternateContent"
                and any(d.tag in (_W + "drawing", _W + "pict") for d in el.iter())):
            out.append(marker)
    return "".join(out)


class _Reader:
    def __init__(self) -> None:
        self.blocks: List[Block] = []
        self.findings: List[Finding] = []

    def paragraph(self, p: ET.Element, location: str, section: str, marker: str) -> None:
        body: List[str] = []
        phases: Dict[str, List[str]] = {"ins": [], "del": []}
        seen_phase = set()
        hidden: List[Tuple[str, List[str]]] = []
        has_field = []

        def walk(el: ET.Element, phase: Optional[str]) -> None:
            for child in el:
                if child.tag in _PHASE_OF:
                    walk(child, _PHASE_OF[child.tag])
                elif child.tag == _W + "fldSimple":
                    has_field.append(1)
                    walk(child, phase)
                elif child.tag == _W + "r":
                    run(child, phase)
                elif child.tag in _TRANSPARENT:
                    walk(child, phase)

        def run(r: ET.Element, phase: Optional[str]) -> None:
            if r.find(_W + "instrText") is not None:
                has_field.append(1)
            text = _run_text(r, marker)
            flags = _run_flags(r)
            if flags:
                if text:
                    hidden.append((text, flags))
            elif phase:
                phases[phase].append(text)
                if phase not in seen_phase:
                    seen_phase.add(phase)
                    self.findings.append(Finding("info", "revision_" + _PHASE_SECTION[phase], location))
            else:
                body.append(text)

        walk(p, None)
        if has_field:
            self.findings.append(Finding("info", "champ_automatique", location))
        if "".join(body).strip():
            self.blocks.append(Block("".join(body), location, section))
        for phase in ("ins", "del"):
            if "".join(phases[phase]).strip():
                self.blocks.append(Block("".join(phases[phase]), location, _PHASE_SECTION[phase]))
        for text, flags in hidden:
            self.blocks.append(Block(text, location, "cache"))
            for code in flags:
                self.findings.append(Finding("attention", code, location))


def _read(z: zipfile.ZipFile, name: str) -> bytes:
    # ponytail: plafond fixe par partie, contre les bombes de décompression
    with z.open(name) as f:
        data = f.read(_MAX_PART + 1)
    if len(data) > _MAX_PART:
        raise Unreadable("Partie du DOCX trop volumineuse.")
    return data


def _parse(z: zipfile.ZipFile, name: str) -> ET.Element:
    data = _read(z, name)
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data:  # refuse les entités (bombe XML)
        raise ET.ParseError("DTD interdite")
    return ET.fromstring(data)


def _metadata(z: zipfile.ZipFile) -> Dict[str, str]:
    meta: Dict[str, str] = {}
    names = set(z.namelist())
    if "docProps/core.xml" in names:
        for el in _parse(z, "docProps/core.xml"):
            if el.tag in _CORE and (el.text or "").strip():
                meta[_CORE[el.tag]] = el.text.strip()
    if "docProps/app.xml" in names:
        for el in _parse(z, "docProps/app.xml"):
            if el.tag.endswith("}Company") and (el.text or "").strip():
                meta["societe"] = el.text.strip()
    return meta


def _active_content(z: zipfile.ZipFile, doc: ET.Element) -> List[Finding]:
    names = z.namelist()
    found: List[Finding] = []
    types = _read(z, "[Content_Types].xml").decode("utf-8", "replace") if "[Content_Types].xml" in names else ""
    if "word/vbaProject.bin" in names or _MACRO_TYPE in types:
        found.append(Finding("alerte", "macro", "document"))
    if (any(n.startswith("word/embeddings/") for n in names)
            or doc.find(".//" + _O + "OLEObject") is not None
            or doc.find(".//" + _W + "object") is not None):
        found.append(Finding("attention", "objet_integre", "document"))
    if doc.find(".//" + _W + "altChunk") is not None:
        found.append(Finding("attention", "altchunk", "document"))
    external = any(
        rel.get("TargetMode") == "External" and rel.get("Type", "").rsplit("/", 1)[-1] in _EXTERNAL_TYPES
        for n in names if n.endswith(".rels") for rel in _parse(z, n))
    if external:
        found.append(Finding("attention", "lien_externe", "document"))
    return found


def extract_docx(path: Path) -> Extracted:
    """Lit un DOCX : blocs par paragraphe, métadonnées, constats d'inspection."""
    try:
        with zipfile.ZipFile(str(path)) as z:
            doc = _parse(z, "word/document.xml")
            reader = _Reader()
            body = doc.find(_W + "body")
            for i, p in enumerate(body.iter(_W + "p") if body is not None else (), 1):
                reader.paragraph(p, "paragraphe %d" % i, "corps", "[IMAGE]")
            for kind, section, location in (("header", "entete", "en-tête"),
                                            ("footer", "pied", "pied de page")):
                for name in sorted(n for n in z.namelist()
                                   if n.startswith("word/%s" % kind) and n.endswith(".xml")):
                    for p in _parse(z, name).iter(_W + "p"):
                        reader.paragraph(p, location, section, "[LOGO]")
            if "word/comments.xml" in z.namelist():
                for i, c in enumerate(_parse(z, "word/comments.xml").iter(_W + "comment"), 1):
                    text = "\n".join("".join(t.text or "" for t in p.iter(_W + "t"))
                                     for p in c.iter(_W + "p"))
                    location = "commentaire %d" % i
                    reader.findings.append(Finding("info", "commentaire", location))
                    if text.strip():
                        reader.blocks.append(Block(text, location, "commentaire"))
            n = 0
            for name in ("word/footnotes.xml", "word/endnotes.xml"):
                if name not in z.namelist():
                    continue
                for note in _parse(z, name):
                    if note.get(_W + "type") in _SKIPPED_NOTES:
                        continue
                    n += 1
                    for p in note.iter(_W + "p"):
                        reader.paragraph(p, "note %d" % n, "corps", "[IMAGE]")
            reader.findings.extend(_active_content(z, doc))
            return Extracted(reader.blocks, _metadata(z), reader.findings)
    except (zipfile.BadZipFile, KeyError, ET.ParseError, RuntimeError, NotImplementedError) as exc:
        raise Unreadable("Fichier DOCX illisible ou corrompu (%s)." % type(exc).__name__) from exc
