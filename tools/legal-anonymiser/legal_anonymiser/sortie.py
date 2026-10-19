"""Sorties console : tous les textes affichés, chemins neutres, silence des bibliothèques tierces.

La console ne reçoit jamais un texte du document, le nom du fichier original, un chemin absolu ni le
message d'une exception inconnue. Les champs des messages sont des entiers, l'identifiant neutre du
contrat ou un chemin passé par `neutral`.
"""
from __future__ import annotations

import contextlib
import io
import logging
import warnings
from pathlib import Path
from typing import Iterator

from .coffre import Vault

HIDDEN = "[chemin masqué]"
MESSAGES = {
    "resume": "Contrat {cid} : {entities} entité(s) masquée(s), {alerts} alerte(s), {ambiguities} ambiguïté(s).",
    "original_inside": "Attention : le fichier original est dans le dossier courant ; "
                       "ne le partagez pas avec le fichier masqué.",
    "pending": "{pending} point(s) à arbitrer dans {path}, puis lancez : legal-anonymiser relancer {cid}",
    "publie": "Publié : {path}",
    "ajuster": "Ajustez {path}, puis lancez : legal-anonymiser relancer {cid}",
    "abandon": "Publication abandonnée : rien n'a été écrit hors du coffre.",
    "impossible": "validation impossible ici : lancez vous-même `legal-anonymiser valider {cid}` dans un terminal",
    "modifie": "fichier modifié pendant la relecture, relancez",
    "publication_impossible": "Publication impossible : le dossier de destination n'est pas accessible en écriture.",
    "aucun_fichier": "Aucun fichier choisi : rien n'a été traité.",
    "introuvable": "Fichier introuvable ou illisible.",
    "illisible": "Format non pris en charge ou fichier illisible.",
    "dependance": "Dépendance manquante : {hint}",
    "id_invalide": "Identifiant de contrat invalide : 6 caractères hexadécimaux attendus.",
    "inconnu": "Contrat {cid} inconnu du coffre.",
    "sans_correspondance": "Contrat {cid} sans table de correspondance : traitez-le d'abord.",
    "rapport_illisible": "Rapport illisible : vérifiez le chemin et l'encodage (UTF-8).",
    "reidentifie": "Rapport réidentifié : {path}",
    "erreur_interne": "Erreur interne : détails dans {path}",
}


def say(key: str, **fields: object) -> None:
    print(MESSAGES[key].format(**fields))


def neutral(path: Path, cwd: Path, vault: Vault) -> str:
    """`coffre/<id>/<nom>` sous le coffre, `./<relatif>` sous le dossier courant, sinon `[chemin masqué]`."""
    p = Path(path).resolve()
    for base, prefix in ((vault.root, "coffre/"), (Path(cwd).resolve(), "./")):
        try:
            return prefix + p.relative_to(base).as_posix()
        except ValueError:
            continue
    return HIDDEN


@contextlib.contextmanager
def quiet() -> Iterator[None]:
    """Sorties standard, avertissements et journaux des bibliothèques tierces absorbés."""
    sink = io.StringIO()
    level = logging.root.manager.disable
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink), warnings.catch_warnings():
        warnings.simplefilter("ignore")
        logging.disable(logging.CRITICAL)
        try:
            yield
        finally:
            logging.disable(level)
