# Scénarios de rédaction : legal-france 3.1

Ces scénarios manuels décrivent les points à examiner par modèle. Utiliser
une conversation neuve et des identités fictives. Avec le plugin actuel,
l'invocation explicite est `/rediger <type>`. Les prompts automatisés et leur
runner restent dans le dossier local `evals/`, exclu du dépôt public.

## Critères communs

- Charger le modèle et le protocole de qualification ; réutiliser les faits
  fournis, demander seulement les inconnues décisives et accepter l'anonymisation.
- Distinguer faits rapportés, pièces réellement lues, contradictions et inconnues.
- Vérifier la règle et sa version temporelle avant un résultat opérationnel.
  Montrer le point de départ et le calcul d'un délai effectivement déterminable.
- Ne pas inventer un fait ou une procédure pour terminer un acte. Une réponse
  conditionnelle ou un brouillon incomplet est adapté aux scénarios incomplets.
- Pour un document produit : champs/branches cohérents, pièces réellement
  disponibles, checklist et deux avertissements prévus par le moteur.
- Examiner le sens et les traces : un mot-clé présent, un lint réussi ou un
  appel d'outil ne suffisent pas à un PASS juridique.

## Cas par modèle

| ID | Modèle | Point décisif |
|---|---|---|
| R1 | `mise-en-demeure-generique` | Demander échéance, solde après paiement et qualité des parties. |
| R2 | `attestation-honneur` | Clarifier la période réellement attestable ou laisser un champ explicite. |
| R3 | `mise-en-demeure-caution` | Demander date/mode/preuve de remise des clés et clarifier les dates contradictoires. |
| R4 | `lettre-licenciement` | Signaler le problème du délai convocation/entretien et distinguer présentation/envoi. |
| R5 | `rupture-conventionnelle` | Identifier le salarié protégé et la procédure d’autorisation spécifique. |
| R6 | `lettre-demission` | Distinguer date d’envoi et notification/première présentation. |
| R7 | `plainte-simple` | Permettre le récit et la plainte contre X sans exiger une qualification ou une preuve complète. |
| R8 | `contestation-amende` | Demander l’avis majoré, ses dates, le mode d’envoi, paiement/consignation et éléments du motif. |
| R9 | `recours-gracieux` | Identifier le régime spécial d’urbanisme et demander décision/notification/voies de recours. |
| R10 | `mentions-legales-et-confidentialite` | Demander les traitements réels, bases, destinataires, durées, traceurs et transferts. |

## Parcours complet et cas transversaux

- **F1** : dossier fictif de restitution entièrement renseigné. Recalcul
  documentaire au 10 septembre 2026 : 900 € de principal ; échéance au 10 juillet
  après remise des clés le 10 juin et états des lieux conformes ; deux périodes
  mensuelles de retard commencées, soit 180 € de majoration si les conditions
  de l'article 22 sont établies. Distinguer ce recalcul de la réussite d'une
  génération par le modèle. Le délai demandé de quinze jours dans la lettre
  est un choix du demandeur, pas le délai légal initial de restitution.
- **Q1** : explication générale d'un dépôt de garantie, sans questionnaire
  personnel inutile.
- **Q2** : contrat ancien et procédure ancienne ; identifier les versions et
  dispositions transitoires, sans appliquer automatiquement le dernier texte.

## Exécution et revue

Pour une exécution manuelle, invoquer le modèle concerné avec un dossier
fictif adapté au point décisif, puis conserver les faits soumis et la réponse.
Relever version du harnais, modèle, version plugin, commit et état du dépôt. Examiner
la réponse complète, les références chargées et la vérification des sources.
Renseigner ensuite PASS/FAIL avec justification et chemin du rapport ; garder
NON ÉVALUABLE si la session est invalide ou interrompue.

## Pass/Fail record

| Date | Cas | Contrôle | Résultat observé | Notes |
|---|---|---|---|---|
| 2026-09-10 | R1–R10 | Revue des modèles et du contrat | PASS documentaire | Dix qualifications/questionnaires relus ; lint des champs, conditions, quatre sections et avertissements réussi. Ce n'est pas une exécution des prompts. |
| 2026-09-10 | F1 | Recalcul du dossier fictif | PASS documentaire | 900 € + 180 € sous les faits du scénario ; texte officiel recoupé. Contrôle distinct des générations ci-dessous. |
| 2026-09-10 | R1, R2, R3, R5, R6, R7, F1 | Comportement après correction commune | PASS ciblé | Série `legal-corrected-20260910.json` ; F1 produit une lettre complète avec total de 1 080 €. Réserves annexes conservées. |
| 2026-09-10 | R4, R8 | Comportement après correction des modèles | PASS ciblé | Série `legal-targeted-20260910.json` ; entretien et consignation accomplis non inventés. |
| 2026-09-10 | R9, R10 | Comportement après dernière correction | PASS ciblé | Série `legal-neutral-20260910.json` ; réserve neutre et traitements à documenter. Les exemples de computation des délais de R9 et la vérification web RGPD de R10 ne sont pas validés. |
| 2026-09-10 | Q1, Q2 | Comportement général / temporalité | PASS ciblé | Première série `legal-authorized-20260910.json` ; pas de questionnaire personnel inutile ni application mécanique du texte actuel. |

Exécutions autorisées sur Claude Code 2.1.251, modèle `claude-fable-5-1[1m]`,
plugin local 3.1.0. Les résultats ci-dessus réunissent les dernières exécutions
pertinentes de plusieurs séries, avec les mêmes prompts. Ils ne constituent
pas une nouvelle exécution complète sur la version finale. Les journaux
locaux dans `evals/` conservent les échecs, corrections et réserves. Un PASS ciblé ne vaut pas satisfaction de tous les
critères communs ni validation de chaque affirmation juridique de la réponse.

Passe du 11 septembre 2026 : mode web prioritaire et clients API facultatifs
ajoutés après ces mesures. Aucun test relancé ; les résultats historiques
ci-dessus ne valident pas ces nouvelles modifications.
