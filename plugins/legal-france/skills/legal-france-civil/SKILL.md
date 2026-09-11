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
