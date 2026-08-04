---
type: mentions-legales-et-confidentialite
domain: numerique
short_description: Mentions légales (LCEN) + politique de confidentialité (RGPD) pour un site web ou e-commerce
required_fields:
  - editeur_type           # "personne-physique" | "personne-morale"
  - editeur_nom
  - editeur_adresse
  - editeur_email
  - editeur_telephone
  - directeur_publication
  - hebergeur_nom
  - hebergeur_adresse
  - hebergeur_telephone
  - site_url
  - traitements_donnees    # short description: visiteurs, comptes, commandes, newsletter, cookies
  - duree_conservation
optional_fields:
  - editeur_siret           # if morale
  - editeur_capital         # if morale
  - editeur_rcs             # if morale
  - editeur_tva             # if assujetti
  - dpo_nom                 # if appointed
  - dpo_email
applicable_law:
  - art. 1-1 de la loi n° 2004-575 du 21 juin 2004 (LCEN, mentions légales obligatoires ; article issu de la loi SREN n° 2024-449 du 21 mai 2024 : l'ancien fondement « art. 6-III » n'existe plus, vérifié le 2026-08-05)
  - art. 13 et 14 RGPD (information des personnes — politique de confidentialité)
  - art. 82 loi 78-17 modifiée + délibération CNIL n° 2020-091 du 17 sept. 2020 (cookies)
disclaimer_level: high
---

## Questionnaire

1. L'éditeur est-il une **personne physique** (auto-entrepreneur, particulier) ou une **personne morale** (société, association) ?
2. Nom complet (ou raison sociale) ?
3. Adresse postale complète du siège ou du domicile professionnel ?
4. Email de contact ?
5. Téléphone de contact ?
6. Directeur de la publication (nom de la personne responsable du contenu) ?
7. *Si personne morale :* SIRET, capital social, RCS ville, numéro de TVA intra (le cas échéant) ?
8. Nom de l'hébergeur ?
9. Adresse complète de l'hébergeur ?
10. Téléphone de l'hébergeur ?
11. URL du site ?
12. Quels traitements de données personnelles effectuez-vous ? (visiteurs anonymes, comptes utilisateurs, commandes e-commerce, newsletter, formulaire de contact, cookies analytics, autres ?)
13. Durée de conservation principale des données (par exemple : 3 ans après dernier contact pour prospect, 10 ans pour facturation, etc.) ?
14. *Optionnel :* avez-vous désigné un Délégué à la Protection des Données (DPO) ? Si oui, nom et email.

## Template

