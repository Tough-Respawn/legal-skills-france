"""Extraction et inspection d'un PDF (pypdf, importé à l'usage seulement)."""
from __future__ import annotations

import io
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ..modele import Block, Extracted, Finding
from . import MissingDependency, Unreadable, ocr

_IDENTITY = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
_SHOW = (b"Tj", b"TJ", b"'", b'"')
_INVISIBLE_MODES = (3, 7)   # sans remplissage ni contour
_NO_FILL_MODES = (1, 5)     # contour seul : la couleur de remplissage ne compte pas
_MIN_SIZE = 2.0             # points, après matrices
_WHITE = 0.95               # composante à partir de laquelle la couleur passe pour blanche
_SCAN_COVER = 0.9           # part de la page couverte par une image de numérisation
_SCAN_TEXT = 200            # caractères visibles au plus sur une page numérisée
_SAME_LINE = 1.0            # écart vertical (pt) sous lequel deux paquets sont sur la même ligne
_OCR_FLAGS = {"texte_invisible", "texte_sous_image"}
_MAX_FIELDS = 10000
_MAX_CHAIN = 16             # profondeur d'une chaîne d'actions /Next
_MAX_ACTIONS = 256          # actions examinées par chaîne (tableaux /Next compris)
_ENCRYPTED = "Fichier PDF chiffré : retirer la protection avant l'analyse."


def _mul(m: List[float], n: List[float]) -> List[float]:
    """Produit de deux matrices PDF [a b c d e f] : m puis n."""
    return [m[0] * n[0] + m[1] * n[2], m[0] * n[1] + m[1] * n[3],
            m[2] * n[0] + m[3] * n[2], m[2] * n[1] + m[3] * n[3],
            m[4] * n[0] + m[5] * n[2] + n[4], m[4] * n[1] + m[5] * n[3] + n[5]]


def _get(d: Any, key: str) -> Any:
    """Valeur résolue d'une clé de dictionnaire PDF, ou None."""
    return d[key] if isinstance(d, dict) and key in d else None


def _resolve(x: Any) -> Any:
    return x.get_object() if hasattr(x, "get_object") else x


def _rect(r: Any) -> Tuple[float, float, float, float]:
    """Rectangle normalisé (x0, y0, x1, y1), coins opposés dans n'importe quel ordre."""
    x0, y0, x1, y1 = (float(v) for v in r)
    return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)


def _white(values: list) -> bool:
    """Couleur de remplissage blanche, selon le nombre de composantes (gris, RVB, CMJN)."""
    v = [float(a) for a in values]
    # ponytail: espaces Separation et Indexed lus comme gris ; résoudre l'espace si besoin
    if len(v) == 4:
        return max(v) <= 1 - _WHITE
    return len(v) in (1, 3) and all(_WHITE <= c <= 1 for c in v)


def _masked(image: Any) -> bool:
    """Image transparente (masque doux, masque ou pochoir) : elle ne cache pas le texte."""
    return (_get(image, "/SMask") is not None or _get(image, "/Mask") is not None
            or _get(image, "/ImageMask") == True or _get(image, "/IM") == True)  # noqa: E712


class _Op:
    """Un opérateur d'affichage de texte : position (espace utilisateur) et codes de constat."""
    __slots__ = ("x", "y", "flags")

    def __init__(self, x: float, y: float, flags: set) -> None:
        self.x, self.y, self.flags = x, y, flags


