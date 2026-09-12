---
type: contestation-amende
domain: penal
short_description: Contestation d'amende forfaitaire auprès de l'officier du ministère public (OMP)
required_fields:
  - contrevenant_nom
  - contrevenant_adresse
  - numero_avis_contravention
  - date_constatation
  - lieu_constatation
  - nature_infraction
  - motif_contestation
optional_fields:
  - vehicule_immatriculation
  - vehicule_proprietaire
  - pieces_jointes
applicable_law:
  - art. 529-2 C. proc. pén. (requête en exonération)
  - art. 529-10 C. proc. pén. (formalités et consignation selon le cas)
  - art. 530 C. proc. pén. (réclamation contre une amende majorée)
  - art. 530-2-1 C. proc. pén. (avis adressé à l’étranger, selon le cas)
disclaimer_level: high
qualification_fields:
  - type_avis
  - date_envoi_avis
  - date_notification_avis
  - mode_notification
  - paiement_ou_consignation
  - qualite_destinataire_avis
  - pays_envoi
  - demarches_anterieures
derived_fields:
  - adresse_omp_indique_sur_avis
  - ville_contrevenant
  - date_du_jour
  - situation_vehicule
  - nature_recours
  - fondement_recours
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`.

Lire l'avis complet et ses voies de contestation. Distinguer amende
forfaitaire contraventionnelle initiale/majorée, amende délictuelle, forfait
de post-stationnement, ordonnance pénale et jugement. Ce corps couvre les
deux premières branches contraventionnelles seulement ; adapter la voie
avant de rédiger pour les autres actes.

Vérifier date d'envoi et mode de notification, éventuel paiement ou
consignation, lieu d'envoi et démarches antérieures. Ne pas transformer un
avis initial en avis majoré par simple déduction de son ancienneté. Pièces :
avis/formulaire complets, notification et pièces propres au motif (cession,
vol, identité du conducteur…). Identifier les formalités de consignation
avant de présenter la contestation comme recevable.

**Avant le corps de réclamation** : si la nature précise de l'infraction,
la qualité du destinataire de l'avis ou l'état des paiements/consignations
manquent, limiter la première réponse au bilan et aux questions ciblées.
Demander notamment si une somme a déjà été payée ou consignée, avant toute
instruction d'en consigner une. Recevoir un avis n'établit pas que l'on est
personnellement titulaire du certificat d'immatriculation. Ne pas ajouter
cette qualité au corps neutre ci-dessous. Une consignation à effectuer et
son justificatif à obtenir restent dans les démarches préparatoires ;
aucune variante ne doit les présenter comme déjà accomplis ou joints.

## Questionnaire

1. Pouvez-vous fournir l'avis complet, son formulaire et les voies/délais indiqués, en masquant les données inutiles ? Quel type d'acte avez-vous reçu ?
2. Quelles dates d'envoi et de réception/notification, quel mode d'envoi, en France ou à l'étranger ? Distinguer ces dates de la constatation des faits.
3. Avez-vous payé l'amende, consigné une somme ou déjà contesté ? Quand et avec quelle preuve ?
4. Quels faits contestez-vous exactement, à quel lieu et quelle date ? À quel titre êtes-vous destinataire de l’avis (titulaire, représentant d’une société, personne désignée…) ? Pour un véhicule, quelle situation au moment des faits (cession, prêt, vol…) ?
5. Quelles pièces sont réellement disponibles pour ce motif et quelles pièces/formalités l'avis demande-t-il ?
6. Après qualification : numéro d'avis, identité/adresse du destinataire, véhicule et adresse exacte de l'OMP figurant sur l'acte, ou champs anonymisés ?

## Template

```
{{contrevenant_nom}}
{{contrevenant_adresse}}

Lettre recommandée avec accusé de réception

Officier du Ministère Public
{{adresse_omp_indique_sur_avis}}

À {{ville_contrevenant}}, le {{date_du_jour}}

Objet : {{nature_recours}} : avis n° {{numero_avis_contravention}}

Monsieur l'Officier du Ministère Public,

J'ai l'honneur de contester l'avis de contravention référencé ci-dessus, qui m'a été adressé concernant les faits suivants :

- **Date de constatation** : {{date_constatation}}
- **Lieu** : {{lieu_constatation}}
- **Nature de l'infraction** : {{nature_infraction}}
{{#if vehicule_immatriculation}}- **Véhicule concerné** : immatriculation {{vehicule_immatriculation}}{{/if}}

### Motif de la contestation

{{motif_contestation}}

{{#if vehicule_proprietaire}}
Au moment des faits, le véhicule était {{situation_vehicule}} (au nom de {{vehicule_proprietaire}}).
{{/if}}

{{#if pieces_jointes}}
### Pièces jointes

{{pieces_jointes}}
{{/if}}

{{fondement_recours}}

Je vous prie de bien vouloir m'adresser votre décision motivée par retour de courrier, et de me notifier toute convocation devant le tribunal de police si vous décidiez de maintenir la poursuite.

Veuillez agréer, Monsieur l'Officier du Ministère Public, l'expression de ma considération distinguée.

{{contrevenant_nom}}
[Signature]
```

## Vérifications juridiques avant envoi

- `nature_recours` distingue requête en exonération et réclamation contre l'amende majorée. `fondement_recours` formule la demande sur le texte pertinent ; ne pas affirmer « dans le délai » avant contrôle.
- Avis initial : examiner les 45 jours et leur point de départ selon l'art. 529-2. Avis majoré : vérifier l'art. 530 (30 jours en principe, cas routier LRAR à trois mois et exceptions de connaissance). Vérifier les prolongations applicables aux envois à l'étranger. Ne pas confondre paiement et consignation.
- Vérifier sur l'avis et le site officiel le canal, le destinataire, les formulaires, les originaux requis et la consignation/exemption propre au motif. Pour la voie postale concernée, suivre l'exigence de recommandé et garder copie du dossier et preuve d'envoi.
- Si type d'acte, notification ou paiement sont inconnus, demander ces éléments avant de conclure sur la recevabilité. Conserver les motifs rapportés sans inventer une preuve de cession ou un autre conducteur.
- Une contestation peut conduire à des poursuites devant le tribunal de police ; ne pas promettre annulation ou absence de conséquence.
- Sources contrôlées pour ces distinctions le 2026-09-10 : https://www.antai.gouv.fr/particulier/designation-ou-contestation/ et les articles du CPP liés par cette page. Vérifier directement leur version à l'usage ; les indications générales du site ne remplacent pas l'avis et les exceptions légales.
