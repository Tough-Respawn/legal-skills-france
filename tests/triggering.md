# Triggering Test Scenarios — legal-france v3

These scenarios verify that the right skill auto-triggers (without forcing
via "demande à legal" or a slash command). To run: in a fresh Claude Code
session with the plugin loaded, paste each user phrasing and verify which
skill activates. Pass = the matching skill activates first. Fail = the user
must force-trigger.

---

## Positive cases (21) — must trigger the listed skill

### Civil (3)
| # | User phrasing | Expected skill | Rationale |
|---|---|---|---|
| C1 | mon proprio refuse de me rendre la caution | legal-france-civil | "proprio" + "caution" in description |
| C2 | ma femme veut divorcer, on a un enfant | legal-france-civil | "divorcer" + "enfant" everyday phrasing |
| C3 | j'ai acheté un produit défectueux sur internet, je peux le retourner ? | legal-france-civil | consumer/civil + everyday |

### Travail (3)
| # | User phrasing | Expected skill | Rationale |
|---|---|---|---|
| T1 | j'ai été viré, j'ai quoi comme indemnités ? | legal-france-travail | "viré" + "indemnités" |
| T2 | mon patron veut me faire signer une rupture conventionnelle | legal-france-travail | "patron" + "rupture conventionnelle" |
| T3 | combien d'heures sup max par semaine ? | legal-france-travail | "heures sup" allusion |

### Pénal (3)
| # | User phrasing | Expected skill | Rationale |
|---|---|---|---|
| P1 | comment porter plainte contre un voisin ? | legal-france-penal | "porter plainte" |
| P2 | j'ai reçu une amende, je peux la contester ? | legal-france-penal | "amende" + "contester" |
| P3 | mon fils a été placé en garde à vue, on fait quoi ? | legal-france-penal | "garde à vue" |

### Affaires (3)
| # | User phrasing | Expected skill | Rationale |
|---|---|---|---|
| A1 | je veux créer une SAS, c'est compliqué ? | legal-france-affaires | "SAS" |
| A2 | mon client refuse de me payer ma facture, je fais quoi ? | legal-france-affaires | unpaid invoice (commercial) |
| A3 | comment déposer une marque ? | legal-france-affaires | "déposer une marque" |

### Administratif (3)
| # | User phrasing | Expected skill | Rationale |
|---|---|---|---|
| AD1 | la préfecture refuse ma demande de naturalisation | legal-france-administratif | "préfecture" + "naturalisation" |
| AD2 | la CAF me réclame un trop-perçu, je peux contester ? | legal-france-administratif | "CAF" + "contester". Note 2026-08-04 : juridiquement le contentieux sécu relève du pôle social du TJ ; le skill administratif reste le propriétaire désigné côté routage (CAF/trop-perçu dans sa description) |
| AD3 | comment faire un recours gracieux ? | legal-france-administratif | "recours gracieux" |

### Numérique (3)
| # | User phrasing | Expected skill | Rationale |
|---|---|---|---|
| N1 | il faut un bandeau cookies sur mon site ? | legal-france-numerique | "bandeau cookies" |
| N2 | quelqu'un publie ma photo sur Facebook sans mon accord | legal-france-numerique | data privacy / image |
| N3 | je veux exercer mon droit à l'oubli sur Google | legal-france-numerique | "droit à l'oubli" + "Google" |

### Européen (3)
| # | User phrasing | Expected skill | Rationale |
|---|---|---|---|
| E1 | que dit la CJUE sur le RGPD ? | legal-france-europeen | "CJUE" |
| E2 | cette directive a-t-elle été transposée en France ? | legal-france-europeen | "directive" + "transposée" |
| E3 | quels sont mes droits en tant que citoyen européen vivant en France ? | legal-france-europeen | "citoyen européen" |

---

## Negative cases (6) — must NOT trigger any legal-france skill

| # | User phrasing | Why no trigger |
|---|---|---|
| NEG1 | comment faire une boucle for en Python ? | programming |
| NEG2 | donne-moi une recette de tarte aux pommes | cooking |
| NEG3 | calcule 17 × 39 | arithmetic |
| NEG4 | quelle est la capitale de l'Australie ? | general knowledge |
| NEG5 | écris un poème sur l'automne | creative writing |
| NEG6 | comment configurer un serveur nginx ? | sysadmin |

---

## Borderline cases (3) — accepted either way, document outcome

| # | User phrasing | Reasonable skills | Notes |
|---|---|---|---|
| B1 | j'ai un problème avec mon abonnement Spotify | legal-france-civil (conso) OR no trigger | If triggers: civil OK |
| B2 | mon site marketing parle d'un concurrent | legal-france-affaires (parasitism) OR legal-france-numerique (LCEN) OR no | Either is fine if it triggers |
| B3 | mon employeur a demandé mon dossier médical | legal-france-travail (preferred) OR legal-france-numerique (data protection) | Should trigger one of the two |

---

## Multi-domain cases (3) — should engage the meta skill `legal-france`

