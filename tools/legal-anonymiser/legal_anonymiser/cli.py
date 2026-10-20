"""Ligne de commande : traiter, relancer, valider, verifier, reidentifier, install-hook, uninstall-hook.

Codes de sortie : 0 publié (ou vérification `publie`), 1 vérification négative, 3 arbitrage en attente,
4 non publié, 5 format ou fichier illisible, 6 dépendance manquante, 7 erreur interne (trace dans le coffre).
Aucun import de pypdf, PIL ou spaCy ici : `nonet.install()` est la première instruction de `main`.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import traceback
from pathlib import Path
from typing import List, Optional

from . import nonet, sortie
from .coffre import RegistryCorrupted, Vault, atomic_write, original_inside
from .sortie import say

CID_RX = re.compile(r"[0-9a-f]{6}")
FILETYPES = [("Contrats", "*.docx *.pdf *.jpg *.jpeg *.png"), ("Word", "*.docx"), ("PDF", "*.pdf"),
             ("Images", "*.jpg *.jpeg *.png")]
_current = {"cid": None}   # contrat en cours, pour ranger la trace d'une erreur interne


class _NoPicker(Exception):
    """tkinter absent ou sans affichage : pas de sélecteur de fichier."""


def _pick() -> Optional[str]:
    """Sélecteur de fichier natif ; None si l'utilisateur annule, `_NoPicker` sans tkinter ni affichage."""
    try:
        import tkinter
        from tkinter import filedialog
    except ImportError:
        raise _NoPicker() from None
    try:
        root = tkinter.Tk()
    except tkinter.TclError:
        raise _NoPicker() from None
    try:
        root.withdraw()
        root.attributes("-topmost", True)
        return filedialog.askopenfilename(parent=root, title="Contrat à masquer", filetypes=FILETYPES) or None
    except tkinter.TclError:
        raise _NoPicker() from None
    finally:
        root.destroy()


def _contract(vault: Vault, cid: str) -> bool:
    """Vrai si `cid` est un identifiant neutre connu ; sinon le message adapté est affiché (jamais `cid`)."""
    if not CID_RX.fullmatch(cid):
        say("id_invalide")
        return False
    if cid not in vault.known_ids():
        say("inconnu", cid=cid)
        return False
    _current["cid"] = cid
    return True


def _after_run(vault: Vault, cid: str, result) -> int:
    say("resume", cid=cid, entities=len(result.entities), alerts=len(result.alerts),
        ambiguities=len(result.ambiguities))
    if result.extracted and any(f.code == "ner_absente" for f in result.extracted.findings):
        say("ner_absente")   # le passage continue sans NER : à dire ici, pas seulement dans masque.md
    path = sortie.neutral(vault.root / cid / "ajustements.txt", Path.cwd(), vault)
    if result.pending:
        say("pending", pending=result.pending, path=path, cid=cid)
        return 3
    if result.alerts or result.ambiguities:   # décisions prises mais points encore ouverts (masquer sans effet, etc.)
        say("ouverts", ouverts=len(result.alerts) + len(result.ambiguities), path=path, cid=cid)
        return 3
    return _validate(vault, cid)


def _ready(vault: Vault, cid: str, state: dict) -> Optional[str]:
    """Clé du message qui empêche la validation, ou None quand le dernier passage n'a rien laissé ouvert
    et que `masque.md` (marqueur `corps=` et `passage=` compris), `ajustements.txt` et `correspondance.json`
    sont ceux qu'il a écrits."""
    from .rendu import MARKER_RE, body_hash
    folder = vault.root / cid
    masque, adj, table = folder / "masque.md", folder / "ajustements.txt", folder / "correspondance.json"
    if not (masque.is_file() and adj.is_file() and table.is_file()):
        return "non_pret"
    data = masque.read_bytes()
    if (state.get("pending") != 0 or state.get("ouverts") != 0 or b"[AMBIGU_" in data):
        return "non_pret"
    marker = MARKER_RE.match(data.split(b"\n", 1)[0].decode("utf-8", "replace"))
    if (body_hash(data) != state.get("sha_masque") or not marker or marker.group("corps") != body_hash(data)[:16]
            or not marker.group("passage")
            or hashlib.sha256(adj.read_bytes()).hexdigest() != state.get("sha_ajustements")
            or hashlib.sha256(table.read_bytes()).hexdigest() != state.get("sha_correspondance")):
        return "modifie_depuis"   # un `masque.md` de la v4.5.0 (sans `corps=`) demande aussi un `relancer`
    return None