# ponytail: granularité du paquet pypdf ; un paquet mêlant texte visible et caché part
# entier en cache (faux positif plutôt qu'oubli) ; découpe par opérateur si cela gêne
class _PageScan:
    """Suit l'état graphique pendant l'extraction pypdf d'une page.

    Le texte arrive par paquets (visitor_text) ; chaque paquet reçoit les codes des
    opérateurs d'affichage vus depuis le paquet précédent.
    """

    def __init__(self, page: Any) -> None:
        crop, media = _rect(page.cropbox), _rect(page.mediabox)  # zone visible : intersection
        self.box = (max(crop[0], media[0]), max(crop[1], media[1]),
                    min(crop[2], media[2]), min(crop[3], media[3]))
        self.ops: List[_Op] = []
        self.pending: List[_Op] = []
        self.segments: List[Tuple[str, List[_Op]]] = []
        self.images: List[tuple] = []  # (x0, y0, x1, y1, couverture de la page, opaque)
        self.state = [0, False, 12.0]  # mode de rendu, remplissage blanc, corps de police
        self.saved: List[list] = []
        self.frames: List[tuple] = []
        self.base = list(_IDENTITY)  # matrice du XObject de formulaire en cours
        self.resources = _get(page, "/Resources")

    def before(self, op: bytes, args: Any, cm: List[float], tm: List[float]) -> None:
        if op == b"Do":  # empilé avant tout, dépilé par after() même si la suite échoue
            self.frames.append((self.base, self.resources, list(self.state), len(self.saved)))
        try:
            self._before(op, args, cm, tm)
        except (TypeError, ValueError, IndexError, KeyError, AttributeError):
            pass  # opérateur mal formé : ignoré, comme le fait pypdf

    def _before(self, op: bytes, args: Any, cm: List[float], tm: List[float]) -> None:
        if op == b"q":
            self.saved.append(list(self.state))
        elif op == b"Q" and self.saved:
            self.state = self.saved.pop()
        elif op == b"Tr":
            self.state[0] = int(args[0])
        elif op == b"cs":  # nouvel espace de couleur : remplissage remis au noir
            self.state[1] = False
        elif op in (b"rg", b"g", b"k", b"sc", b"scn"):
            self.state[1] = _white(args)
        elif op == b"Tf":
            self.state[2] = float(args[1])
        elif op in _SHOW:
            self._show(cm, tm)
        elif op == b"Do":
            self._do(args[0], cm)
        elif op == b"INLINE IMAGE":
            self._image(cm, not _masked(_get(args, "settings")))
        # ponytail: rectangles « re f » couvrants et transparence de l'état graphique ignorés

    def after(self, op: bytes, args: Any, cm: List[float], tm: List[float]) -> None:
        if op == b"Do" and self.frames:
            self.base, self.resources, self.state, depth = self.frames.pop()
            del self.saved[depth:]

    def text(self, text: str, *_: Any) -> None:
        # Paquet sans nouvel opérateur (coupure bidirectionnelle) : rattaché au dernier.
        ops = self.pending or (self.ops[-1:] if text.strip() else [])
        if text:
            self.segments.append((text, ops))
        self.pending = []

    def _show(self, cm: List[float], tm: List[float]) -> None:
        m = _mul(_mul(tm, cm), self.base)
        render, white, size = self.state
        flags = set()
        if render in _INVISIBLE_MODES:
            flags.add("texte_invisible")
        if white and render not in _NO_FILL_MODES:
            flags.add("texte_blanc")
        if abs(size) * math.hypot(m[2], m[3]) < _MIN_SIZE:  # corps négatif : texte miroir
            flags.add("texte_minuscule")
        x0, y0, x1, y1 = self.box
        if not (x0 <= m[4] <= x1 and y0 <= m[5] <= y1):
            flags.add("texte_hors_page")
        op = _Op(m[4], m[5], flags)
        self.ops.append(op)
        self.pending.append(op)

    def _do(self, name: Any, cm: List[float]) -> None:
        xobject = _get(_get(self.resources, "/XObject"), name)
        subtype = _get(xobject, "/Subtype")
        if subtype == "/Image":
            self._image(cm, not _masked(xobject))
        elif subtype == "/Form":  # pypdf repart d'une matrice identité dans le formulaire
            matrix = [float(v) for v in (_get(xobject, "/Matrix") or _IDENTITY)]
            self.base = _mul(matrix, _mul(cm, self.base))
            self.resources = _get(xobject, "/Resources") or self.resources

    def _image(self, cm: List[float], opaque: bool) -> None:
        """L'image occupe le carré unité transformé ; opaque, elle cache le texte déjà peint."""
        a, b, c, d, e, f = _mul(cm, self.base)
        xs, ys = (e, a + e, c + e, a + c + e), (f, b + f, d + f, b + d + f)
        x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
        px0, py0, px1, py1 = self.box
        page = max(0.0, px1 - px0) * max(0.0, py1 - py0)
        inter = (max(0.0, min(x1, px1) - max(x0, px0)) * max(0.0, min(y1, py1) - max(y0, py0)))
        self.images.append((x0, y0, x1, y1, inter / page if page else 0.0, opaque))
        if opaque:  # ponytail: origine du texte seulement, sans sa largeur
            for op in self.ops:
                if x0 <= op.x <= x1 and y0 <= op.y <= y1:
                    op.flags.add("texte_sous_image")

    def blocks(self, location: str) -> Tuple[List[Block], List[Finding], bool]:
        """Bloc corps (couche OCR comprise), blocs cache par suite de codes, constats, OCR."""
        # Numérisation : image opaque sur 90 % de la page, jamais un filigrane transparent.
        scans = [im[:4] for im in self.images if im[4] >= _SCAN_COVER and im[5]]

        def in_scan(ops: List[_Op]) -> bool:
            return bool(ops) and all(any(x0 <= o.x <= x1 and y0 <= o.y <= y1
                                         for x0, y0, x1, y1 in scans) for o in ops)

        body: List[str] = []
        hidden: List[list] = []
        ocr = False
        visible_on_scan = 0
        for text, ops in self.segments:
            flags = set().union(*(op.flags for op in ops))
            if flags and flags <= _OCR_FLAGS and in_scan(ops):  # couche OCR d'une numérisation
                ocr = True
                body.append(text)
            elif not flags:
                body.append(text)
                if in_scan(ops):
                    visible_on_scan += len(text.strip())
            elif hidden and hidden[-1][0] == sorted(flags):
                group = hidden[-1]  # [codes, texte, ordonnée du dernier opérateur]
                if (abs(ops[0].y - group[2]) >= _SAME_LINE
                        and not (group[1][-1:].isspace() or text[:1].isspace())):
                    group[1] += "\n"  # lignes distinctes : ne pas recoller les valeurs
                group[1] += text  # même ligne : changement de police au milieu d'un mot
                group[2] = ops[-1].y
            else:
                hidden.append([sorted(flags), text, ops[-1].y])
        blocks: List[Block] = []
        findings: List[Finding] = []
        corps = "".join(body).strip()
        if corps:
            blocks.append(Block(corps, location, "corps"))
        for flags, text, _ in hidden:
            if text.strip():
                blocks.append(Block(text.strip(), location, "cache"))
                findings.extend(Finding("attention", code, location) for code in flags)
        if ocr:
            findings.append(Finding("info", "texte_ocr", location))
        # Une couche OCR présente tient lieu de texte : pas de seconde reconnaissance.
        if self.images and not ocr and (not blocks or (scans and visible_on_scan <= _SCAN_TEXT)):
            findings.append(Finding("info", "page_sans_texte", location))  # consommé par extract_pdf
        return blocks, findings, ocr


