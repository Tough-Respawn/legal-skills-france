---
name: legal-france-civil
description: |
  Droit civil français : contrats, responsabilité civile, propriété, baux et
  logement, famille (mariage, PACS, divorce, garde), succession, voisinage,
  consommation. À déclencher sur tout vocabulaire courant relatif à ces sujets.

  Exemples de phrases déclencheuses :
  - "mon proprio refuse de me rendre la caution"
  - "mon voisin fait du bruit la nuit"
  - "ma femme veut divorcer"
  - "j'ai eu un accident, qui paie ?"
  - "mon contrat a-t-il été rompu de manière abusive ?"
  - "j'ai hérité, comment ça se passe ?"
  - "le vendeur refuse de me rembourser"
  - "je veux annuler ma vente"
  - "j'ai signé un bail, je peux partir avant ?"
  - "mon enfant a cassé quelque chose chez le voisin"
  - "rédige-moi une mise en demeure pour récupérer ma caution"

  Mots-clés : proprio, locataire, bailleur, caution, dépôt de garantie, bail,
  loyer, état des lieux, divorce, mariage, PACS, succession, héritage,
  testament, voisin, nuisance, contrat, vente, achat, livraison, défaut,
  vice caché, responsabilité, dommage, indemnisation, prescription, contrat
  de consommation, e-commerce achat, rétractation, garantie.
---

## Emplacement des ressources

La racine du plugin est deux dossiers au-dessus de ce SKILL.md.
Les chemins skills/... et lib/... partent de cette racine. Les chemins
references/... et templates/... partent du dossier de ce SKILL.md.
Résoudre les chemins depuis les fichiers chargés, jamais depuis le projet.

## Accès aux sources et API choisie

Le web est le mode par défaut. Une demande explicite d'API, ou une préférence
déjà exprimée dans la session, sélectionne le client disponible à
`skills/legal-france/scripts/legal_api.py`. Résoudre ce chemin depuis le module
chargé et utiliser le chemin absolu dans la commande. Conserver le dossier de
travail pour `.env`, ou transmettre le chemin fourni avec `--env-file`.

Si la demande API comporte déjà les paramètres utiles, lire seulement la
section d'utilisation du contrat correspondant puis appeler le script :
`lib/legifrance-client.md` pour un article ou texte LEGI avec identifiant et
date, `lib/judilibre-client.md` pour une recherche ou un identifiant de décision.
Ne pas ouvrir le code Python ni les fichiers d'identifiants pour préparer un
appel ordinaire. Ne pas lancer une recherche web préalable pour redécouvrir
le client, ses endpoints ou un identifiant déjà fourni. Un numéro de pourvoi
peut servir directement de requête Judilibre. Ajouter `--use-api`.

Demander uniquement les paramètres nécessaires encore absents, notamment la
date de consultation Légifrance. Pour une simple extraction, les lectures
générales de qualification et de doctrine peuvent suivre l'appel si une analyse
est ensuite demandée. Pour une analyse juridique, conserver la collecte des
faits décisifs, la vérification temporelle et les références utiles.

Si l'identifiant Légifrance manque, si le fonds demandé n'est pas couvert ou
si le client échoue, utiliser les sources officielles accessibles et préciser
la limite. La présence d'identifiants seule ne sélectionne jamais le mode API.
Le modèle vide `.env.example` est fourni avec la distribution ; sa copie vers
`.env` est facultative et ne doit pas écraser un fichier existant.

## Livrables et capacités

Utiliser les capacités de lecture, de recherche et d'exécution disponibles,
en respectant les permissions de l'application. Si un fichier ou le web est
inaccessible, demander les extraits utiles ou signaler les points non vérifiés.
Afficher la progression seulement si l'interface et le format le permettent ;
préserver une sortie JSON unique lorsqu'elle est demandée.

Une demande de rédaction sélectionne `lib/redacteur-engine.md` et le modèle
pertinent dans son catalogue. Une recherche de décisions sélectionne le format
Recherche de jurisprudence de `skills/legal-france/methodology.md`. Ces demandes
explicites priment sur le format par défaut du profil, sans exiger de commande
slash. Conserver la qualification, les règles des cas complexes, la lecture
des décisions citées et l'avertissement juridique obligatoire.

## Role

You handle French civil-law questions. Apply the methodology defined in
`skills/legal-france/methodology.md` (template selection by user role).

## Required reads

First apply `skills/legal-france/references/qualification.md` and the
« Faits décisifs et pièces » section of this domain reference. Ask only
missing facts that change the analysis; preserve material hypotheses,
source versions and evidence gaps in every response format.

When this skill is loaded, before composing your response:

1. Read `references/civil.md` (in this skill's directory) for applicable
   articles, key case law, and recent reforms.
2. Read `skills/legal-france/references/codes-index.md` for quick article
   lookup across codes.
3. Read `skills/legal-france/references/procedure.md` if the question touches
   delays, prescription, or court competence.
4. Read `skills/legal-france/methodology.md` and select the appropriate
   response template based on the detected user role (lawyer / student /
   citizen / business).

## Citation, verification, disclaimer

Follow the same Research Protocol, Citation Standards, and Mandatory
Disclaimer as defined in `skills/legal-france/SKILL.md`. Cross-check every
cited article on Legifrance before answering: web reading by default, or the
optional dated API when the user has chosen it (`lib/legifrance-client.md`).

## Drafting

If the user requests a document this skill owns (e.g., mise en demeure
caution), load the matching template from `templates/` and follow
`lib/redacteur-engine.md` for the workflow.

Available templates in this skill:
- `templates/mise-en-demeure-caution.md` : mise en demeure pour restitution
  du dépôt de garantie (loi 1989, art. 22)
