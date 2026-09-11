---
type: mentions-legales-et-confidentialite
domain: numerique
short_description: Mentions légales (LCEN) + politique de confidentialité (RGPD) pour un site web ou e-commerce
required_fields:
  - editeur_type
  - editeur_nom
  - editeur_adresse
  - editeur_email
  - editeur_telephone
  - directeur_publication
  - hebergeur_nom
  - hebergeur_adresse
  - hebergeur_telephone
  - site_url
  - traitements_donnees
  - duree_conservation
optional_fields:
  - editeur_siret
  - editeur_capital
  - editeur_rcs
  - editeur_tva
  - dpo_nom
  - dpo_email
applicable_law:
  - art. 1-1 de la loi n° 2004-575 du 21 juin 2004 (LCEN, mentions de l’éditeur)
  - art. 5, 6, 12 à 14 et 15 à 22 RGPD (traitements et information)
  - art. 82 loi n° 78-17 modifiée et lignes directrices/recommandation CNIL sur les traceurs
disclaimer_level: high
qualification_fields:
  - activite_public
  - role_traitement
  - origine_donnees
  - bases_legales
  - destinataires
  - transferts
  - traceurs
  - procedure_droits
  - decision_automatisee
  - pieces_disponibles
derived_fields:
  - presentation_responsable
  - date_du_jour
  - tableau_traitements
  - information_destinataires
  - information_transferts
  - information_cookies
  - information_droits
  - information_complementaire
  - modalites_conservation
---

## Qualification préalable

Appliquer `skills/legal-france/references/qualification.md`. Identifier
l'activité, les publics et territoires visés, le caractère professionnel,
et le rôle réel de l'éditeur dans chaque traitement. Vérifier les mentions
requises pour ce type d'éditeur ; ne pas qualifier automatiquement toute
personne physique d'entrepreneur individuel.

La politique décrit des traitements réels : demander l'inventaire,
formulaires, contrats des prestataires, paramètres des traceurs et parcours
d'exercice des droits. Pour chaque finalité, déterminer données, origine,
base légale, destinataires et durée/critère de conservation. Vérifier
séparément les transferts, le consentement aux traceurs et les informations
supplémentaires dues lors d'une collecte indirecte ou d'une décision automatisée.

Si ces informations manquent, produire une trame avec lacunes identifiées,
sans affirmer que le site est conforme, qu'un contrat de sous-traitance est
signé, qu'aucune donnée n'est vendue ou qu'un prestataire est certifié.

**Remplissage d'une trame sans inventaire** : le caractère « site marchand »
ne permet pas d'inventer des comptes clients, une collecte directe, des
champs obligatoires, un traitement antifraude ou des destinataires. Dans
`tableau_traitements`, reprendre seulement les finalités déclarées ; chaque
donnée, origine, base et durée inconnue reste un champ à établir. Laisser
`information_cookies`, `information_droits` et les autres paragraphes inconnus
comme champs entiers à compléter. Ne pas y préremplir un bandeau, un lien
de désabonnement, une absence de stockage ou de décision automatisée, même
suivis de « à confirmer ». Distinguer ce qui serait requis de ce qui existe.
Lorsque seul le nom d'une finalité est fourni, `tableau_traitements` est un
**tableau de collecte à compléter** : seule la colonne « Finalité déclarée »
est renseignée. Les colonnes données, origine, base et durée portent chacune
« À documenter » tant que leur valeur n'est pas donnée. L'origine de collecte
ne se déduit ni de la finalité ni du nom d'un outil. Les questions et pistes
de vérification restent hors de ce tableau ; elles ne deviennent pas ses
valeurs factuelles.
Si les sources n'ont pas été consultées dans la session, le dire explicitement
avant la trame ; la date historique du modèle ne constitue pas ce contrôle.

## Questionnaire

1. Quelle activité, quel public (dont mineurs si concernés), quels pays et quel caractère professionnel ? Qui décide des finalités et moyens des traitements ?
2. Pour chaque traitement réellement effectué : quelle finalité, quelles données, quelle origine directe ou indirecte, quelle base envisagée et quelles pièces permettent de le vérifier ?
3. Qui reçoit les données et quels prestataires interviennent ? Dans quels pays, avec quels contrats et mécanismes de transfert effectivement vérifiables ?
4. Quelles durées ou critères de conservation par finalité, puis quelles modalités d'archivage et de suppression sont réellement pratiquées ?
5. Quels cookies/traceurs sont effectivement utilisés, à quoi servent-ils, et quels mécanismes de choix existent ? Une exemption est-elle revendiquée et documentée ?
6. Comment les personnes exercent-elles leurs droits ? Quel contact/DPO, et existe-t-il une décision automatisée ou des traitements demandant une analyse particulière ?
7. Après qualification : forme et identité de l'éditeur, identifiants pertinents, coordonnées, directeur de publication, hébergeur et URL ? Des champs à compléter sont possibles pour la trame.

## Template