def _annotations(page: Any, location: str) -> Tuple[List[Block], List[Finding]]:
    """Notes /Text et /FreeText : section commentaire ; liens : JavaScript dans leurs actions.

    Un lien URI ou GoTo est ordinaire : seul le JavaScript de sa chaîne est signalé.
    """
    blocks, findings = [], []
    for annot in _get(page, "/Annots") or []:
        annot = _resolve(annot)
        subtype, contents = _get(annot, "/Subtype"), _get(annot, "/Contents")
        if subtype in ("/Text", "/FreeText") and isinstance(contents, str) and contents.strip():
            blocks.append(Block(contents.strip(), location, "commentaire"))
            findings.append(Finding("info", "commentaire", location))
        elif subtype == "/Link":
            aa = _get(annot, "/AA")
            actions = [_get(annot, "/A")] + [aa[k] for k in (aa if isinstance(aa, dict) else ())]
            js = Finding("alerte", "javascript", location)
            if js not in findings and any(_is_js(a) for x in actions for a in _chain(x)):
                findings.append(js)
    return blocks, findings


def _is_js(action: Any) -> bool:
    return isinstance(action, dict) and (_get(action, "/S") == "/JavaScript" or "/JS" in action)


def _chain(action: Any) -> List[Any]:
    """Une action et sa chaîne /Next (dictionnaire ou tableau), profondeur et taille bornées."""
    found: List[Any] = []
    todo = [(action, 0)] if isinstance(_resolve(action), dict) else []  # tableau : destination
    for _ in range(_MAX_ACTIONS):
        if not todo:
            break
        item, depth = todo.pop()
        item = _resolve(item)
        if isinstance(item, list):
            todo.extend((x, depth) for x in item)
        elif isinstance(item, dict) and depth < _MAX_CHAIN:
            found.append(item)
            if "/Next" in item:
                todo.append((item["/Next"], depth + 1))
    return found


