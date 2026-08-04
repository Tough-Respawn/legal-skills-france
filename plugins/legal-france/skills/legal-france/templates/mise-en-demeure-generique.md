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
  - art. 1344 C. civ. (mise en demeure — modes)
  - art. 1344-1 C. civ. (intérêt moratoire — uniquement pour une obligation de somme d'argent)
disclaimer_level: high
---

## Questionnaire

1. Votre nom complet (expéditeur) ?
2. Votre adresse postale complète ?
3. Nom complet du destinataire ?
4. Adresse postale complète du destinataire ?
5. Objet précis du litige en une phrase (ex : "facture impayée du 12 mars", "non-restitution de matériel prêté", "non-respect d'un délai contractuel") ?
6. Quelle obligation demandez-vous (paiement, restitution, exécution, cessation d'agissements) ?
7. *Si paiement :* montant en euros (chiffres et lettres) ?
8. *Si contrat :* référence du contrat (numéro, date de signature) ?
9. Délai accordé pour exécuter (en général 8 à 15 jours après réception) ?
10. *Optionnel :* avez-vous eu des échanges précédents (mail, téléphone) ? Mentionner brièvement.

## Template

```
{{expediteur_nom}}
{{expediteur_adresse}}

Lettre recommandée avec accusé de réception

{{destinataire_nom}}
{{destinataire_adresse}}

À {{ville_expediteur}}, le {{date_du_jour}}

Objet : Mise en demeure — {{objet_du_litige}}

Madame, Monsieur,

{{#if precedents_echanges}}
Malgré mes précédentes démarches ({{precedents_echanges}}), aucune suite favorable n'a été donnée à ma demande.
{{/if}}

{{#if reference_contrat}}
Au titre du contrat {{reference_contrat}}, je vous demande de bien vouloir {{obligation_demandee}}{{#if montant}} pour un montant de {{montant}} euros{{/if}}.
{{else}}
Je vous demande de bien vouloir {{obligation_demandee}}{{#if montant}} pour un montant de {{montant}} euros{{/if}}.
{{/if}}

En conséquence, je vous mets en demeure, par la présente, d'exécuter cette obligation dans un délai de {{delai_execution}} jours à compter de la réception de la présente lettre, en application de l'article 1344 du Code civil{{#if montant}} et de l'article 1344-1 du même code{{/if}}.

À défaut, je me réserve le droit d'engager toute action judiciaire utile aux fins d'obtenir l'exécution de cette obligation, ainsi que la réparation du préjudice subi{{#if montant}}, y compris les intérêts moratoires au taux légal courant à compter de la présente mise en demeure (art. 1344-1 C. civ.){{/if}}.

Veuillez agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{{expediteur_nom}}
[Signature]
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur de l'art. 1344 C. civ. (et de l'art. 1344-1 si créance de somme d'argent).
- Références vérifiées sur Legifrance le 2026-08-04 : art. 1344 (https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032042162), art. 1344-1 (https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032035273 — vise exclusivement les obligations de somme d'argent).
- Envoyer par lettre recommandée avec accusé de réception (preuve juridique).
- Conserver une copie signée de la lettre.
- Délai recommandé : 8 jours minimum, 15 jours raisonnable. Si contractuel, respecter le délai prévu.
- Si dette commerciale et destinataire est professionnel : possibilité d'ajouter "intérêts de retard de plein droit à compter de cette mise en demeure" (art. L. 441-10 C. com.).