```
# Mentions légales et politique de confidentialité

## 1. Mentions légales (art. 1-1 LCEN, issu de la loi SREN 2024)

### 1.1 Éditeur du site

{{#if editeur_type=="personne-morale"}}
{{editeur_nom}}
Forme juridique : [SAS / SARL / SA / Association loi 1901 / autre]
{{#if editeur_capital}}Capital social : {{editeur_capital}}{{/if}}
{{#if editeur_siret}}SIRET : {{editeur_siret}}{{/if}}
{{#if editeur_rcs}}RCS : {{editeur_rcs}}{{/if}}
{{#if editeur_tva}}N° TVA intracommunautaire : {{editeur_tva}}{{/if}}
{{else}}
{{editeur_nom}}
{{#if editeur_siret}}SIRET : {{editeur_siret}}{{/if}}
{{/if}}
Adresse : {{editeur_adresse}}
Email : {{editeur_email}}
Téléphone : {{editeur_telephone}}

### 1.2 Directeur de la publication

{{directeur_publication}}

### 1.3 Hébergeur

{{hebergeur_nom}}
{{hebergeur_adresse}}
Téléphone : {{hebergeur_telephone}}

---

## 2. Politique de confidentialité (RGPD art. 13/14)

### 2.1 Responsable du traitement

{{presentation_responsable}}

{{#if dpo_nom}}
Délégué à la Protection des Données (DPO) : {{dpo_nom}}, contact : {{dpo_email}}.
{{/if}}

### 2.2 Données collectées et finalités

Les traitements suivants sont mis en œuvre sur le site :

{{traitements_donnees}}

{{tableau_traitements}}

{{information_complementaire}}

### 2.3 Destinataires

{{information_destinataires}}

### 2.4 Transferts hors UE

{{information_transferts}}

### 2.5 Durée de conservation

Les durées de conservation principales sont les suivantes : {{duree_conservation}}.

{{modalites_conservation}}

### 2.6 Droits des personnes

{{information_droits}}

En cas de difficulté, vous pouvez introduire une réclamation auprès de la **CNIL** : https://www.cnil.fr.

### 2.7 Cookies et traceurs

{{information_cookies}}

---

## 3. Propriété intellectuelle

Les contenus du site peuvent être protégés par des droits de propriété intellectuelle. Les utilisations doivent respecter les droits des titulaires et les exceptions légales applicables (Code de la propriété intellectuelle).

## 4. Droit applicable et juridiction compétente

Les règles de droit applicable et de compétence sont déterminées selon la situation, en tenant compte des dispositions impératives, notamment celles protégeant les consommateurs.

---

Dernière mise à jour : {{date_du_jour}}
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur de l'art. 1-1 de la loi n° 2004-575 (LCEN), https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000049568614 (vérifié le 2026-08-05).
- Confirmer sur eur-lex.europa.eu la version actuelle du RGPD (règlement 2016/679) : articles 13, 14, 15-22.
- Vérifier sur cnil.fr la dernière délibération sur les cookies (n° 2020-091 ou plus récente).
- Vérifier la nécessité du consentement pour les traceurs réellement utilisés et les conditions des exemptions éventuelles ; vérifier que refuser est aussi simple qu’accepter lorsque le consentement est requis. Décrire seulement les fonctions effectivement disponibles.
- Si transferts hors UE : préciser le mécanisme légal (CCT, BCR, décision d'adéquation, Data Privacy Framework si États-Unis). NE PAS oublier, c'est un point d'audit CNIL fréquent.
- Distinguer les catégories particulières de données de l’art. 9 (notamment santé, opinions et biométrie aux fins d’identifier une personne de manière unique) des données de mineurs. Examiner les risques du traitement et les critères de l’art. 35 pour déterminer si une AIPD est nécessaire ; ne pas présumer que toute donnée de mineur relève de l’art. 9.
- Le DPO devient obligatoire (art. 37 RGPD) dans certains cas : organisme public, surveillance régulière de personnes à grande échelle, traitement à grande échelle de données sensibles.
- Pour un site e-commerce : ces mentions doivent être complétées par des **CGV** distinctes (non couvertes par ce modèle).

- `presentation_responsable` identifie le ou les responsables réellement déterminés, leur contact et le site concerné ; ne pas assimiler automatiquement éditeur et responsable de tous les traitements.
- `tableau_traitements` reprend les finalités réelles, données et bases vérifiées ; aucun tableau fictif compte/newsletter/statistiques n'est conservé par défaut. Les champs `information_*` et `modalites_conservation` décrivent les pratiques établies ou restent explicitement à compléter.
- Adapter l'information sur les droits à leurs conditions d'exercice ; ne pas imposer systématiquement une pièce d'identité. Examiner les informations complémentaires des art. 13/14 (origine, fourniture obligatoire, conséquences, décision automatisée…) selon la collecte.
- Source du contrat d'information, contrôle ciblé le 2026-09-10 : RGPD, art. 5, 6, 12 à 14, https://eur-lex.europa.eu/eli/reg/2016/679/oj/fra. Les affirmations factuelles doivent être confirmées par l'éditeur et les pièces.
