---
type: mise-en-demeure-caution
domain: civil
short_description: Mise en demeure pour restitution du dépôt de garantie d'un bail d'habitation
qualification_fields:
  - regime_bail
  - residence_principale
  - date_bail
  - date_remise_cles
  - mode_remise_cles
  - conformite_etats_lieux
  - date_transmission_adresse
  - immeuble_collectif
  - regime_charges
  - loyer_mensuel_hors_charges
  - restitutions_effectuees
  - justificatifs_retenues
  - demarches_anterieures
required_fields:
  - locataire_nom
  - locataire_adresse_actuelle
  - bailleur_nom
  - bailleur_adresse
  - logement_adresse
  - montant_caution
  - date_versement
  - delai_execution
optional_fields:
  - date_etat_lieux_sortie
  - motif_retenue_invoque
  - montant_retenu
  - justification_locataire
  - pieces_jointes
derived_fields:
  - ville_locataire
  - date_du_jour
  - delai_restitution
  - date_limite_restitution
  - solde_principal_reclame
  - decompte_reclamation
  - majoration_reclamable
  - montant_majoration
applicable_law:
  - art. 22 loi n° 89-462 du 6 juillet 1989 (restitution, retenues et majoration)
  - art. 25-3 de la même loi (champ des locations meublées)
  - art. 7-1 de la même loi (prescription des actions dérivant du bail)
disclaimer_level: high
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`. Confirmer le
champ de la loi de 1989 : logement, usage, type et date du bail. Si le bail
relève d'un autre régime, adapter le fondement avant d'utiliser ce corps.

Distinguer la remise effective des clés de l'état des lieux et de la fin du
bail. Si la date de remise des clés est inconnue, les dates figurant sur un
état des lieux ne deviennent pas des dates candidates de remise : demander
ce que chaque date désigne et la preuve de remise. Aucun retard acquis,
échéance certaine ou nombre de périodes de majoration ne peut en être déduit.
Examiner les deux états des lieux, la preuve de remise, les loyers et
charges, les restitutions et les justificatifs de retenues. Pour un immeuble
collectif, vérifier une éventuelle provision justifiée et la régularisation
annuelle des comptes ; ne pas la présumer sur le seul mot « copropriété ».

Avant génération, établir le solde réclamé, le délai de restitution et son
échéance ; vérifier séparément la prescription avec les démarches déjà
faites. La nouvelle adresse et l'origine du retard doivent être examinées
avant toute majoration. Si ces points sont inconnus, la majoration reste à
confirmer et n'est pas présentée comme acquise.

## Questionnaire

1. Quel logement et quel bail sont concernés : vide/meublé/autre, résidence principale ou non, date du bail ? Pouvez-vous fournir le bail ou les clauses utiles ?
2. Quand, comment et à qui avez-vous effectivement remis les clés ? Quelle preuve avez-vous ? Quelle est, séparément, la date de l'état des lieux de sortie ?
3. Les états des lieux d'entrée et de sortie sont-ils conformes ? Fournir leurs passages utiles ; si l'un manque, préciser les circonstances.
4. Quel dépôt avez-vous versé et quand ? Quel est le loyer mensuel hors charges ? Quelles sommes ont déjà été restituées, et à quelles dates ?
5. Quelles retenues le bailleur invoque-t-il, pour quels montants et avec quels justificatifs ? Que contestez-vous précisément ?
6. Quand et comment avez-vous communiqué votre nouvelle adresse au bailleur ou à son mandataire ? A-t-il expliqué un retard par l'absence de cette adresse ?
7. Le logement est-il dans un immeuble collectif ? Les charges sont-elles au réel ou au forfait ? Une provision est-elle retenue, pour quel montant et avec quel arrêté des comptes ?
8. Quelles relances, réponses, démarches amiables ou judiciaires ont déjà eu lieu, et à quelles dates ? Quelles pièces sont disponibles ?
9. Après qualification : noms et adresses du locataire et du bailleur, adresse du logement, délai d'exécution demandé ? Des champs anonymisés sont possibles.

## Template

```
{{locataire_nom}}
{{locataire_adresse_actuelle}}

