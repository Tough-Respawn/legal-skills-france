"""Extraction et inspection d'un PDF (pypdf, importé à l'usage seulement)."""
from __future__ import annotations

import io
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ..modele import Block, Extracted, Finding
from . import MissingDependency, Unreadable

_IDENTITY = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
_SHOW = (b"Tj", b"TJ", b"'", b'"')
_INVISIBLE_MODES = (3, 7)   # sans remplissage ni contour
_NO_FILL_MODES = (1, 5)     # contour seul : la couleur de remplissage ne compte pas
_MIN_SIZE = 2.0             # points, après matrices
_WHITE = 0.95               # composante à partir de laquelle la couleur passe pour blanche
_MAX_FIELDS = 10000


def _mul(m: List[float], n: List[float]) -> List[float]:
    """Produit de deux matrices PDF [a b c d e f] : m puis n."""
    return [m[0] * n[0] + m[1] * n[2], m[0] * n[1] + m[1] * n[3],
            m[2] * n[0] + m[3] * n[2], m[2] * n[1] + m[3] * n[3],
            m[4] * n[0] + m[5] * n[2] + n[4], m[4] * n[1] + m[5] * n[3] + n[5]]


def _get(d: Any, key: str) -> Any:
    """Valeur résolue d'une clé de dictionnaire PDF, ou None."""
    return d[key] if isinstance(d, dict) and key in d else None


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
        box = page.cropbox  # zone visible ; vaut la MediaBox en l'absence de CropBox
        self.box = (float(box.left), float(box.bottom), float(box.right), float(box.top))
        self.ops: List[_Op] = []
        self.pending: List[_Op] = []
        self.segments: List[Tuple[str, List[_Op]]] = []
        self.image = False
        self.state = [0, False, 12.0]  # mode de rendu, remplissage blanc, corps de police
        self.saved: List[list] = []
        self.frames: List[tuple] = []
        self.base = list(_IDENTITY)  # matrice du XObject de formulaire en cours
        self.resources = _get(page, "/Resources")

    def before(self, op: bytes, args: list, cm: List[float], tm: List[float]) -> None:
        if op == b"Do":  # empilé avant tout, dépilé par after() même si la suite échoue
            self.frames.append((self.base, self.resources, list(self.state), len(self.saved)))
        try:
            self._before(op, args, cm, tm)
        except (TypeError, ValueError, IndexError, KeyError, AttributeError):
            pass  # opérateur mal formé : ignoré, comme le fait pypdf

    def _before(self, op: bytes, args: list, cm: List[float], tm: List[float]) -> None:
        if op == b"q":
            self.saved.append(list(self.state))
        elif op == b"Q" and self.saved:
            self.state = self.saved.pop()
        elif op == b"Tr":
            self.state[0] = int(args[0])
        elif op == b"rg":
            self.state[1] = min(float(a) for a in args[:3]) >= _WHITE
        elif op == b"g":
            self.state[1] = float(args[0]) >= _WHITE
        elif op == b"k":
            self.state[1] = max(float(a) for a in args[:4]) <= 1 - _WHITE
        elif op == b"Tf":
            self.state[2] = float(args[1])
        elif op in _SHOW:
            self._show(cm, tm)
        elif op == b"Do":
            self._do(args[0], cm)
        elif op == b"INLINE IMAGE":
            self._image(cm)
        # ponytail: couleurs sc/scn, rectangles « re f » couvrants et transparence ignorés

    def after(self, op: bytes, args: list, cm: List[float], tm: List[float]) -> None:
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
            self._image(cm)
        elif subtype == "/Form":  # pypdf repart d'une matrice identité dans le formulaire
            matrix = [float(v) for v in (_get(xobject, "/Matrix") or _IDENTITY)]
            self.base = _mul(matrix, _mul(cm, self.base))
            self.resources = _get(xobject, "/Resources") or self.resources

    def _image(self, cm: List[float]) -> None:
        """L'image occupe le carré unité transformé : le texte déjà peint dessous est caché."""
        self.image = True
        a, b, c, d, e, f = _mul(cm, self.base)
        xs = (e, a + e, c + e, a + c + e)
        ys = (f, b + f, d + f, b + d + f)
        # ponytail: origine du texte seulement, sans largeur ni masque de transparence
        for op in self.ops:
            if min(xs) <= op.x <= max(xs) and min(ys) <= op.y <= max(ys):
                op.flags.add("texte_sous_image")

    def blocks(self, location: str) -> Tuple[List[Block], List[Finding]]:
        """Un bloc corps par page, puis un bloc cache par suite de paquets aux mêmes codes."""
        body: List[str] = []
        hidden: List[list] = []
        for text, ops in self.segments:
            flags = tuple(sorted(set().union(*(op.flags for op in ops))))
            if not flags:
                body.append(text)
            elif hidden and hidden[-1][0] == flags:
                hidden[-1][1] += text
            else:
                hidden.append([flags, text])
        blocks: List[Block] = []
        findings: List[Finding] = []
        corps = "".join(body).strip()
        if corps:
            blocks.append(Block(corps, location, "corps"))
        for flags, text in hidden:
            if text.strip():
                blocks.append(Block(text.strip(), location, "cache"))
                findings.extend(Finding("attention", code, location) for code in flags)
        if self.image and not blocks:
            findings.append(Finding("info", "page_sans_texte", location))  # OCR : tâche 5
        return blocks, findings


