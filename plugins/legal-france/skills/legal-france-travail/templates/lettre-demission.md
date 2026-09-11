---
type: lettre-demission
domain: travail
short_description: Lettre de démission d'un CDI (avec calcul du préavis)
required_fields:
  - salarie_nom
  - salarie_adresse
  - employeur_nom
  - employeur_adresse
  - poste
  - date_envoi
  - convention_collective
  - statut
optional_fields:
  - date_souhaitee_depart
  - dispense_preavis_souhaitee
applicable_law:
  - art. L. 1237-1 C. trav. (démission, existence et durée du préavis fixées par la loi, la convention collective ou les usages)
disclaimer_level: high
qualification_fields:
  - type_contrat
  - periode_essai
  - volonte_demission
  - date_notification
  - mode_notification
  - anciennete
  - evenements_preavis
  - pieces_disponibles
derived_fields:
  - ville_salarie
  - dispositions_preavis
  - date_fin_preavis
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`.

Confirmer un CDI hors période d'essai et la volonté claire de démissionner.
En CDD, période d'essai, emploi public ou situation ambiguë, examiner le
régime adapté avant d'utiliser ce modèle. Demander contrat, avenants,
convention/accord et classification, ainsi que le mode de notification.
Distinguer demande de dispense et accord effectivement donné.

Le début du préavis dépend de la notification, pas du seul envoi. Une
présentation postale future ne permet pas de fixer une fin certaine.
Vérifier durée, computation, événements affectant le préavis et clauses
applicables ; aucune grille universelle « 1/2/3 mois » n'est présumée.

## Questionnaire

1. Quel contrat, quelle situation (hors essai ou non) et quelle volonté de rupture ? La lettre a-t-elle déjà été envoyée ou la démission notifiée autrement ?
2. Quelle convention collective (IDCC et champ), classification, ancienneté et clause de préavis ? Fournir les extraits utiles.
3. Quel mode de notification et quelle date de présentation/remise ou autre notification établie ? Distinguer cette date de l'envoi prévu.
4. Quels congés ou événements peuvent affecter le préavis ? Souhaitez-vous une dispense, pour quelle date, et l'employeur a-t-il déjà donné son accord ?
5. Après qualification : nom, adresse, employeur, poste et date de lettre, ou champs anonymisés ?

## Template

```
{{salarie_nom}}
{{salarie_adresse}}

Lettre recommandée avec accusé de réception
(ou remise en main propre contre décharge)

{{employeur_nom}}
{{employeur_adresse}}

À {{ville_salarie}}, le {{date_envoi}}

Objet : Démission

Madame, Monsieur,

Par la présente, je vous informe de ma décision de mettre un terme à mon contrat de travail à durée indéterminée, en qualité de {{poste}}, que j'occupe au sein de votre entreprise.

{{dispositions_preavis}}

{{#if dispense_preavis_souhaitee}}
Je sollicite, dans la mesure du possible, votre accord pour être dispensé(e) de tout ou partie de ce préavis, afin de pouvoir quitter mes fonctions le {{date_souhaitee_depart}}.

À défaut d'accord de votre part, je m'engage évidemment à exécuter mon préavis dans les conditions normales jusqu'à son terme.
{{else}}
J'effectuerai le préavis applicable, sous réserve d'un accord de dispense ou d'un événement modifiant son terme.
{{/if}}

Je vous remercie de bien vouloir me transmettre, à la fin de ma période de préavis, les documents légaux suivants :
- mon certificat de travail,
- mon attestation France Travail,
- mon reçu pour solde de tout compte,
- ainsi que le règlement de mes congés payés acquis non pris.

Je profite de cette occasion pour vous remercier de la confiance que vous m'avez accordée durant ces années.

Veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{{salarie_nom}}
[Signature]
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur de l'art. L. 1237-1 du Code du travail (référence vérifiée le 2026-08-04 : https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901174).
- Consulter la convention collective applicable pour le préavis exact (variable selon statut et ancienneté). Source d'autorité : Legifrance ou le portail de la branche.
- Aucun motif n'est exigé : la démission est un droit (sauf preuve d'abus).
- Envoyer en lettre recommandée avec accusé de réception OU remettre en main propre contre décharge datée et signée : pour preuve.
- En période d'essai : la rupture par le salarié est libre, avec un délai de prévenance de 48 heures, ramené à 24 heures si la présence dans l'entreprise est inférieure à 8 jours (art. L. 1221-26, jamais « 1 semaine » ; le L. 1221-25 cité auparavant régit le délai à la charge de l'EMPLOYEUR. Vérifié le 2026-08-05).
- Démission en CDD : ne pas utiliser ce modèle. Le CDD ne peut être rompu unilatéralement que dans des cas limitatifs (art. L. 1243-1).
- En cas de volonté ambiguë, de pression ou de griefs contre l’employeur, examiner la qualification de la rupture avant de rédiger une démission sans réserve.

- `dispositions_preavis` expose la durée et son fondement vérifié, le mode et l’événement de départ ; une date inconnue reste à confirmer. `date_fin_preavis` n’est calculée qu’avec les éléments nécessaires, en précisant le dernier jour inclus. Source sur le départ du préavis, consultée le 2026-09-10 : https://www.service-public.gouv.fr/particuliers/vosdroits/F2883.
