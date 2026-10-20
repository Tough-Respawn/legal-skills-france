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
    "ner_absente": "Modèle de reconnaissance des noms absent : détection réduite, relisez avec attention.",
    "original_inside": "Attention : le fichier original est dans le dossier courant ; "
                       "ne le partagez pas avec le fichier masqué.",
    "pending": "{pending} point(s) à arbitrer dans {path}, puis lancez : legal-anonymiser relancer {cid}",
    "ouverts": "{ouverts} alerte(s) ou ambiguïté(s) restent ouvertes : voir {path}, "
               "puis lancez : legal-anonymiser relancer {cid}",
    "arguments": "Arguments invalides : voir `legal-anonymiser --help`.",
    "non_pret": "Contrat {cid} : des points restent ouverts ; traitez {path}, puis lancez : "
                "legal-anonymiser relancer {cid}",
    "modifie_depuis": "Contrat {cid} : fichiers du coffre modifiés depuis le dernier passage ; "
                      "relancez : legal-anonymiser relancer {cid}",
    "publie": "Publié : {name}",
    "rappel": "La validation porte sur le texte relu ; le risque résiduel listé reste visible pour le modèle.",
    "ajuster": "Ajustez {path}, puis lancez : legal-anonymiser relancer {cid}",
    "abandon": "Publication abandonnée : rien n'a été écrit hors du coffre.",
    "impossible": "validation impossible ici : lancez vous-même `legal-anonymiser valider {cid}` dans un terminal",
    "modifie": "fichier modifié pendant la relecture, relancez",
    "modifie_pendant_relecture": "Contrat {cid} : fichiers modifiés pendant la relecture, rien n'a été publié ; "
                                 "relancez : legal-anonymiser relancer {cid}",
    "publication_impossible": "Publication impossible : le dossier de destination n'est pas accessible en écriture.",
    "publication_refusee": "Publication refusée : le texte masqué ou sa table ne correspondent plus au dernier "
                           "passage, rien n'a été publié ; relancez : legal-anonymiser relancer {cid}",
    "aucun_fichier": "Aucun fichier choisi : rien n'a été traité.",
    "selecteur_indisponible": "Sélecteur de fichier indisponible : lancez `legal-anonymiser traiter <chemin>` vous-même.",
    "introuvable": "Fichier introuvable ou illisible.",
    "illisible": "Format non pris en charge ou fichier illisible.",
    "interrompu": "Interrompu : rien n'a été publié.",
    "dependance": "Dépendance manquante : {hint}",
    "ajustements_illisible": "Fichier d'ajustements illisible : {path}",
    "ajustements_ligne": "Ligne {line} mal formée dans {path} : corrigez-la puis relancez.",
    "id_invalide": "Identifiant de contrat invalide : 6 caractères hexadécimaux attendus.",
    "inconnu": "Contrat {cid} inconnu du coffre.",
    "reidentification_sans_publication": "Contrat {cid} : aucune publication ne correspond à ce rapport ; sa "
                                         "première ligne doit être celle du fichier publié contrat-{cid}.masque.md. "
                                         "Rien n'a été réidentifié.",
    "rapport_illisible": "Rapport illisible : vérifiez le chemin et l'encodage (UTF-8).",
    "reidentifie": "Rapport réidentifié : {path}",
    "erreur_interne": "Erreur interne : détails dans {path}",
    "verrou_installe": "Verrou Claude Code installé dans les réglages (version précédente du fichier, s'il existait, "
                       "sauvegardée en `settings.json.legal-france.bak` à côté). Redémarrez les sessions Claude Code "
                       "ouvertes.",
    "verrou_deja": "Verrou Claude Code déjà installé, à jour : réglages inchangés.",
    "verrou_retire": "Verrou Claude Code retiré des réglages (version précédente sauvegardée en "
                     "`settings.json.legal-france.bak` à côté).",
    "verrou_absent": "Aucun verrou Claude Code dans les réglages : rien à retirer, rien n'a été écrit.",
    "verrou_version": "Claude Code 2.1.295 ou plus récent est requis pour `onFailure: block` (version trouvée : "
                      "{version}). Verrou non installé.",
    "verrou_reglages_invalides": "Le fichier de réglages de Claude Code n'est pas un objet JSON valide (commentaires "
                                 "compris) : rien n'a été écrit. Corrigez-le, puis relancez.",
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