def _validate(vault: Vault, cid: str) -> int:
    from . import publication, validation
    folder = vault.root / cid
    masque, rapport, adj = folder / "masque.md", folder / "rapport.md", folder / "ajustements.txt"
    cwd = Path.cwd()
    state = vault.read_state(cid)
    blocker = _ready(vault, cid, state)
    if blocker:
        say(blocker, cid=cid, path=sortie.neutral(adj, cwd, vault))
        return 3
    today = datetime.date.today().isoformat()
    first, rest = masque.read_text("utf-8").split("\n", 1)
    text = re.sub(r"date=\d{4}-\d{2}-\d{2}", "date=" + today, first, count=1) + "\n" + rest
    data = text.encode("utf-8")
    atomic_write(masque, data)
    digest = hashlib.sha256(data).hexdigest()
    answer = validation.confirm([masque, rapport],
                                question="Contrat %s : relisez les fichiers ouverts. Publier ce contrat masqué ?" % cid)
    if answer == "publier":
        data = masque.read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            say("modifie")
            return 4
        if _ready(vault, cid, vault.read_state(cid)):   # ajustements ou état modifiés pendant la fenêtre
            say("modifie_pendant_relecture", cid=cid)
            return 3
        try:
            target = publication.publish(vault, cid, data.decode("utf-8"), Path(state["destination"]))
        except OSError:
            say("publication_impossible")
            return 4
        except ValueError:   # marqueur ou table figée incohérents : jamais le message, il peut citer un chemin
            say("publication_refusee", cid=cid)
            return 4
        say("publie", name=target.name)
        say("rappel")
        return 0
    if answer == "ajuster":
        say("ajuster", path=sortie.neutral(adj, cwd, vault), cid=cid)
        return 3
    say("impossible" if answer == validation.IMPOSSIBLE else "abandon", cid=cid)
    return 4


def _run(vault: Vault, original: Path, cid: str) -> int:
    from . import pipeline
    _current["cid"] = cid
    if original_inside(original, Path.cwd()):
        say("original_inside")
    return _after_run(vault, cid, pipeline.run(original, vault, cid))


def _traiter(args: argparse.Namespace) -> int:
    from .extraction import supported
    vault = Vault()
    chosen = args.chemin
    if not chosen:
        try:
            chosen = _pick()
        except _NoPicker:
            say("selecteur_indisponible")
            return 4
    if not chosen:
        say("aucun_fichier")
        return 4
    original = Path(chosen)
    if not original.is_file():
        say("introuvable")
        return 5
    if not supported(original):   # contrôlé avant tout enregistrement au coffre
        say("illisible")
        return 5
    vault.ensure()   # après le sélecteur et les contrôles : un choix annulé ne crée pas le coffre
    return _run(vault, original, vault.id_for_original(original))


def _relancer(args: argparse.Namespace) -> int:
    vault = Vault()
    if not _contract(vault, args.id):
        return 4
    original = vault.original_for(args.id)
    if original is None or not original.is_file():
        say("introuvable")
        return 5
    return _run(vault, original, args.id)


def _valider(args: argparse.Namespace) -> int:
    vault = Vault()
    return _validate(vault, args.id) if _contract(vault, args.id) else 4


def _verifier(args: argparse.Namespace) -> int:
    from . import publication
    status = publication.verify(Vault(), Path(args.fichier))
    print(status)
    return 0 if status == "publie" else 1


def _reidentifier(args: argparse.Namespace) -> int:
    from . import reidentification, validation
    vault = Vault()
    if not _contract(vault, args.id):
        return 7
    try:
        target = reidentification.run(vault, args.id, Path(args.rapport))
    except reidentification.SansPublication:
        say("reidentification_sans_publication", cid=args.id)
        return 7
    except (OSError, UnicodeDecodeError, ValueError):
        say("rapport_illisible")
        return 7
    say("reidentifie", path=sortie.neutral(target, Path.cwd(), vault))
    validation.default_open(target)
    return 0


def _settings_path(given: Optional[str]) -> Path:
    return Path(given) if given else Path.home() / ".claude" / "settings.json"


