---
type: rupture-conventionnelle
domain: travail
short_description: Convention de rupture conventionnelle individuelle (modèle utilisable en complément du CERFA 14598)
required_fields:
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
---

## Questionnaire

1. Raison sociale + adresse + SIRET de l'employeur ?
2. Nom complet, adresse, poste du salarié ?
3. Date d'embauche initiale (début du contrat de travail) ?
4. Salaire brut mensuel (de référence : moyenne des 12 derniers mois ou 3 derniers, le plus favorable) ?
5. Date envisagée pour la rupture (au plus tôt le lendemain de l'homologation par la DREETS) ?
6. Montant de l'indemnité spécifique de rupture conventionnelle (au minimum l'indemnité légale de licenciement, calculée selon l'art. R. 1234-2) ?
7. Convention collective applicable ?
8. Ancienneté en années complètes au moment de la rupture ?

(Le minimum légal est de 1/4 de mois de salaire par année pour les 10 premières années, puis 1/3 pour les suivantes : vérifier le minimum conventionnel qui peut être supérieur.)

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

Le Salarié et l'Employeur se sont rencontrés au cours d'un (ou plusieurs) entretien(s) préalable(s) tenu(s) le(s) :

- [Date entretien 1]
- [Date entretien 2 si applicable]

Au cours de ces entretiens, le Salarié a été informé qu'il pouvait se faire assister, conformément à l'article L. 1237-12 du Code du travail, par une personne de son choix appartenant au personnel de l'entreprise ou, en l'absence d'institutions représentatives du personnel, par un conseiller du salarié.

### Article 3 : Date envisagée de rupture

La date de rupture du contrat de travail est fixée au {{date_envisagee_rupture}}, sous réserve de l'homologation de la présente convention par la DREETS.

Conformément à l'article L. 1237-13, cette date ne peut être antérieure au lendemain du jour de l'homologation de la convention.

### Article 4 : Indemnité spécifique de rupture

L'Employeur versera au Salarié une indemnité spécifique de rupture conventionnelle d'un montant brut de {{indemnite_montant}} euros.

Cette indemnité respecte le montant minimum prévu par l'article L. 1234-9 et la convention collective {{convention_collective}} le cas échéant.

Ce montant sera versé au plus tard le jour de la rupture effective du contrat.

### Article 5 : Documents de fin de contrat

Au jour de la rupture, l'Employeur remettra au Salarié :
- le certificat de travail,
- l'attestation France Travail (ex-Pôle emploi),
- le reçu pour solde de tout compte,
- le solde de tout compte incluant l'indemnité de rupture conventionnelle, les congés payés non pris et tout autre élément dû.

### Article 6 : Délai de rétractation

Conformément à l'article L. 1237-13, les parties disposent d'un délai de **15 jours calendaires** à compter de la date de signature de la présente convention pour exercer leur droit de rétractation par lettre recommandée avec accusé de réception adressée à l'autre partie.

### Article 7 : Homologation

À l'expiration du délai de rétractation, la partie la plus diligente adresse la présente convention à la DREETS compétente. Celle-ci dispose de **15 jours ouvrables** à compter de sa réception pour s'assurer du respect des conditions et homologuer la convention. À défaut de notification dans ce délai, l'homologation est réputée acquise.

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
- Trois exemplaires originaux signés : un pour l'employeur, un pour le salarié, un pour la DREETS.
- Délais à respecter :
  - 15 jours calendaires de rétractation après signature.
  - 15 jours ouvrables d'instruction par la DREETS.
- Pour les salariés protégés (élu CSE, délégué syndical) : procédure d'autorisation par l'inspection du travail au lieu de l'homologation DREETS (art. L. 1237-15).
- Vérifier la qualification du salarié au regard d'éventuels avantages en cas de licenciement (allocation chômage : la rupture conventionnelle ouvre droit à l'ARE comme un licenciement).