```
# Mentions légales et politique de confidentialité

## 1. Mentions légales (art. 1-1 LCEN, issu de la loi SREN 2024)

### 1.1 Éditeur du site

{{#if editeur_type=="personne-morale"}}
{{editeur_nom}}
Forme juridique : [SAS / SARL / SA / Association loi 1901 / autre]
Capital social : {{editeur_capital}}
SIRET : {{editeur_siret}}
RCS : {{editeur_rcs}}
{{#if editeur_tva}}N° TVA intracommunautaire : {{editeur_tva}}{{/if}}
{{else}}
{{editeur_nom}} (entrepreneur individuel)
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

Le responsable du traitement des données personnelles collectées sur le site {{site_url}} est : {{editeur_nom}}, {{editeur_adresse}}. Contact : {{editeur_email}}.

{{#if dpo_nom}}
Délégué à la Protection des Données (DPO) : {{dpo_nom}}, contact : {{dpo_email}}.
{{/if}}

### 2.2 Données collectées et finalités

Les traitements suivants sont mis en œuvre sur le site :

{{traitements_donnees}}

Pour chaque traitement, les bases légales sont précisées dans le tableau suivant (à compléter selon vos traitements réels) :

| Finalité | Données | Base légale (RGPD art. 6) |
|---|---|---|
| Gestion du compte utilisateur | Nom, email, mot de passe haché | Exécution du contrat (art. 6.1.b) |
| Commandes et facturation | Nom, adresse, paiement | Exécution du contrat + obligation légale (art. 6.1.b et c) |
| Newsletter | Email | Consentement (art. 6.1.a) |
| Statistiques de visite | Adresse IP, données techniques | Intérêt légitime (art. 6.1.f) après consentement cookies si applicable |
| Lutte contre la fraude | Adresse IP, logs | Intérêt légitime (art. 6.1.f) |

### 2.3 Destinataires

Les données ne sont communiquées qu'aux destinataires habilités au sein de l'éditeur et à ses sous-traitants techniques (hébergeur, prestataire de paiement, service de routage email) liés par contrat conforme à l'art. 28 RGPD.

Aucune donnée n'est cédée ni revendue à des tiers à des fins commerciales sans le consentement explicite de l'utilisateur.

### 2.4 Transferts hors UE

[Préciser si applicable : ex. "Nos sous-traitants Google Analytics / Mailchimp peuvent traiter certaines données aux États-Unis ; ces transferts sont encadrés par les clauses contractuelles types de la Commission européenne / certifiés Data Privacy Framework."]

### 2.5 Durée de conservation

Les durées de conservation principales sont les suivantes : {{duree_conservation}}.

Au-delà de ces durées, les données sont supprimées ou anonymisées.

### 2.6 Droits des personnes

Conformément aux articles 15 à 22 du RGPD et à la loi n° 78-17 modifiée, vous disposez des droits suivants sur vos données :

- **Droit d'accès** (art. 15)
- **Droit de rectification** (art. 16)
- **Droit à l'effacement** (art. 17 — « droit à l'oubli »)
- **Droit à la limitation** (art. 18)
- **Droit à la portabilité** (art. 20)
- **Droit d'opposition** (art. 21)
- **Droit de retrait du consentement** à tout moment lorsque ce dernier est la base légale du traitement

Pour exercer ces droits, contactez : {{editeur_email}}{{#if dpo_nom}} ou directement le DPO : {{dpo_email}}{{/if}}. Une preuve d'identité pourra vous être demandée.

En cas de difficulté, vous pouvez introduire une réclamation auprès de la **CNIL** : www.cnil.fr — 3 Place de Fontenoy, 75007 Paris.

### 2.7 Cookies et traceurs

Le site utilise des cookies pour son fonctionnement et, sous réserve de votre consentement préalable, pour la mesure d'audience ou la personnalisation.

À votre première visite, un bandeau vous permet d'accepter, refuser, ou personnaliser le dépôt des cookies non strictement nécessaires. Votre choix (consentement ou refus) est conservé pendant 6 mois, durée recommandée par la CNIL (recommandation « cookies », délibération n° 2020-092 du 17 septembre 2020 ; c'est une bonne pratique recommandée, pas un maximum réglementaire).

Vous pouvez à tout moment modifier vos choix via la page « Gestion des cookies ».

---

## 3. Propriété intellectuelle

L'ensemble du contenu du site (textes, images, logos, marques, code source) est protégé par le droit d'auteur et le droit des marques. Toute reproduction non autorisée est interdite (art. L. 122-4 CPI).

## 4. Droit applicable et juridiction compétente

Les présentes mentions légales sont régies par le droit français. En cas de litige, et à défaut de résolution amiable, les juridictions françaises seront seules compétentes.

---

Dernière mise à jour : {{date_du_jour}}
```

## Vérifications juridiques avant envoi

- Confirmer sur Legifrance la version en vigueur de l'art. 1-1 de la loi n° 2004-575 (LCEN), https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000049568614 (vérifié le 2026-08-05).
- Confirmer sur eur-lex.europa.eu la version actuelle du RGPD (règlement 2016/679) — articles 13, 14, 15-22.
- Vérifier sur cnil.fr la dernière délibération sur les cookies (n° 2020-091 ou plus récente).
- Sur le bandeau cookies : il doit présenter de manière équivalente les boutons "Accepter", "Refuser" et "Personnaliser". Pas de cases pré-cochées. Action positive obligatoire.
- Si transferts hors UE : préciser le mécanisme légal (CCT, BCR, décision d'adéquation, Data Privacy Framework si États-Unis). NE PAS oublier — c'est un point d'audit CNIL fréquent.
- Si vous traitez des données sensibles (santé, opinions, biométrie, mineurs) : l'analyse d'impact (AIPD, art. 35 RGPD) peut être obligatoire — consulter un DPO ou un avocat spécialisé.
- Le DPO devient obligatoire (art. 37 RGPD) dans certains cas : organisme public, surveillance régulière de personnes à grande échelle, traitement à grande échelle de données sensibles.
- Pour un site e-commerce : ces mentions doivent être complétées par des **CGV** distinctes (non couvertes par ce modèle).
