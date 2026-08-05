---
type: mise-en-demeure-caution
domain: civil
short_description: Mise en demeure du bailleur pour restitution du dépôt de garantie
required_fields:
  - locataire_nom
  - locataire_adresse_actuelle
  - bailleur_nom
  - bailleur_adresse
  - logement_adresse
  - date_entree
  - date_etat_lieux_sortie
  - montant_caution
  - date_versement
optional_fields:
  - motif_retenue_invoque
  - montant_retenu
applicable_law:
  - art. 22 loi n° 89-462 du 6 juillet 1989 (délais de restitution + pénalité 10% par mois)
disclaimer_level: high
---

## Questionnaire

1. Votre nom complet (locataire) ?
2. Votre adresse actuelle (après déménagement) ?
3. Nom complet du bailleur (personne physique ou SCI / agence) ?
4. Adresse complète du bailleur ?
5. Adresse exacte du logement loué ?
6. Date d'entrée dans le logement ?
7. Date de l'état des lieux de sortie ?
8. Montant du dépôt de garantie versé (en euros) ?
9. Date à laquelle vous avez versé le dépôt de garantie ?
10. *Si le bailleur invoque une retenue :* quel motif a-t-il évoqué ?
11. *Si retenue :* quel montant retient-il ?

(Le délai légal de restitution est de 1 mois si état des lieux conforme, 2 mois si retenue. Au-delà, pénalité de 10% du loyer mensuel par mois de retard.)

## Template

```
{{locataire_nom}}
{{locataire_adresse_actuelle}}

Lettre recommandée avec accusé de réception

{{bailleur_nom}}
{{bailleur_adresse}}

À {{ville_locataire}}, le {{date_du_jour}}

Objet : Mise en demeure de restituer le dépôt de garantie, logement {{logement_adresse}}

Madame, Monsieur,

J'ai occupé en qualité de locataire le logement situé {{logement_adresse}} du {{date_entree}} au {{date_etat_lieux_sortie}}, date à laquelle un état des lieux de sortie a été établi.

Lors de la signature du bail, j'ai versé un dépôt de garantie d'un montant de {{montant_caution}} euros, le {{date_versement}}.

{{#if motif_retenue_invoque}}
Vous avez invoqué une retenue de {{montant_retenu}} euros au motif suivant : {{motif_retenue_invoque}}. Cette retenue n'est pas justifiée à mes yeux car {{justification_locataire}} ; à tout le moins, vous n'avez pas restitué le solde dans les délais légaux.
{{else}}
À ce jour, vous ne m'avez restitué ni tout ni partie de cette somme.
{{/if}}

Conformément à l'article 22 de la loi n° 89-462 du 6 juillet 1989, le dépôt de garantie doit être restitué :
- dans un délai d'un mois suivant la remise des clés lorsque l'état des lieux de sortie est conforme à l'état des lieux d'entrée ;
- dans un délai de deux mois lorsque le bailleur entend retenir tout ou partie du dépôt sur des justificatifs.

À défaut de restitution dans ces délais, le solde dû majoré d'une somme égale à 10% du loyer mensuel en principal pour chaque mois commencé en retard est dû de plein droit au locataire.

Par la présente, je vous mets donc en demeure de me restituer la somme de {{montant_caution}} euros{{#if motif_retenue_invoque}} (ou à tout le moins le solde non contesté){{/if}}, augmentée des pénalités légales applicables, dans un délai de 8 jours à compter de la réception de la présente lettre, à l'adresse indiquée en tête.

À défaut, je serai contraint(e) de saisir la juridiction compétente (tribunal judiciaire : protection des locataires) afin d'obtenir le paiement de la somme due, des pénalités et de tout dommage et intérêt.

Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{{locataire_nom}}
[Signature]

Pièces jointes :
- Copie du bail
- Copie de l'état des lieux d'entrée
- Copie de l'état des lieux de sortie
- Copie du justificatif de versement du dépôt de garantie
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur de l'art. 22 loi n° 89-462 du 6 juillet 1989 (vérifier le pourcentage de pénalité : actuellement 10% du loyer mensuel par mois entamé).
- Vérifier que les délais 1 mois / 2 mois sont à jour.
- Envoyer obligatoirement en lettre recommandée avec accusé de réception.
- Joindre les pièces listées en pied du modèle.
- Si pas de réponse 8 jours après réception : saisir la commission départementale de conciliation OU le juge des contentieux de la protection (au sein du tribunal judiciaire), sans avocat obligatoire quel que soit le montant en matière de bail d'habitation (art. 761 CPC pour la dispense générale ≤ 10 000 €).
- Attention : la majoration de 10 % par mois de retard n'est pas due si le locataire n'a pas indiqué au bailleur l'adresse de son nouveau domicile (art. 22 loi 89-462, vérifié le 2026-08-05).
- Pour un bailleur professionnel (agence) : la mise en demeure peut faire courir des intérêts de retard plus élevés.
