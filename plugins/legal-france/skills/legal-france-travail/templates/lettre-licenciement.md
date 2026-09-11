---
type: lettre-licenciement
domain: travail
short_description: Projet de notification de licenciement après qualification du motif et de la procédure
qualification_fields:
  - type_contrat
  - statut_protection
  - autorisation_administrative
  - effectif_entreprise
  - representation_personnel
  - nombre_licenciements_periode
  - motif_type
  - motif_sous_type
  - date_connaissance_faits
  - date_presentation_convocation
  - date_entretien_prealable
  - anciennete_retenue
  - classification
  - convention_collective
  - remuneration_reference
  - reclassement_et_csp
required_fields:
  - employeur_signataire_nom
  - employeur_signataire_fonction
  - employeur_nom
  - employeur_adresse
  - salarie_nom
  - salarie_adresse
  - salarie_poste
  - date_embauche
  - motif_detaille
  - date_envoi
optional_fields:
  - faits_reproches
  - difficultes_economiques
  - pieces_examinees
derived_fields:
  - ville_employeur
  - salarie_formule_politesse
  - chronologie_procedure
  - expose_motif
  - dispositions_preavis
  - dispositions_indemnites
  - mentions_economiques
applicable_law:
  - art. L. 1232-1 à L. 1232-6 C. trav. (motif personnel)
  - art. L. 1332-2 et L. 1332-4 C. trav. (discipline)
  - art. L. 1233-1 à L. 1233-16 C. trav. (motif économique)
  - art. L. 1233-45 et L. 1233-65 et s. C. trav. (réembauche et CSP selon le cas)
  - art. L. 1234-1, L. 1234-9 et R. 1234-2 C. trav. (préavis et indemnité)
  - art. L. 2411-1 et s. C. trav. (salariés protégés)
disclaimer_level: high
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`. Identifier un
CDI de droit privé, le motif exact et la procédure suivie. Un CDD, un agent
public, une période d'essai, une inaptitude, une protection particulière ou
un licenciement collectif peuvent nécessiter un autre déroulement.
Vérifier ce régime avant de produire une notification personnalisée.

**Condition d'utilisation du corps ci-dessous** : les faits permettant de
notifier doivent être établis. Si la convocation, la tenue de l'entretien,
les explications effectivement recueillies ou une autorisation nécessaire
restent inconnues ou irrégulières, répondre par le bilan et les questions de
préparation ; ne pas reproduire une notification qui raconte ces étapes.
Un éventuel brouillon demandé expressément conserve `chronologie_procedure`
comme champ entier à compléter, sans phrase préremplie sur un entretien tenu,
la présence du salarié ou des explications qui n'auraient rien changé.

Distinguer la protection liée à un mandat ou une candidature (autorisation
administrative selon L. 2411-1 et s.) des protections contre la rupture liées
à la maternité ou à un accident du travail/maladie professionnelle. Ces
situations n'imposent pas, à elles seules, l'autorisation de l'inspecteur du
travail : contrôler leurs règles propres (L. 1225-4, L. 1226-9).

Ne pas présumer qu'un salarié n'est pas protégé ; demander les mandats,
candidatures et protections pertinentes. Si une autorisation est requise,
la notification ne peut être présentée comme prête tant que cette condition
n'a pas été vérifiée. Pour un motif économique, établir le nombre de
ruptures, la période, l'effectif, les consultations, le reclassement et le
régime CSP/congé de reclassement ; une phrase générique ne prouve aucune
recherche ni proposition.

Pièces utiles : contrat et avenants, convention/accord et classification,
convocation et preuve de présentation, éléments sur l'entretien, faits et
justificatifs, bulletins utiles ; selon le régime, avis médical, échanges
de reclassement, documents CSE et décision administrative. Une simple
allégation d'« insuffisance » ne suffit pas à affirmer la cause réelle et sérieuse.

## Questionnaire

1. Quel contrat, quel secteur et quel stade de procédure ? Cherchez-vous un brouillon ou une lettre à envoyer, et à quelle date ?
2. Quel motif précis : disciplinaire (quelle faute), insuffisance professionnelle, inaptitude ou économique ? Quels faits datés, quand ont-ils été connus, et quelles pièces les étayent ?
3. Le salarié a-t-il un mandat, une candidature ou une ancienne fonction représentative, ou une autre protection pertinente ? Une autorisation administrative a-t-elle été obtenue si nécessaire ?
4. Quels effectif et représentants du personnel ? Pour un motif économique : combien de licenciements sur quelle période, quelles consultations, recherches de reclassement et démarches CSP/congé de reclassement ?
5. Quand la convocation a-t-elle été présentée ou remise, et quand l'entretien a-t-il eu lieu ou été prévu en cas d'absence ? Fournir les éléments utiles ; ne pas confondre envoi et présentation.
6. Quelle convention collective (IDCC et champ), quelle classification, date d'embauche et ancienneté avec reprises/interruption ? Quels éléments de rémunération servent aux indemnités ?
7. Après cette analyse : identité/adresse des parties, poste, signataire habilité et date prévue d'envoi ? Des champs anonymisés sont possibles.

## Template

```
{{employeur_nom}}
{{employeur_adresse}}

