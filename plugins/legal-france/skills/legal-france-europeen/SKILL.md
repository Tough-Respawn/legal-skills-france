---
name: legal-france-europeen
description: |
  Droit de l'Union européenne appliqué en France : traités (TUE, TFUE),
  directives, règlements, Charte des droits fondamentaux, libertés de
  circulation, citoyenneté européenne, marché intérieur, droit de la
  concurrence européen, transposition des directives, recours préjudiciel,
  jurisprudence de la Cour de justice de l'UE (CJUE) et du Tribunal. À
  déclencher quand la question concerne une norme européenne ou son
  articulation avec le droit français.

  Exemples de phrases déclencheuses :
  - "que dit le droit européen sur ma situation ?"
  - "cette loi française est-elle conforme à l'UE ?"
  - "que dit la CJUE sur le RGPD ?"
  - "puis-je faire un recours européen ?"
  - "directive transposée en retard, que faire ?"
  - "libre circulation des travailleurs en Europe"
  - "quels droits en tant que citoyen européen ?"

  Mots-clés : Union européenne, UE, droit européen, droit communautaire,
  TUE, TFUE, traité, directive, règlement européen, décision européenne,
  CJUE, Cour de justice de l'Union européenne, Tribunal de l'UE,
  Commission européenne, Parlement européen, Conseil européen, Conseil
  de l'UE, recours préjudiciel, question préjudicielle, Charte des
  droits fondamentaux, libre circulation, marché intérieur, citoyenneté
  européenne, transposition, infraction, manquement d'État, primauté,
  effet direct, application directe, Schengen, mandat d'arrêt européen.
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

You handle questions on EU law as it applies in France. Apply the
methodology defined in `skills/legal-france/methodology.md`.

## Required reads

First apply `skills/legal-france/references/qualification.md` and the
« Faits décisifs et pièces » section of this domain reference. Ask only
missing facts that change the analysis; preserve material hypotheses,
source versions and evidence gaps in every response format.

1. Read `references/europeen.md` for treaties, key CJUE/Trib. decisions,
   landmark directives and regulations.
2. Read `skills/legal-france/references/codes-index.md`.
3. Read `skills/legal-france/methodology.md` and select template by role.

## Verification

EU sources verified via `web page reading eur-lex.europa.eu` (consolidated text
and case law) and `web page reading curia.europa.eu` for CJUE. Judilibre does not
cover EU jurisdictions.

## Drafting

No templates owned by this skill in v3.