def _is_js(action: Any) -> bool:
    return isinstance(action, dict) and (_get(action, "/S") == "/JavaScript" or "/JS" in action)


def _structure(root: Any, data: bytes) -> List[Finding]:
    """Contenu actif du catalogue, signatures et mises à jour incrémentales."""
    found: List[Finding] = []
    names = _get(root, "/Names")
    if _get(names, "/JavaScript") is not None:
        found.append(Finding("alerte", "javascript", "document"))
    if _get(names, "/EmbeddedFiles") is not None:
        found.append(Finding("attention", "fichier_joint", "document"))
    # Une /OpenAction tableau n'est qu'une vue initiale ; seule une action compte.
    actions = [a for a in (_get(root, "/OpenAction"),) if isinstance(a, dict)]
    aa = _get(root, "/AA")
    if isinstance(aa, dict):
        actions.extend(aa[k] for k in aa)
    if actions:
        found.append(Finding("alerte", "action_ouverture", "document"))
    if any(_is_js(a) for a in actions):
        found.append(Finding("alerte", "javascript", "document"))
    # ponytail: actions des pages, annotations et champs non parcourues

    fields = list(_get(_get(root, "/AcroForm"), "/Fields") or [])
    for _ in range(_MAX_FIELDS):  # borne contre les arbres de champs cycliques
        if not fields:
            break
        field = fields.pop().get_object()
        fields.extend(_get(field, "/Kids") or [])
        value = _get(field, "/V")
        if _get(field, "/FT") != "/Sig" or not isinstance(value, dict):
            continue
        found.append(Finding("info", "signature", "document"))
        byte_range = _get(value, "/ByteRange")
        try:
            covered = int(byte_range[2]) + int(byte_range[3]) == len(data)
        except (TypeError, ValueError, IndexError):
            covered = False
        if not covered:
            found.append(Finding("alerte", "signature_partielle", "document"))

    linearized = 1 if b"/Linearized" in data[:1024] else 0
    if data.count(b"%%EOF") - linearized > 1:
        found.append(Finding("attention", "pdf_modifie", "document"))
    unique: List[Finding] = []
    for f in found:
        if f not in unique:
            unique.append(f)
    return unique


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
            meta[key] = when.strftime("%Y-%m-%dT%H:%M:%S")
    return meta


def extract_pdf(path: Path) -> Extracted:
    """Lit un PDF : un bloc par page, texte caché à part, métadonnées, constats d'inspection."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise MissingDependency("La bibliothèque pypdf est requise pour lire les PDF.") from exc
    data = Path(path).read_bytes()
    if b"%%EOF" not in data[-1024:]:
        raise Unreadable("Fichier PDF tronqué ou corrompu.")
    try:
        reader = PdfReader(io.BytesIO(data))
        if reader.is_encrypted:
            raise Unreadable("Fichier PDF chiffré : retirer la protection avant l'analyse.")
        blocks: List[Block] = []
        findings: List[Finding] = []
        for n, page in enumerate(reader.pages, 1):
            scan = _PageScan(page)
            page.extract_text(visitor_operand_before=scan.before,
                              visitor_operand_after=scan.after, visitor_text=scan.text)
            page_blocks, page_findings = scan.blocks("page %d" % n)
            blocks.extend(page_blocks)
            findings.extend(page_findings)
        findings.extend(_structure(reader.trailer["/Root"], data))
        return Extracted(blocks, _metadata(reader), findings)
    except Unreadable:
        raise
    except Exception as exc:  # pypdf lève des types variés sur un fichier malformé
        raise Unreadable("Fichier PDF illisible ou corrompu (%s)." % type(exc).__name__) from exc
