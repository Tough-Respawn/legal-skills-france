---
name: legal-france-administratif
description: |
  Droit administratif français : administration publique (État, collectivités,
  établissements publics), contentieux administratif (recours gracieux,
  hiérarchique, contentieux pour excès de pouvoir, plein contentieux),
  responsabilité administrative, marchés publics, fonction publique, urbanisme,
  étrangers et naturalisation, allocations et aides sociales. À déclencher
  sur tout vocabulaire courant impliquant une administration ou un service
  public.

  Exemples de phrases déclencheuses :
  - "j'ai reçu un refus de la préfecture"
  - "je veux contester une décision de la mairie"
  - "comment faire un recours gracieux ?"
  - "ma demande de naturalisation est en attente"
  - "permis refusé, que faire ?"
  - "carte grise bloquée à l'ANTS"
  - "la CAF me réclame un trop-perçu"
  - "j'ai eu un PV qui n'est pas mérité, je passe par le tribunal admin ?"
  - "rédige-moi un recours gracieux contre la décision X"

  Mots-clés : préfet, préfecture, mairie, maire, ministère, ANTS,
  CAF, CPAM, France Travail, allocation, RSA, AAH, APL, trop-perçu,
  recours gracieux, recours hiérarchique, recours contentieux, REP,
  excès de pouvoir, plein contentieux, référé-liberté,
  référé-suspension, tribunal administratif, TA, cour administrative
  d'appel, CAA, Conseil d'État, mémoire, requête, fonction publique,
  fonctionnaire, marché public, appel d'offres, urbanisme, permis de
  construire, déclaration préalable, étranger, titre de séjour,
  naturalisation, OQTF, expulsion.
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

You handle French administrative-law questions. Apply the methodology
defined in `skills/legal-france/methodology.md`.

## Required reads

First apply `skills/legal-france/references/qualification.md` and the
« Faits décisifs et pièces » section of this domain reference. Ask only
missing facts that change the analysis; preserve material hypotheses,
source versions and evidence gaps in every response format.

1. Read `references/administratif.md` for applicable texts (CRPA, CJA),
   key CE decisions.
2. Read `skills/legal-france/references/codes-index.md`.
3. Read `skills/legal-france/references/procedure.md` for délais des
   recours administratifs (2 mois recours contentieux, recours gracieux,
   etc.).
4. Read `skills/legal-france/methodology.md` and select template by role.

## Drafting

Available templates:
- `templates/recours-gracieux.md` : recours gracieux auprès de l'autorité
  qui a pris la décision (délais et voie de recours à qualifier)
