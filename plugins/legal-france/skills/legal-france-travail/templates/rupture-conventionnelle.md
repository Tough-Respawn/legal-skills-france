---
type: rupture-conventionnelle
domain: travail
short_description: Projet complémentaire de rupture conventionnelle individuelle d’un CDI non protégé
required_fields:
  - employeur_signataire_nom
  - employeur_signataire_fonction
  - employeur_nom
  - employeur_adresse
  - employeur_siret
  - salarie_nom
  - salarie_adresse
  - salarie_poste
  - date_embauche
  - salaire_brut_mensuel
  - date_envisagee_rupture
  - indemnite_montant
optional_fields:
  - convention_collective
  - anciennete_annees
applicable_law:
  - art. L. 1237-11 à L. 1237-16 C. trav. (rupture conventionnelle individuelle)
  - art. L. 1234-9 C. trav. (montant plancher de l'indemnité)
  - art. R. 1234-2 (calcul de l'indemnité légale)
disclaimer_level: high
qualification_fields:
  - type_contrat
  - statut_protection
  - consentement_parties
  - dates_entretiens
  - date_signature_prevue
  - anciennete_detaillee
  - elements_remuneration
  - pieces_disponibles
derived_fields:
  - ville_signature
  - date_signature
  - entretiens_et_assistance
  - verification_indemnite
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`.

Ce corps correspond à une rupture conventionnelle individuelle d'un CDI
privé non protégé. Pour un salarié protégé, examiner la procédure
d'autorisation de l'inspecteur du travail ; ne pas produire les clauses
d'homologation DREETS comme si elles s'appliquaient. Identifier aussi les
régimes exclus ou spécifiques avant utilisation.

Établir le consentement des deux parties, les entretiens, l'assistance,
l'ancienneté (reprises et fractions d'année), la rémunération et le minimum
applicable. Demander contrat, avenants, bulletins pertinents, convention et
projet TéléRC. Ne pas certifier que le minimum est respecté sans calcul.
La date de rupture reste projetée tant que les étapes et dates nécessaires
ne sont pas établies ; calculer séparément rétractation et instruction.

## Questionnaire

1. S'agit-il d'un CDI privé et d'une rupture individuelle librement envisagée par les deux parties ? Existe-t-il une pression, un conflit ou une protection liée à un mandat/candidature ?
2. Quels entretiens ont réellement eu lieu, avec quelle information et quelle assistance ? Quelle date de signature est prévue ou déjà intervenue ?
3. Quelles date d'embauche, reprises d'ancienneté, interruptions et fractions d'année à la date projetée de rupture ?
4. Quelle convention collective (IDCC et champ) et quels éléments de salaire, primes et absences permettent de déterminer la référence applicable ? Fournir les pièces utiles.
5. Quel montant d'indemnité proposez-vous et quelle date de rupture souhaitez-vous ? Vérifier le minimum et le calendrier avant de les arrêter.
6. Après qualification : raison sociale, adresse, SIRET, signataire habilité et identité/adresse/poste du salarié, ou champs anonymisés ?

## Template

```
CONVENTION DE RUPTURE CONVENTIONNELLE DU CONTRAT DE TRAVAIL

Entre :

{{employeur_nom}}, immatriculée au SIRET {{employeur_siret}}, dont le siège social est situé {{employeur_adresse}}, représentée par {{employeur_signataire_nom}} en qualité de {{employeur_signataire_fonction}}, dûment habilité(e),

ci-après dénommée « l'Employeur »,

D'une part,

ET

{{salarie_nom}}, demeurant {{salarie_adresse}}, embauché(e) le {{date_embauche}} en qualité de {{salarie_poste}}, à durée indéterminée, au sein de l'entreprise précitée,

ci-après dénommé(e) « le Salarié »,

D'autre part,

Il a été convenu ce qui suit, dans le cadre des articles L. 1237-11 à L. 1237-16 du Code du travail.

---

### Article 1 : Principe de la rupture

Les parties conviennent, d'un commun accord et sans contrainte, de mettre un terme au contrat de travail qui les lie.

### Article 2 : Entretiens préalables

{{entretiens_et_assistance}}

### Article 3 : Date envisagée de rupture

La date de rupture du contrat de travail est fixée au {{date_envisagee_rupture}}, sous réserve de l'homologation de la présente convention par la DREETS.

Conformément à l'article L. 1237-13, cette date ne peut être antérieure au lendemain du jour de l'homologation de la convention.

### Article 4 : Indemnité spécifique de rupture

L'Employeur versera au Salarié une indemnité spécifique de rupture conventionnelle d'un montant brut de {{indemnite_montant}} euros.

{{verification_indemnite}}

Ce montant sera versé au plus tard le jour de la rupture effective du contrat.

### Article 5 : Documents de fin de contrat

Au jour de la rupture, l'Employeur remettra au Salarié :
- le certificat de travail,
- l'attestation France Travail (ex-Pôle emploi),
- le reçu pour solde de tout compte,
- le solde de tout compte incluant l'indemnité de rupture conventionnelle, les congés payés non pris et tout autre élément dû.

### Article 6 : Délai de rétractation

Conformément à l'article L. 1237-13, les parties disposent d'un délai de **15 jours calendaires** à compter de la date de signature de la présente convention pour exercer leur droit de rétractation par une lettre adressée par un moyen attestant de sa date de réception par l'autre partie.

### Article 7 : Homologation

À l'expiration du délai de rétractation, la partie la plus diligente demande l'homologation par la procédure applicable (TéléRC, sauf exception justifiée). L’autorité administrative dispose de **15 jours ouvrables** à compter de la réception de la demande pour s'assurer du respect des conditions et homologuer la convention. À défaut de notification dans ce délai, l'homologation est réputée acquise.

### Article 8 : Litiges

Tout litige relatif à la conclusion, l'exécution ou la rupture de la présente convention relève de la compétence du conseil de prud'hommes territorialement compétent.

---

Fait en trois exemplaires originaux à {{ville_signature}}, le {{date_signature}}.

L'Employeur                                Le Salarié

[Signature + cachet]                       [Signature, précédée de la
                                            mention manuscrite "Lu et
                                            approuvé : bon pour accord"]
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur des articles L. 1237-11 à L. 1237-16, L. 1234-9, R. 1234-2.
- Calculer rigoureusement l'indemnité minimale : 1/4 de mois × années (pour les 10 premières), puis 1/3 × années (au-delà). Si convention collective plus favorable, appliquer ce minimum supérieur.
- Demande d'homologation obligatoirement en ligne via **TéléRC** depuis le 1er avril 2022 (délai d'instruction : 15 jours ouvrables, art. L. 1237-14) ; le formulaire cerfa n° 14598 (version en vigueur) n'est admis qu'en cas d'impossibilité d'utiliser le téléservice. (Vérifié le 2026-08-05.)
- Prévoir un exemplaire signé remis à chaque partie et conserver la preuve de remise ; suivre les pièces et modalités de transmission requises par TéléRC. Les trois exemplaires proposés par ce modèle ne sont pas présentés comme une obligation générale.
- Délais à respecter :
  - 15 jours calendaires de rétractation après signature.
  - 15 jours ouvrables d'instruction par la DREETS.
- Pour les salariés protégés (élu CSE, délégué syndical) : procédure d'autorisation par l'inspection du travail au lieu de l'homologation DREETS (art. L. 1237-15).
- Vérifier la qualification du salarié au regard d'éventuels avantages en cas de licenciement (allocation chômage : la rupture conventionnelle ouvre droit à l'ARE comme un licenciement).

- `entretiens_et_assistance` reprend les faits confirmés ; `verification_indemnite` expose la référence, l’ancienneté et le minimum contrôlé. Les signataires sont renseignés par l’utilisateur. Sources pour ces corrections, consultées le 2026-09-10 : https://www.service-public.gouv.fr/particuliers/vosdroits/F19030 et https://www.service-public.gouv.fr/particuliers/vosdroits/R15060.
