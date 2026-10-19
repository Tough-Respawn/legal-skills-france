"""Ligne de commande : traiter, relancer, valider, verifier, reidentifier.

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


def _pick() -> Optional[str]:
    """Sélecteur de fichier natif ; None sans tkinter ou si l'utilisateur annule."""
    try:
        import tkinter
        from tkinter import filedialog
    except ImportError:
        return None
    try:
        root = tkinter.Tk()
    except tkinter.TclError:
        return None
    try:
        root.withdraw()
        root.attributes("-topmost", True)
        return filedialog.askopenfilename(parent=root, title="Contrat à masquer", filetypes=FILETYPES) or None
    except tkinter.TclError:
        return None
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
    if result.pending:
        say("pending", pending=result.pending, path=sortie.neutral(vault.root / cid / "ajustements.txt",
                                                                   Path.cwd(), vault), cid=cid)
        return 3
    return _validate(vault, cid)


def _validate(vault: Vault, cid: str) -> int:
    from . import publication, validation
    folder = vault.root / cid
    masque, rapport, adj = folder / "masque.md", folder / "rapport.md", folder / "ajustements.txt"
    cwd = Path.cwd()
    state = vault.read_state(cid)
    if state.get("pending", 1) or not masque.is_file():
        say("pending", pending=state.get("pending", 1), path=sortie.neutral(adj, cwd, vault), cid=cid)
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
        try:
            target = publication.publish(vault, cid, data.decode("utf-8"), Path(state["destination"]))
        except OSError:
            say("publication_impossible")
            return 4
        say("publie", path=sortie.neutral(target, cwd, vault))
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
    vault = Vault()
    vault.ensure()
    chosen = args.chemin or _pick()
    if not chosen:
        say("aucun_fichier")
        return 4
    original = Path(chosen)
    if not original.is_file():
        say("introuvable")
        return 5
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
    if not (vault.root / args.id / "correspondance.json").is_file():
        say("sans_correspondance", cid=args.id)
        return 7
    try:
        target = reidentification.run(vault, args.id, Path(args.rapport))
    except (OSError, UnicodeDecodeError, ValueError):
        say("rapport_illisible")
        return 7
    say("reidentifie", path=sortie.neutral(target, Path.cwd(), vault))
    validation.default_open(target)
    return 0


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="legal-anonymiser", description="Pseudonymisation locale de contrats, sans réseau.")
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
    except (UnsupportedFormat, Unreadable):
        say("illisible")
        return 5
    except MissingDependency as exc:   # ModelMissing compris ; le message ne contient aucun chemin
        say("dependance", hint=str(exc))
        return 6
    except (RegistryCorrupted, AdjustmentsError) as exc:   # messages neutres par contrat
        print(str(exc))
        return 7
    except Exception:
        vault = Vault()
        try:
            say("erreur_interne", path=sortie.neutral(_trace(vault), Path.cwd(), vault))
        except Exception:
            print(sortie.MESSAGES["erreur_interne"].format(path=sortie.HIDDEN))
        return 7
