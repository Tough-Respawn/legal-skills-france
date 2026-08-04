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
  - statut          # "ouvrier-employe" | "agent-maitrise-technicien" | "cadre"
optional_fields:
  - date_souhaitee_depart
  - dispense_preavis_souhaitee
applicable_law:
  - art. L. 1237-1 C. trav. (démission — existence et durée du préavis fixées par la loi, la convention collective ou les usages)
disclaimer_level: high
---

## Questionnaire

1. Vos nom et prénom complets ?
2. Votre adresse complète ?
3. Raison sociale + adresse de l'employeur ?
4. Intitulé exact de votre poste ?
5. Date d'envoi de la lettre (point de départ du préavis) ?
6. Convention collective applicable ?
7. Votre statut : **ouvrier/employé** | **agent de maîtrise/technicien** | **cadre** ?
8. *Optionnel :* date de départ effective souhaitée (si vous voulez négocier une dispense de préavis) ?
9. *Optionnel :* souhaitez-vous demander une dispense de préavis ? (oui/non — l'employeur n'est pas obligé d'accepter)

(Préavis indicatif selon convention collective : ouvrier 1 mois — agent de maîtrise 2 mois — cadre 3 mois. Vérifier sur la CC précise.)

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

Conformément à la convention collective {{convention_collective}} applicable, mon préavis est de {{duree_preavis}}. Il débutera à compter de la première présentation de la présente lettre, soit le {{date_debut_preavis}}, et prendra fin le {{date_fin_preavis}}.

{{#if dispense_preavis_souhaitee}}
Je sollicite, dans la mesure du possible, votre accord pour être dispensé(e) de tout ou partie de ce préavis, afin de pouvoir quitter mes fonctions le {{date_souhaitee_depart}}.

À défaut d'accord de votre part, je m'engage évidemment à exécuter mon préavis dans les conditions normales jusqu'à son terme.
{{else}}
Je m'engage à effectuer l'intégralité de mon préavis jusqu'au {{date_fin_preavis}}, en assurant la bonne transition de mes dossiers en cours.
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
- Envoyer en lettre recommandée avec accusé de réception OU remettre en main propre contre décharge datée et signée — pour preuve.
- En période d'essai : la rupture par le salarié est libre, avec un délai de prévenance de 48 heures, ramené à 24 heures si la présence dans l'entreprise est inférieure à 8 jours (art. L. 1221-26, jamais « 1 semaine » ; le L. 1221-25 cité auparavant régit le délai à la charge de l'EMPLOYEUR. Vérifié le 2026-08-05).
- Démission en CDD : ne pas utiliser ce modèle. Le CDD ne peut être rompu unilatéralement que dans des cas limitatifs (art. L. 1243-1).
- Une démission "sous le coup de la colère" peut être requalifiée en prise d'acte aux torts de l'employeur si elle est suivie de manifestations sans équivoque ; demander conseil avant envoi en cas de conflit.
