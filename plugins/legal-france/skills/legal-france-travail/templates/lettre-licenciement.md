---
type: lettre-licenciement
domain: travail
short_description: Lettre de notification de licenciement (motif personnel ou économique)
required_fields:
  - employeur_nom
  - employeur_adresse
  - salarie_nom
  - salarie_adresse
  - salarie_poste
  - date_embauche
  - motif_type           # "personnel" | "economique"
  - motif_detaille
  - date_entretien_prealable
  - date_envoi
optional_fields:
  - convention_collective
  - faits_reproches      # only if motif_type=personnel
  - difficultes_economiques  # only if motif_type=economique
applicable_law:
  - art. L. 1232-1 à L. 1232-6 C. trav. (procédure motif personnel)
  - art. L. 1233-1 à L. 1233-16 C. trav. (procédure motif économique)
  - art. L. 1234-1 (préavis)
  - art. L. 1234-9 (indemnité légale)
  - art. L. 1235-3 (barème Macron, dommages-intérêts en cas de licenciement sans cause réelle et sérieuse)
disclaimer_level: high
---

## Questionnaire

1. Nom et raison sociale de l'employeur ?
2. Adresse complète du siège social ?
3. Nom complet du salarié ?
4. Adresse complète du salarié ?
5. Intitulé exact du poste occupé ?
6. Date d'embauche (début du contrat) ?
7. Motif de licenciement : **personnel** (faute, insuffisance, inaptitude…) ou **économique** (difficultés, mutation technologique, cessation d'activité…) ?
8. *Si motif personnel :* faits précis reprochés (dates, circonstances, témoins ou éléments objectifs) ?
9. *Si motif économique :* nature exacte des difficultés économiques + recherche de reclassement effectuée (oui/non, détail) ?
10. Date de l'entretien préalable (obligatoire, au moins 5 jours ouvrables avant la lettre) ?
11. Convention collective applicable ?
12. Date prévue d'envoi de la lettre ?

(Délai légal : la lettre doit être envoyée au plus tôt **2 jours ouvrables** après l'entretien préalable ; le plafond d'un mois ne vaut que pour les licenciements DISCIPLINAIRES, art. L. 1332-2 ; pour un motif personnel non disciplinaire, ex. insuffisance professionnelle, seul un délai raisonnable s'applique. Vérifié le 2026-08-05.)

## Template

```
{{employeur_nom}}
{{employeur_adresse}}

Lettre recommandée avec accusé de réception

{{salarie_nom}}
{{salarie_adresse}}

À {{ville_employeur}}, le {{date_envoi}}

Objet : Notification de licenciement {{#if motif_type=="personnel"}}pour motif personnel{{else}}pour motif économique{{/if}}

{{salarie_nom_formule_politesse}},

Faisant suite à l'entretien préalable qui s'est tenu le {{date_entretien_prealable}}, auquel vous avez été régulièrement convoqué(e) par lettre recommandée du [date envoi convocation], nous avons le regret de vous notifier votre licenciement{{#if motif_type=="personnel"}} pour motif personnel{{else}} pour motif économique{{/if}}.

{{#if motif_type=="personnel"}}
Les faits reprochés, qui constituent une cause réelle et sérieuse de licenciement, sont les suivants :

{{faits_reproches}}

Nous considérons que ces faits, par leur nature et leurs conséquences, rendent impossible la poursuite de la relation de travail.
{{else}}
Le présent licenciement repose sur les motifs économiques suivants :

{{difficultes_economiques}}

Nous avons examiné toutes les possibilités de reclassement au sein de l'entreprise et du groupe. {{recherche_reclassement_detail}}.
{{/if}}

Votre préavis, d'une durée de {{duree_preavis}} prévue par {{#if convention_collective}}la convention collective {{convention_collective}}{{else}}les dispositions légales{{/if}}, débutera à la première présentation de la présente lettre et prendra fin le {{date_fin_preavis}}.

À l'issue du préavis, nous vous remettrons :
- votre certificat de travail,
- votre attestation Pôle emploi (France Travail),
- votre reçu pour solde de tout compte,
- ainsi que le règlement de votre indemnité légale (ou conventionnelle) de licenciement, calculée conformément aux articles L. 1234-9 et suivants du Code du travail.

{{#if motif_type=="economique"}}
Nous vous informons que vous bénéficiez de la priorité de réembauche prévue à l'article L. 1233-45 du Code du travail pendant un délai d'un an à compter de la date de rupture de votre contrat, À CONDITION d'en faire la demande au cours de ce même délai (mention exigée par L. 1233-16). Vous pouvez également solliciter un contrat de sécurisation professionnelle (CSP) le cas échéant.
{{/if}}

Nous vous prions d'agréer, {{salarie_nom_formule_politesse}}, l'expression de nos salutations distinguées.

{{employeur_signataire_nom}}
{{employeur_signataire_fonction}}
[Signature]
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur des articles L. 1232-6, L. 1233-15, L. 1234-1, L. 1234-9, L. 1235-3 du Code du travail.
- Vérifier la durée légale **et** conventionnelle du préavis.
- Confirmer le calcul de l'indemnité légale : 1/4 de mois par année pour les 10 premières années, 1/3 ensuite (art. R. 1234-2).
- Pour motif économique : avoir notifié à la DREETS / fait les consultations obligatoires (CSE).
- Délais à respecter :
  - Convocation à entretien préalable au moins 5 jours ouvrables avant l'entretien.
  - Lettre envoyée au plus tôt **2 jours ouvrables** après l'entretien (motif personnel) ou **7 jours ouvrables** (motif économique individuel, portés à **15 jours ouvrables** pour un membre du personnel d'encadrement, art. L. 1233-15 ; vérifié le 2026-08-05).
- Risque : un licenciement sans cause réelle et sérieuse expose à des dommages-intérêts plafonnés selon l'art. L. 1235-3 (barème Macron, dépend de l'ancienneté et de l'effectif).
- En cas de doute sérieux sur la justification : consulter un avocat ou un syndicat **avant** envoi.