def _fields(root: Any, data: bytes, pages: Dict[int, int]) -> Tuple[List[Block], List[Finding]]:
    """Champs AcroForm : valeurs texte et liste en blocs, signatures en constats."""
    blocks: List[Block] = []
    found: List[Finding] = []
    stack = [(f, None) for f in reversed(_get(_get(root, "/AcroForm"), "/Fields") or [])]
    for _ in range(_MAX_FIELDS):  # borne contre les arbres de champs cycliques
        if not stack:
            break
        ref, inherited = stack.pop()
        field = _resolve(ref)
        if not isinstance(field, dict):
            continue
        ft = _get(field, "/FT") or inherited
        kids = [_resolve(k) for k in _get(field, "/Kids") or []]
        stack.extend((k, ft) for k in reversed(kids))
        value = _get(field, "/V")
        if ft == "/Sig" and isinstance(value, dict):
            found.append(Finding("info", "signature", "document"))
            byte_range = _get(value, "/ByteRange")
            try:
                covered = int(byte_range[2]) + int(byte_range[3]) == len(data)
            except (TypeError, ValueError, IndexError):
                covered = False
            if not covered:
                found.append(Finding("alerte", "signature_partielle", "document"))
        elif ft in ("/Tx", "/Ch") and value is not None:
            items = value if isinstance(value, list) else [value]
            text = "\n".join(v for v in map(_resolve, items) if isinstance(v, str)).strip()
            if not text:
                continue
            refs = [field.get("/P")] + [k.get("/P") for k in kids if isinstance(k, dict)]
            page = next((pages[r.idnum] for r in refs if getattr(r, "idnum", None) in pages), None)
            blocks.append(Block(text, "page %d" % page if page else "champ %d" % (len(blocks) + 1),
                                "corps"))
    return blocks, found


def _structure(root: Any, data: bytes) -> List[Finding]:
    """Contenu actif du catalogue et mises à jour incrémentales."""
    found: List[Finding] = []
    names = _get(root, "/Names")
    if _get(names, "/JavaScript") is not None:
        found.append(Finding("alerte", "javascript", "document"))
    if _get(names, "/EmbeddedFiles") is not None:
        found.append(Finding("attention", "fichier_joint", "document"))
    # /OpenAction tableau ou /GoTo seul : simple vue initiale ; toute autre chaîne compte.
    opening = _chain(_get(root, "/OpenAction"))
    triggered = len(opening) > 1 or any(_get(a, "/S") != "/GoTo" for a in opening)
    aa = _get(root, "/AA")
    for key in aa if isinstance(aa, dict) else ():
        chain = _chain(aa[key])
        opening += chain
        triggered = triggered or bool(chain)
    if triggered:
        found.append(Finding("alerte", "action_ouverture", "document"))
    if any(_is_js(a) for a in opening):
        found.append(Finding("alerte", "javascript", "document"))
    # ponytail: actions des pages et des champs non parcourues
    linearized = 1 if b"/Linearized" in data[:1024] else 0
    if data.count(b"%%EOF") - linearized > 1:
        found.append(Finding("attention", "pdf_modifie", "document"))
    return found