Lettre recommandée avec accusé de réception

{{salarie_nom}}
{{salarie_adresse}}

À {{ville_employeur}}, le {{date_envoi}}

Objet : Notification de licenciement pour motif {{motif_type}}

{{salarie_formule_politesse}},

{{chronologie_procedure}}

Nous vous notifions votre licenciement pour les motifs suivants :

{{expose_motif}}

{{dispositions_preavis}}

{{dispositions_indemnites}}

À la fin du contrat, les documents de fin de contrat seront mis à votre disposition : certificat de travail, attestation France Travail et reçu pour solde de tout compte.

{{#if mentions_economiques}}
{{mentions_economiques}}
{{/if}}

Veuillez agréer, {{salarie_formule_politesse}}, l'expression de nos salutations distinguées.

{{employeur_signataire_nom}}
{{employeur_signataire_fonction}}
[Signature]
```

## Vérifications juridiques avant envoi

- En motif personnel, les cinq jours ouvrables courent entre la présentation/remise de la convocation et l'entretien (L. 1232-2), pas entre l'entretien et la notification. Vérifier séparément le délai minimal de deux jours ouvrables après l'entretien (L. 1232-6), et les délais disciplinaires le cas échéant.
- En économique individuel ou collectif de moins de dix salariés sur trente jours, vérifier L. 1233-15 : sept jours ouvrables, quinze pour le licenciement individuel du personnel d'encadrement visé par le texte. Ne pas appliquer ces délais à tout licenciement collectif.
- `chronologie_procedure` reprend seulement les événements établis ; ne pas écrire « régulièrement convoqué » sans contrôle. `expose_motif` distingue faits précis et qualification soutenue par l'employeur ; ne pas inventer des griefs ou une recherche de reclassement.
- `dispositions_preavis` et `dispositions_indemnites` sont déterminées selon le motif, la convention et la situation : aucun préavis exécuté ni indemnité de licenciement n'est promis automatiquement. Une date de première présentation future ne permet pas de fixer une date de fin certaine.
- `mentions_economiques` est établi seulement pour la branche économique : vérifier notamment priorité de réembauche et dispositif CSP/congé de reclassement pertinent avant notification. Ne pas remplacer la procédure par « vous pouvez solliciter un CSP ».
- Les nom et fonction du signataire doivent être obtenus auprès de l'utilisateur ; ils ne se déduisent pas du nom de l'entreprise.
- Si un point déterminant reste inconnu, produire seulement un brouillon incomplet ou poursuivre l'analyse adaptée. Préserver les avertissements renforcé et standard du moteur.
- Sources contrôlées pour ces corrections le 2026-09-10 : [L. 1232-2](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006901000), [L. 1233-15](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032344944), [procédure personnelle](https://www.service-public.gouv.fr/particuliers/vosdroits/F2839), [salarié protégé](https://www.service-public.gouv.fr/particuliers/vosdroits/F37916). Les autres références se vérifient selon la branche effectivement retenue.

- Distinction des protections contrôlée le 2026-09-10 : [L. 1225-4](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033022614), [L. 1226-9](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900975). Ne pas étendre le régime d'autorisation des mandats à toute protection contre le licenciement.
