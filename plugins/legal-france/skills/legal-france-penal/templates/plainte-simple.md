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
  - prejudice_subi
optional_fields:
  - auteur_identifie
  - temoins
  - pieces_jointes
  - qualification_envisagee
applicable_law:
  - art. 40 et 40-1 C. proc. pén. (signalement au procureur)
  - art. 7, 8, 9 C. proc. pén. (prescription)
disclaimer_level: high
qualification_fields:
  - danger_actuel
  - age_au_moment_faits
  - chronologie_procedures
  - origine_preuves
derived_fields:
  - tribunal_competent_ville
  - tribunal_adresse
  - ville_plaignant
  - date_du_jour
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`.

Identifier d'abord les faits, la sécurité immédiate et le stade de la
procédure. Demander les dates/périodes connues, sans fabriquer une date
précise. Le manque de qualification pénale ou de preuve complète ne doit
pas empêcher le récit d'une plainte. Distinguer constat personnel,
soupçon, propos rapporté et pièce disponible.

Pièces utiles selon les faits : échanges, captures et fichiers d'origine,
certificat, facture, constat, témoignages ou récépissé antérieur. Examiner
la prescription et ses exceptions selon la qualification, l'âge et les
actes intervenus ; ne pas conclure à l'irrecevabilité sur le seul âge des faits.

## Questionnaire

1. Y a-t-il un danger actuel ou une mesure urgente ? Quels faits souhaitez-vous signaler, où, à quelles dates ou pendant quelle période ?
2. Qu'avez-vous personnellement constaté, que vous a-t-on rapporté et que soupçonnez-vous ? L'auteur est-il connu, sinon quels éléments descriptifs sont fiables ?
3. Quel âge avaient les personnes concernées au moment des faits, si cela influe sur leur qualification ou la prescription ?
4. Quels préjudices et quelles pièces/témoins sont disponibles ? Préciser l'origine des pièces et ce qu'elles permettent d'établir ; ne pas inventer un témoin manquant.
5. Une plainte, une main courante, une décision ou une autre démarche existe-t-elle déjà ? Quelles dates et quels récépissés/réponses ?
6. Avez-vous une qualification envisagée ? Elle peut rester indéterminée ; le récit suffit pour préparer ce courrier.
7. Après cette analyse : identité, coordonnées et informations utiles pour vous contacter, ou champs anonymisés pour le brouillon ?

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

Objet : Plainte simple contre {{#if auteur_identifie}}{{auteur_identifie}}{{else}}X{{/if}} {{#if qualification_envisagee}}pour {{qualification_envisagee}}{{else}}pour les faits exposés ci-dessous{{/if}}

Monsieur le Procureur de la République,

J'ai l'honneur de porter plainte contre {{#if auteur_identifie}}{{auteur_identifie}}{{else}}X{{/if}} pour les faits suivants{{#if qualification_envisagee}}, susceptibles de relever de la qualification de {{qualification_envisagee}}{{/if}}, sous réserve de la qualification retenue par vos services.

### Description des faits

Date ou période connue : {{date_faits}}. Lieu : {{lieu_faits}}.

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
- Identifier le procureur territorialement compétent selon les faits et les règles applicables ; le seul domicile de la victime ne suffit pas à présumer la compétence.
- Envoi recommandé : lettre recommandée avec accusé de réception, OU dépôt au commissariat / gendarmerie qui la transmettra au procureur (l'envoi direct est rapide mais le commissariat conserve une copie horodatée utile).
- Ne pas promettre une réponse du procureur sous trois mois. Une plainte avec constitution de partie civile peut être envisagée après un classement ou un délai, sous les conditions et exceptions de l’art. 85 CPP ; vérifier les actes et leur preuve avant de la recommander.
- Joindre **copies** des pièces, jamais d'originaux.
- Conserver une copie complète de la plainte signée.
- Si urgence ou danger immédiat → appeler le 17 et/ou se rendre au commissariat sans délai.

- Correction du délai de réponse et du questionnaire, contrôle ciblé le 2026-09-10 : https://www.service-public.gouv.fr/particuliers/vosdroits/F35505. Les délais pénaux doivent être recontrôlés pour la qualification et la version du CPP applicables.
