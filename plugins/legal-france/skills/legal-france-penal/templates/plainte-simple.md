---
type: plainte-simple
domain: penal
short_description: Plainte simple adressée au procureur de la République
required_fields:
  - plaignant_nom
  - plaignant_date_naissance
  - plaignant_lieu_naissance
  - plaignant_nationalite
  - plaignant_profession
  - plaignant_adresse
  - date_faits
  - lieu_faits
  - description_faits
  - qualification_envisagee   # ex: vol, escroquerie, dégradation, harcèlement, etc.
  - prejudice_subi
optional_fields:
  - auteur_identifie
  - temoins
  - pieces_jointes
applicable_law:
  - art. 40 et 40-1 C. proc. pén. (signalement au procureur)
  - art. 7, 8, 9 C. proc. pén. (prescription)
disclaimer_level: high
---

## Questionnaire

1. Vos nom, prénoms, date de naissance, lieu de naissance, nationalité, profession ?
2. Votre adresse complète ?
3. Date(s) et heure(s) des faits ?
4. Lieu précis des faits (adresse, ville) ?
5. Description chronologique et factuelle des faits (qui, quoi, quand, comment) ?
6. Quelle qualification pénale envisagez-vous ? (vol, escroquerie, dégradation, harcèlement, menaces, abus de confiance, agression, etc. : si vous ne savez pas, dites "qualification à laisser au procureur").
7. Quel préjudice avez-vous subi (matériel, corporel, moral, financier) ?
8. *Optionnel :* l'auteur des faits est-il identifié ? (nom, ou éléments de description, sinon mentionner "auteur inconnu" / "plainte contre X").
9. *Optionnel :* y a-t-il des témoins ? (nom et coordonnées)
10. *Optionnel :* avez-vous des pièces à joindre ? (constat, factures, photos, captures d'écran, certificats médicaux, etc.)

## Template

```
{{plaignant_nom}}
Né(e) le {{plaignant_date_naissance}} à {{plaignant_lieu_naissance}}
Nationalité : {{plaignant_nationalite}}
Profession : {{plaignant_profession}}
Demeurant : {{plaignant_adresse}}

Lettre recommandée avec accusé de réception

Monsieur le Procureur de la République
Tribunal judiciaire de {{tribunal_competent_ville}}
{{tribunal_adresse}}

À {{ville_plaignant}}, le {{date_du_jour}}

Objet : Plainte simple contre {{#if auteur_identifie}}{{auteur_identifie}}{{else}}X{{/if}} pour {{qualification_envisagee}}

Monsieur le Procureur de la République,

J'ai l'honneur de porter plainte contre {{#if auteur_identifie}}{{auteur_identifie}}{{else}}X{{/if}} pour les faits suivants, susceptibles de constituer le délit (ou la contravention) de {{qualification_envisagee}}.

### Description des faits

Le {{date_faits}}, à {{lieu_faits}} :

{{description_faits}}

### Préjudice

À la suite de ces faits, j'ai subi le préjudice suivant : {{prejudice_subi}}.

{{#if temoins}}
### Témoins

Les personnes suivantes peuvent témoigner des faits ou de leurs conséquences :

{{temoins}}
{{/if}}

{{#if pieces_jointes}}
### Pièces jointes

Je joins à la présente :

{{pieces_jointes}}
{{/if}}

En conséquence, je sollicite l'ouverture d'une enquête et, le cas échéant, la mise en mouvement de l'action publique. Je me tiens à la disposition de vos services pour toute audition ou complément d'information.

Je me réserve par ailleurs le droit de me constituer partie civile, le cas échéant, en cas de classement sans suite ou pour obtenir réparation du préjudice subi.

Veuillez agréer, Monsieur le Procureur de la République, l'expression de ma haute considération.

{{plaignant_nom}}
[Signature]
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance les délais de prescription applicables à la qualification visée :
  - Contraventions : 1 an (art. 9 CPP).
  - Délits : 6 ans (art. 8 CPP).
  - Crimes : 20 ans (art. 7 CPP).
  - Délais spécifiques (mineurs, infractions sexuelles, terrorisme…) : vérifier.
- Identifier le **procureur de la République territorialement compétent** (tribunal judiciaire du lieu de l'infraction OU du domicile du suspect OU du domicile de la victime selon les cas).
- Envoi recommandé : lettre recommandée avec accusé de réception, OU dépôt au commissariat / gendarmerie qui la transmettra au procureur (l'envoi direct est rapide mais le commissariat conserve une copie horodatée utile).
- Le procureur a 3 mois pour répondre. En cas de classement sans suite ou silence, possibilité de plainte avec constitution de partie civile devant le doyen des juges d'instruction.
- Joindre **copies** des pièces, jamais d'originaux.
- Conserver une copie complète de la plainte signée.
- Si urgence ou danger immédiat → appeler le 17 et/ou se rendre au commissariat sans délai.
