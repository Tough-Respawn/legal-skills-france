# Rédaction Test Scenarios — legal-france v3

One scenario per template (10 total). To run: in a fresh Claude Code
session, invoke `/rediger <type>` and provide the listed inputs. Verify
that the generated document contains all expected sections and that
cited articles match Legifrance.

---

## R1 — mise-en-demeure-generique

**Invoke:** `/rediger mise-en-demeure-generique`

**Inputs:**
- Expéditeur : Jean Dupont, 12 rue de Paris, 75011 Paris
- Destinataire : SARL DemoCorp, 8 avenue de Lyon, 69003 Lyon
- Objet : Facture impayée du 14 février 2026
- Obligation : paiement de 2 400 € HT
- Délai : 15 jours

**Expected:**
- Output cites articles 1344 et 1344-1 C. civ.
- Final document mentions "Lettre recommandée avec accusé de réception".
- Reinforced disclaimer present.
- Standard disclaimer at the end.

---

## R2 — attestation-honneur

**Invoke:** `/rediger attestation-honneur`

**Inputs:**
- Marie Martin, née le 03/05/1985 à Lille (59)
- Adresse : 7 rue des Lilas, 75019 Paris
- Fait : héberge depuis le 1er janvier 2026 son frère Paul Martin
- Usage : dossier CAF

**Expected:**
- Mention "Je soussigné(e)…"
- Avertissement art. 441-7 C. pén. présent
- Mention "Fait à … le …"

---

## R3 — mise-en-demeure-caution

**Invoke:** `/rediger mise-en-demeure-caution`

**Inputs:**
- Locataire : Thomas Bernard, 22 avenue du Maine, 75014 Paris
- Bailleur : SCI Dupont, 1 rue Saint-Honoré, 75001 Paris
- Logement : 4 place de la République, 75011 Paris
- État des lieux sortie : 31 janvier 2026
- Dépôt versé : 1 800 € le 15 février 2024

**Expected:**
- Citation art. 22 loi 89-462 du 6 juillet 1989.
- Mention pénalité 10% du loyer par mois.
- Pièces jointes listées.

---

## R4 — lettre-licenciement (motif personnel)

**Invoke:** `/rediger lettre-licenciement`

**Inputs:**
- Employeur : SAS TechCorp, 5 rue de la Pompe, 75116 Paris
- Salarié : David Dubois, 88 boulevard Saint-Germain, 75006 Paris
- Poste : Développeur senior
- Date d'embauche : 12 janvier 2020
- Motif : personnel — insuffisance professionnelle (3 retards de livraison documentés Q4 2025)
- Entretien préalable : 5 mai 2026
- Convention collective : Syntec

**Expected:**
- Citation art. L. 1232-6 C. trav.
- Préavis Syntec mentionné (cadre = 3 mois).
- Mention barème Macron pour information.

---

## R5 — rupture-conventionnelle

**Invoke:** `/rediger rupture-conventionnelle`

**Inputs:**
- Employeur : SARL ConsultPro, 14 rue Lafayette, 75009 Paris, SIRET 12345678900012
- Salarié : Aurélie Lefèvre, agent de maîtrise, embauchée 01/06/2018, salaire brut 2 800 €
- Date envisagée rupture : 30 juin 2026
- Indemnité : 12 600 €
- Convention : Syntec

**Expected:**
- Citation art. L. 1237-11 à L. 1237-16 C. trav.
- Mention délai de rétractation 15 jours.
- Mention DREETS et homologation.
- Trois exemplaires originaux mentionnés.

---

## R6 — lettre-demission

**Invoke:** `/rediger lettre-demission`

**Inputs:**
- Mathieu Petit, ingénieur (cadre)
- Date envoi : 1er juin 2026
- Convention collective : Syntec

**Expected:**
- Préavis cadre Syntec = 3 mois → date fin préavis calculée correctement (1er septembre 2026).
- Citation art. L. 1237-1 C. trav.
- Mention documents à remettre (certificat, attestation France Travail, solde de tout compte).

---

## R7 — plainte-simple

**Invoke:** `/rediger plainte-simple`

**Inputs:**
- Plaignant : Sophie Garcia, née 12/08/1990 à Marseille, française, infirmière, 9 rue du Bac 75007 Paris
- Faits : vol d'un sac à main le 14 avril 2026 vers 19h, métro Châtelet
- Qualification envisagée : vol
- Préjudice : 350 € + papiers d'identité

**Expected:**
- Référence "Monsieur le Procureur de la République".
- Citation possible art. 311-1 C. pén. (vol).
- Mention prescription 6 ans (délit).

---

## R8 — contestation-amende

**Invoke:** `/rediger contestation-amende`

**Inputs:**
- Olivier Roux, 4 chemin Vert, 38000 Grenoble
- Avis n° 1234567890
- Date constatation : 22 mars 2026
- Lieu : A48 km 12
- Infraction : excès de vitesse de moins de 20 km/h
- Véhicule : AB-123-CD
- Motif : véhicule vendu le 1er mars 2026 (joint le certificat de cession)

**Expected:**
- Citation art. 529-2 C. proc. pén.
- Mention délai 45 jours.
- Mention pièce jointe : certificat de cession.

---

## R9 — recours-gracieux

**Invoke:** `/rediger recours-gracieux`

**Inputs:**
- Requérant : Camille Moreau, 17 rue Saint-Maur, 75011 Paris
- Autorité : Préfet de Paris
- Décision : refus de délivrance de titre de séjour n° 2026-AB-001 du 1er avril 2026, notifiée le 10 avril 2026
- Moyens de droit : violation de l'art. L. 423-23 CESEDA (regroupement familial)
- Moyens de fait : situation familiale non examinée correctement

**Expected:**
- Référence "Monsieur le Préfet".
- Citation art. L. 411-2 CRPA et R. 421-2 CJA.
- Mention délai 2 mois et silence vaut rejet.

---

## R10 — mentions-legales-et-confidentialite

**Invoke:** `/rediger mentions-legales-et-confidentialite`

**Inputs:**
- Éditeur : SAS WebShop, capital 10 000 €, SIRET 11122233344455, RCS Paris B 123 456 789, TVA FR12345678901
- Adresse : 1 place Vendôme, 75001 Paris
- Email : contact@webshop.fr, Tél : 01 23 45 67 89
- Directeur publication : Léa Bernard
- Hébergeur : OVH SAS, 2 rue Kellermann 59100 Roubaix, 09 72 10 10 07
- URL : https://webshop.fr
- Traitements : comptes clients + commandes + newsletter + cookies analytics
- Durée conservation : commandes 10 ans, newsletter jusqu'au désabonnement, analytics 13 mois
- DPO : aucun

**Expected:**
- Citation art. 1-1 LCEN (issu de la loi SREN 2024 ; l'ancien art. 6 ne fonde plus les mentions légales).
- Citation RGPD art. 13/14 + 15-22.
- Section cookies citant délibération CNIL n° 2020-091.
- Lien CNIL présent.
- Mention transferts hors UE (à compléter).

---

## Pass/Fail record

| Date | Test ID | Pass/Fail | Notes |
|---|---|---|---|
| _ | _ | _ | _ |