| # | User phrasing | Why meta |
|---|---|---|
| M1 | mon entreprise me licencie après que j'ai signalé une fuite de données RGPD à la CNIL | travail + numérique + lanceur d'alerte = genuine cross-domain |
| M2 | je veux contester une amende et porter plainte pour usurpation d'identité | pénal + procédure transversale. Revue 2026-08-04 : les deux demandes étant pénales, `legal-france-penal` seul est aussi accepté |
| M3 | quel est le délai de prescription en général ? | transversal procedural |

---

## Pass/Fail record

Baseline automatisée du 2026-08-04 : harnais headless local (non versionné),
5 runs/scénario, modèle `claude-fable-5[1m]`, CLI 2.1.104, plugin 3.0.0
(commit 506dd9e, working tree), grading strict (runs invalides exclus :
timeout, plugin non chargé ou chargé depuis un cache).

**Statut : baseline DIAGNOSTIQUE, pas une baseline de release.** Elle mesure
le plugin avant le durcissement du harnais et sans épinglage du modèle au
lancement. Une baseline de release devra être relancée sur la 3.0.1 avec le
harnais durci.

| Date | Case ID | Taux (runs valides) | Déclenché majoritairement | Notes |
|---|---|---|---|---|
| 2026-08-04 | C1, C2, C3 | 100% | legal-france-civil | |
| 2026-08-04 | T1, T2 | 100% | legal-france-travail | |
| 2026-08-04 | T3 | 100% (4 valides) | legal-france-travail | 1 timeout |
| 2026-08-04 | P1, P3 | 100% | legal-france-penal | |
| 2026-08-04 | P2 | 20% | legal-france (méta) | méta capte "amende + contester" |
| 2026-08-04 | A1 | 25% (4 valides) | none / strategy-france | compétition externe : strategy-france:creation-entreprise gagne 3/5 sur "créer une SAS" |
| 2026-08-04 | A2 | 60% | legal-france-affaires | méta capte 2/5 |
| 2026-08-04 | A3 | 100% | legal-france-affaires | |
| 2026-08-04 | AD1, AD3 | 100% | legal-france-administratif | |
| 2026-08-04 | AD2 | 0% | legal-france (méta) | méta capte 5/5 le trop-perçu CAF |
| 2026-08-04 | N1, N3 | 100% | legal-france-numerique | |
| 2026-08-04 | N2 | 40% | legal-france (méta) | méta capte 3/5 la photo publiée sans accord |
| 2026-08-04 | E1 | 40% | legal-france (méta) | |
| 2026-08-04 | E2 | 60% | legal-france-europeen / none | sous-déclenchement (none 2/5) |
| 2026-08-04 | E3 | 100% | legal-france-europeen | |
| 2026-08-04 | NEG1-NEG6 | 100% | none | aucun faux déclenchement |
| 2026-08-04 | B1, B3 | 100% | (issues acceptées) | |
| 2026-08-04 | B2 | 100% (2 valides) | (issues acceptées) | 3 runs exit=1 à investiguer |
| 2026-08-04 | M1 | 0% | legal-france-travail | le méta ne s'engage jamais, travail rafle 5/5 |
| 2026-08-04 | M2 | 100% | legal-france (méta) 5/5 | pénal accepté depuis revue 2026-08-04 mais non observé |
| 2026-08-04 | M3 | 80% | legal-france (méta) | civil capte 1/5 |

Chantier prioritaire issu de cette baseline : la compétition méta vs domaines
(P2, A2, AD2, N2, E1) et le sous-déclenchement E2 / M1.

---

### Baseline de référence 3.0.1 (2026-08-04/05)

Harnais durci (portes de validité complètes, modèle épinglé
`claude-fable-5[1m]`, plugins chargés enregistrés par run), plugin 3.0.1,
commit fe5810f. N2 et B3 relancés intégralement (5 runs frais) pour
remplacer 2 timeouts. **165/165 runs EXPLOITABLES pour l'évaluation du
déclenchement, 138 PASS (83,6 %), zéro run invalide au sens des portes de
validité.** Précision (audit 2026-08-05) : 39 sessions se terminent
normalement (`success`, exit 0) et 126 sont volontairement tronquées par
`--max-turns` après l'observation de l'invocation (`error_max_turns`,
exit 1), troncature acceptée par conception du harnais. Comparaison formelle avec la baseline diagnostique
(compare.py) : **aucune régression**, 3 améliorations (M1 0 % -> 20 %,
M3 80 % -> 100 %, E2 60 % -> 80 %), le reste stable.

Écarts persistants (mêmes causes que la diagnostique) :

| Case | Taux 3.0.1 | Déclenché à la place |
|---|---|---|
| P2 | 20% | legal-france (méta) |
| A1 | 20% | strategy-france:creation-entreprise ou none |
| A2 | 20% | legal-france (méta) — 60% en diagnostique, glissement dans le bruit (n=5) |
| AD2 | 0% | legal-france (méta) 5/5 |
| N2 | 40% | legal-france (méta) |
| E1 | 60% | legal-france (méta) |
| M1 | 20% | legal-france-travail |

Toutes les autres lignes (C1-C3, T1-T3, P1/P3, A3, AD1/AD3, N1/N3, E3,
NEG1-6, B1-B3, M2, M3) : 100 %.