def _install_hook(args: argparse.Namespace) -> int:
    from . import installation
    version = installation.claude_version()
    try:
        result = installation.install(_settings_path(args.settings), Vault().root, version)
    except installation.VersionTooOld:
        say("verrou_version", version=version or "aucune")
        return 6
    except installation.SettingsInvalid:
        say("verrou_reglages_invalides")
        return 7
    say("verrou_installe" if result == "installé" else "verrou_deja")
    return 0


def _uninstall_hook(args: argparse.Namespace) -> int:
    from . import installation
    try:
        result = installation.uninstall(_settings_path(args.settings))
    except installation.SettingsInvalid:
        say("verrou_reglages_invalides")
        return 7
    say("verrou_retire" if result == "retiré" else "verrou_absent")
    return 0


class _Parser(argparse.ArgumentParser):
    """Une erreur d'arguments n'est jamais relayée (argparse y cite l'argument fautif, chemin compris)."""

    def error(self, message: str) -> None:   # type: ignore[override]
        self.exit(2, sortie.MESSAGES["arguments"] + "\n")


def _parser() -> argparse.ArgumentParser:
    p = _Parser(prog="legal-anonymiser", description="Pseudonymisation locale de contrats, sans réseau.")
    sub = p.add_subparsers(dest="commande", required=True)
    s = sub.add_parser("traiter", help="masquer un contrat (sélecteur de fichier sans chemin)")
    s.add_argument("chemin", nargs="?")
    s.set_defaults(func=_traiter)
    s = sub.add_parser("relancer", help="relire ajustements.txt et relancer le masquage")
    s.add_argument("id")
    s.set_defaults(func=_relancer)
    s = sub.add_parser("valider", help="relecture et publication, si plus rien n'est en attente")
    s.add_argument("id")
    s.set_defaults(func=_valider)
    s = sub.add_parser("verifier", help="publie, modifie ou inconnu")
    s.add_argument("fichier")
    s.set_defaults(func=_verifier)
    s = sub.add_parser("reidentifier", help="rapport final avec les valeurs réelles, dans le coffre")
    s.add_argument("id")
    s.add_argument("rapport")
    s.set_defaults(func=_reidentifier)
    for name, func, help_ in (("install-hook", _install_hook, "verrou Claude Code dans ~/.claude/settings.json"),
                              ("uninstall-hook", _uninstall_hook, "retirer le verrou Claude Code")):
        s = sub.add_parser(name, help=help_)
        s.add_argument("--settings", help="fichier de réglages (défaut : ~/.claude/settings.json)")
        s.set_defaults(func=func)
    return p


def _trace(vault: Vault) -> Path:
    cid = _current["cid"]
    if cid:
        target = vault.contract_dir(cid) / "erreur.txt"
    else:
        folder = vault.root / "erreurs"
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / (datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".txt")
    atomic_write(target, traceback.format_exc().encode("utf-8"))
    return target


def main(argv: Optional[List[str]] = None) -> int:
    nonet.install()
    from .ajustements import AdjustmentsError
    from .extraction import MissingDependency, Unreadable, UnsupportedFormat
    args = _parser().parse_args(argv)
    _current["cid"] = None
    try:
        return args.func(args)
    except KeyboardInterrupt:
        say("interrompu")
        return 4
    except (UnsupportedFormat, Unreadable):
        say("illisible")
        return 5
    except MissingDependency as exc:   # ModelMissing compris ; messages fixes de nos modules, sans chemin
        say("dependance", hint=str(exc))
        return 6
    except RegistryCorrupted as exc:   # messages fixes de coffre.py : étiquette neutre du fichier, rien d'autre
        print(str(exc))
        return 7
    except AdjustmentsError as exc:   # jamais str(exc) : le numéro de ligne et le chemin neutre suffisent
        vault = Vault()
        path = sortie.neutral(vault.root / (_current["cid"] or "") / "ajustements.txt", Path.cwd(), vault)
        if exc.line_no:
            say("ajustements_ligne", line=exc.line_no, path=path)
        else:
            say("ajustements_illisible", path=path)
        return 7
    except Exception:
        vault = Vault()
        try:
            say("erreur_interne", path=sortie.neutral(_trace(vault), Path.cwd(), vault))
        except Exception:
            print(sortie.MESSAGES["erreur_interne"].format(path=sortie.HIDDEN))
        return 7
