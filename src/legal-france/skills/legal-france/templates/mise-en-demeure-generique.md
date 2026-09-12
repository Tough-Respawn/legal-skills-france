---
type: mise-en-demeure-generique
domain: meta
short_description: Mise en demeure paramétrable (créance impayée, exécution d'obligation, restitution)
required_fields:
  - expediteur_nom
  - expediteur_adresse
  - destinataire_nom
  - destinataire_adresse
  - objet_du_litige
  - obligation_demandee
  - delai_execution
optional_fields:
  - montant
  - reference_contrat
  - precedents_echanges
applicable_law:
  - art. 1344 C. civ. (mise en demeure, modes)
  - art. 1344-1 C. civ. (intérêt moratoire, uniquement pour une obligation de somme d'argent)
disclaimer_level: high
qualification_fields:
  - qualite_parties
  - fondement_obligation
  - date_exigibilite
  - etat_execution
  - paiements_recus
  - procedure_collective
  - pieces_disponibles
derived_fields:
  - ville_expediteur
  - date_du_jour
  - interets_civils
  - penalites_commerciales
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`.

Établir l'obligation réclamée, son fondement, son exigibilité et le solde
éventuel. Demander contrat, facture/commande, preuve de prestation ou de
remise, paiements et échanges. Identifier une contestation et une procédure
collective éventuelle avant de proposer le recouvrement individuel.
Le délai laissé dans la lettre n'est ni un délai légal universel ni un moyen
présumé d'interrompre une prescription. Si l'obligation n'est pas encore
exigible, adapter la demande sans affirmer un retard.

## Questionnaire

1. Quel résultat demandez-vous, contre qui et à quel titre ? Les parties agissent-elles comme particuliers, consommateurs ou professionnels ?
2. Quelle obligation et quel fondement : contrat, facture, restitution ou autre ? Quand devait-elle être exécutée et quelles pièces l'établissent ?
3. Qu'avez-vous exécuté de votre côté ? Quels paiements ou restitutions ont déjà eu lieu, et que reste-t-il exactement à réclamer ?
4. Quelle contestation, relance, réponse ou procédure existe déjà, avec quelles dates ? Une procédure collective du débiteur est-elle connue ?
5. Quel délai d'exécution souhaitez-vous accorder, sous réserve des stipulations et règles applicables ?
6. Après qualification : objet du courrier, référence du contrat si utile, noms et adresses des parties, ou champs anonymisés ?

## Template

```
{{expediteur_nom}}
{{expediteur_adresse}}

Lettre recommandée avec accusé de réception

{{destinataire_nom}}
{{destinataire_adresse}}

À {{ville_expediteur}}, le {{date_du_jour}}

Objet : Mise en demeure, {{objet_du_litige}}

Madame, Monsieur,

{{#if precedents_echanges}}
Malgré mes précédentes démarches ({{precedents_echanges}}), aucune suite favorable n'a été donnée à ma demande.
{{/if}}

{{#if reference_contrat}}
Au titre du contrat {{reference_contrat}}, je vous demande de bien vouloir {{obligation_demandee}}{{#if montant}} pour un montant de {{montant}} euros{{/if}}.
{{else}}
Je vous demande de bien vouloir {{obligation_demandee}}{{#if montant}} pour un montant de {{montant}} euros{{/if}}.
{{/if}}

En conséquence, je vous mets en demeure, par la présente, d'exécuter cette obligation dans un délai de {{delai_execution}} jours à compter de la réception de la présente lettre, en application de l'article 1344 du Code civil{{#if interets_civils}} et de l'article 1344-1 du même code{{/if}}.

À défaut, je me réserve le droit d'engager toute action judiciaire utile aux fins d'obtenir l'exécution de cette obligation, ainsi que la réparation du préjudice subi{{#if interets_civils}}, y compris les intérêts moratoires au taux légal courant à compter de la présente mise en demeure (art. 1344-1 C. civ.){{/if}}.

{{#if penalites_commerciales}}
{{penalites_commerciales}}
{{/if}}

Veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{{expediteur_nom}}
[Signature]
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur de l'art. 1344 C. civ. (et de l'art. 1344-1 si créance de somme d'argent).
- Références vérifiées sur Legifrance le 2026-08-04 : art. 1344 (https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032042162), art. 1344-1 (https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032035273, vise exclusivement les obligations de somme d'argent).
- Envoyer par lettre recommandée avec accusé de réception (preuve juridique).
- Conserver une copie signée de la lettre.
- Justifier le délai demandé selon la situation et le contrat ; ne pas présenter huit jours comme un minimum légal général. Vérifier séparément les prescriptions et leurs causes d’interruption.
- Si dette commerciale et destinataire est professionnel : les pénalités de retard de l'art. L. 441-10 C. com. sont exigibles de plein droit dès le jour suivant la date d'échéance, SANS mise en demeure nécessaire (taux BCE + 10 points, plancher 3 fois le taux légal, indemnité forfaitaire de 40 €) ; les rappeler dans la lettre est utile mais elles ne partent pas de la mise en demeure (vérifié le 2026-08-05).

- `montant` désigne le solde réclamé après paiements. `interets_civils` suppose une créance de somme d’argent relevant de ce régime, sans le présumer quand la qualité des parties est inconnue ; `penalites_commerciales` nécessite les conditions, taux et dates du régime commercial vérifiés, sans cumul automatique. Si le régime n’est pas établi, laisser la clause à déterminer ; présenter les régimes comme des alternatives à vérifier, pas comme des pénalités « en plus » par défaut. Contrôle documentaire du questionnaire le 2026-09-10 ; recontrôler les sources ci-dessus à l’usage.
