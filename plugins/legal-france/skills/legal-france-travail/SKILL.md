---
name: legal-france-travail
description: |
  Droit du travail français : contrat de travail, licenciement, démission,
  rupture conventionnelle, harcèlement, salaire, heures sup, congés, durée
  du travail, conventions collectives, prud'hommes, syndicats. À déclencher
  sur tout vocabulaire courant relatif au monde du travail salarié.

  Exemples de phrases déclencheuses :
  - "j'ai été viré, j'ai quoi comme indemnités ?"
  - "mon patron veut me licencier"
  - "ma boîte refuse de me payer mes heures sup"
  - "je veux démissionner, quel préavis ?"
  - "rupture conventionnelle, comment ça marche ?"
  - "mon collègue me harcèle"
  - "puis-je refuser une mutation ?"
  - "je veux saisir les prud'hommes"
  - "mon contrat est un CDD, peut-on le rompre ?"
  - "rédige-moi une lettre de démission"
  - "modèle de lettre de licenciement pour faute"

  Mots-clés : viré, licencié, licenciement, démission, rupture conventionnelle,
  CDI, CDD, intérim, période d'essai, prud'hommes, conseil de prud'hommes,
  patron, employeur, salarié, boîte, entreprise, prime, salaire, paye,
  fiche de paie, heures supplémentaires, congés, RTT, indemnités, indemnité
  de licenciement, préavis, faute grave, faute lourde, abandon de poste,
  harcèlement moral, harcèlement sexuel, discrimination, mobbing, mutation,
  reclassement, plan social, PSE, convention collective, syndicat, grève,
  DUP, CSE, élu du personnel, inaptitude, médecin du travail, accident
  du travail, maladie professionnelle, AT/MP, télétravail.
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

You handle French labour-law questions. Apply the methodology defined in
`skills/legal-france/methodology.md`.

## Required reads

First apply `skills/legal-france/references/qualification.md` and the
« Faits décisifs et pièces » section of this domain reference. Ask only
missing facts that change the analysis; preserve material hypotheses,
source versions and evidence gaps in every response format.

1. Read `references/travail.md` for applicable articles (Code du travail),
   key Cour de cassation soc. decisions, reforms (ordonnances Macron 2017,
   loi Travail 2016, loi Marché du travail 2022).
2. Read `skills/legal-france/references/codes-index.md` for cross-cutting
   article lookup.
3. Read `skills/legal-france/references/procedure.md` for prud'hommes
   delays, prescription, and competence rules.
4. Read `skills/legal-france/methodology.md` and select template by role.

## Specific verifications

For dismissal questions, always re-verify on Legifrance:
- Art. L. 1232-1 et s. C. trav. (licenciement pour motif personnel)
- Art. L. 1233-1 et s. C. trav. (licenciement économique)
- Art. L. 1234-9, L. 1234-1 (indemnités, préavis)
- Art. L. 1235-3 (barème Macron)
- Art. L. 1471-1 (délais de prescription des actions)

## Drafting

Available templates:
- `templates/lettre-licenciement.md` : pour motif personnel ou économique
- `templates/rupture-conventionnelle.md` : convention homologable par la
  DREETS
- `templates/lettre-demission.md` : avec calcul automatique du préavis selon
  convention collective indiquée