def _iso(when: Any) -> str:
    """Date ISO 8601 à la seconde, fuseau conservé (Z pour UTC)."""
    text = when.isoformat(timespec="seconds")
    return text[:-6] + "Z" if text.endswith("+00:00") else text


def _metadata(reader: Any) -> Dict[str, str]:
    meta: Dict[str, str] = {}
    info = reader.metadata
    if info is None:
        return meta
    if info.author and info.author.strip():
        meta["auteur"] = info.author.strip()
    for key, attr in (("cree", "creation_date"), ("modifie", "modification_date")):
        try:
            when = getattr(info, attr)
        except ValueError:  # date mal formée : ignorée
            continue
        if when is not None:
            meta[key] = _iso(when)
    return meta


def extract_pdf(path: Path, workdir: Path) -> Extracted:
    """Lit un PDF : un bloc par page, texte caché à part, métadonnées, constats d'inspection."""
    try:
        from pypdf import PdfReader
        from pypdf.errors import DependencyError
    except ImportError as exc:
        raise MissingDependency("La bibliothèque pypdf est requise pour lire les PDF.") from exc
    data = Path(path).read_bytes()
    if b"%%EOF" not in data[-1024:]:
        raise Unreadable("Fichier PDF tronqué ou corrompu.")
    try:
        try:
            reader = PdfReader(io.BytesIO(data))
        except DependencyError as exc:  # chiffrement AES sans bibliothèque de chiffrement
            raise Unreadable(_ENCRYPTED) from exc
        if reader.is_encrypted:
            raise Unreadable(_ENCRYPTED)
        blocks: List[Block] = []
        findings: List[Finding] = []
        has_ocr = False
        pages: Dict[int, int] = {}
        for n, page in enumerate(reader.pages, 1):
            location = "page %d" % n
            if page.indirect_reference is not None:
                pages[page.indirect_reference.idnum] = n
            scan = _PageScan(page)
            page.extract_text(visitor_operand_before=scan.before,
                              visitor_operand_after=scan.after, visitor_text=scan.text)
            page_blocks, page_findings, page_ocr = scan.blocks(location)
            if any(f.code == "page_sans_texte" for f in page_findings):
                ocr.require()  # jamais de dégradation silencieuse sur une numérisation
                text = ocr.page_text(page, workdir)
                page_findings = [f for f in page_findings if f.code != "page_sans_texte"]
                if text:
                    page_blocks.append(Block(text, location, "corps"))
                    page_findings.append(Finding("info", "texte_ocr", location, "ocr_local"))
                    page_ocr = True
            notes, note_findings = _annotations(page, location)
            blocks += page_blocks + notes
            findings += page_findings + note_findings
            has_ocr = has_ocr or page_ocr
        root = reader.trailer["/Root"]
        field_blocks, field_findings = _fields(root, data, pages)
        blocks += field_blocks
        for f in field_findings + _structure(root, data):  # constats du document : uniques
            if f not in findings:
                findings.append(f)
        return Extracted(blocks, _metadata(reader), findings, has_ocr)
    except (Unreadable, MissingDependency):
        raise
    except Exception as exc:  # pypdf lève des types variés sur un fichier malformé
        raise Unreadable("Fichier PDF illisible ou corrompu (%s)." % type(exc).__name__) from exc
