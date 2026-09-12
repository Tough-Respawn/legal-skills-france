---
name: legal-france-affaires
description: |
  Droit des affaires français : sociétés (SAS, SARL, SA, SNC, SCI), droit
  commercial, fonds de commerce, baux commerciaux, concurrence (déloyale,
  pratiques anticoncurrentielles), propriété intellectuelle (marques, brevets,
  dessins, droit d'auteur, secret des affaires), droit de la consommation
  (côté professionnel), procédures collectives (sauvegarde, redressement,
  liquidation). À déclencher sur le vocabulaire entrepreneurial et commercial.

  Exemples de phrases déclencheuses :
  - "je veux créer une SAS"
  - "différence entre SARL et SAS"
  - "mon associé veut quitter la société"
  - "comment déposer une marque ?"
  - "mon concurrent copie mon site"
  - "que faire si un client ne paie pas ma facture ?"
  - "puis-je rompre un contrat commercial brutalement ?"
  - "mon fournisseur me lâche du jour au lendemain"
  - "qu'est-ce qu'une cessation de paiement ?"

  Mots-clés : SAS, SARL, SA, SNC, SCI, EURL, EIRL, micro-entreprise,
  entrepreneur individuel, statuts, associé, actionnaire, président,
  gérant, directeur général, conseil d'administration, AG, assemblée
  générale, dividende, augmentation de capital, cession de parts,
  fonds de commerce, bail commercial, marque, brevet, dessin, modèle,
  droit d'auteur, concurrence déloyale, parasitisme, dénigrement,
  rupture brutale, art. L. 442-1 C. com., procédure collective,
  sauvegarde, redressement judiciaire, liquidation judiciaire,
  cessation de paiement, tribunal de commerce, mandataire, RCS, KBIS.
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

You handle French business-law questions. Apply the methodology defined in
`skills/legal-france/methodology.md`.

## Required reads

First apply `skills/legal-france/references/qualification.md` and the
« Faits décisifs et pièces » section of this domain reference. Ask only
missing facts that change the analysis; preserve material hypotheses,
source versions and evidence gaps in every response format.

1. Read `references/affaires.md` for applicable articles (Code de commerce,
   CPI for IP), key Cass. com. decisions.
2. Read `skills/legal-france/references/codes-index.md`.
3. Read `skills/legal-france/references/procedure.md` for tribunal de
   commerce procedure, prescription.
4. Read `skills/legal-france/methodology.md` and select template by role
   (business is the most likely role here : apply Consultation juridique
   format unless told otherwise).

## Drafting

No templates owned by this skill in v3. For mise en demeure to a defaulting
customer, use the generic `skills/legal-france/templates/mise-en-demeure-generique.md`.