Lettre recommandée avec accusé de réception

{{bailleur_nom}}
{{bailleur_adresse}}

À {{ville_locataire}}, le {{date_du_jour}}

Objet : Mise en demeure de restituer le dépôt de garantie : {{logement_adresse}}

Madame, Monsieur,

Au titre de la location du logement indiqué ci-dessus, j'ai versé un dépôt de garantie de {{montant_caution}} euros le {{date_versement}}. Les clés vous ont été remises le {{date_remise_cles}}, selon les modalités suivantes : {{mode_remise_cles}}.
{{#if date_etat_lieux_sortie}}L'état des lieux de sortie a été établi le {{date_etat_lieux_sortie}}.{{/if}}

L'article 22 de la loi du 6 juillet 1989 prévoit un délai maximal de restitution de deux mois après remise des clés, réduit à un mois lorsque l'état des lieux de sortie est conforme à celui d'entrée. Les déductions autorisées doivent être justifiées.

Au regard des éléments exposés, le délai de restitution retenu est de {{delai_restitution}}, avec une échéance au {{date_limite_restitution}}.

{{decompte_reclamation}}

{{#if motif_retenue_invoque}}
Vous invoquez une retenue de {{montant_retenu}} euros pour {{motif_retenue_invoque}}. Je la conteste pour les raisons suivantes : {{justification_locataire}}.
{{/if}}

Je vous mets en demeure de me verser le solde principal réclamé de {{solde_principal_reclame}} euros dans les {{delai_execution}} jours suivant la réception de cette lettre.
{{#if majoration_reclamable}}
Je demande également {{montant_majoration}} euros au titre de la majoration prévue par l'article 22, selon le calcul détaillé ci-dessus, arrêté à la date de cette lettre.
{{/if}}

À défaut de règlement, je me réserve les démarches amiables et judiciaires adaptées pour obtenir restitution des sommes dues.

Veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{{locataire_nom}}
[Signature]
{{#if pieces_jointes}}
Pièces jointes :
{{pieces_jointes}}
{{/if}}
```

## Vérifications juridiques avant envoi

- Vérifier les art. 22, 25-3 et 7-1 dans la version applicable au bail et à l'action ; ne pas déduire la prescription de la seule date du déménagement.
- Retenues possibles même lorsque le délai est d'un mois ; provision justifiée en immeuble collectif limitée à 20 % du dépôt jusqu'à l'arrêté annuel, puis régularisation dans le mois suivant l'approbation définitive des comptes. Vérifier le régime des charges.
- Majoration : 10 % du loyer mensuel hors charges par période mensuelle de retard commencée. Examiner l'exception lorsque le défaut de nouvelle adresse est à l'origine du retard ; ne pas l'écarter automatiquement pour toute communication tardive.
- `solde_principal_reclame` exclut toute majoration. `decompte_reclamation` distingue dépôt, paiements, retenues admises/contestées, provision, principal, éventuelle majoration et total demandé ; éviter tout double comptage. Ne pas réclamer comme impayée une somme déjà rendue. `majoration_reclamable` n'est vrai qu'après vérification des conditions et des entrées du calcul.
- Si l'échéance de restitution n'est pas atteinte, proposer une demande de renseignements/restitution adaptée, sans présenter le bailleur comme déjà en retard.
- Pièces utiles : bail, états des lieux, preuve de versement, remise des clés, transmission de l'adresse, décompte et échanges. Ne lister comme jointes que celles effectivement disponibles.
- Vérifier la voie amiable préalable éventuelle, la compétence du juge des contentieux de la protection et les formalités de saisine avant de conseiller l'action. Le délai demandé dans la lettre ne remplace aucun délai légal.
- Sources contrôlées pour ces corrections le 2026-09-10 : [art. 22](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000028806696), [loi de 1989](https://www.legifrance.gouv.fr/loda/id/LEGITEXT000006069108), [fiche Service Public](https://www.service-public.gouv.fr/particuliers/vosdroits/F31269). Recontrôler à l'usage les points décisifs.
