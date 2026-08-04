# Changelog — legal-france

All notable changes to this plugin are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/), and this project adheres
to [Semantic Versioning](https://semver.org/).

---

## [3.0.1] — 2026-08-04

### Fixed

- **Citations juridiques corrigées après audit externe**, chacune vérifiée sur Legifrance avec URL + date dans les fichiers : bloc CJA de `administratif.md` (numérotation entièrement réattribuée : L211-1, L111-1, R311-1, L3, L211-2, L213-1, L231-1 ; entrées inattribuables supprimées), CRPA L100-2 et L211-1 (textes réels restaurés), CRPA « silence vaut acceptation » L.131-1 → L.231-1 (`codes-index.md`), mise en demeure générique 1231-5 → 1344/1344-1 (1344-1 et intérêts moratoires désormais conditionnels au montant), lettre de démission L.1234-1 retiré.
- Frontmatter YAML invalide de `commands/rediger.md` (`claude plugin validate plugins/legal-france` passe).
- Versions marketplace/plugin désynchronisées (2.0.0 vs 3.0.0).
- Méta-skill recentré sur le transversal/multi-domaines pour réduire la compétition avec les 7 skills de domaine ; descriptions numerique et administratif ramenées sous la limite de 1 536 caractères.
- Judilibre : appels documentés via Bash `curl` (WebFetch ne peut pas faire le POST OAuth), exemple exécutable en une invocation sans exposer le secret, pagination 0-indexed vérifiée sur le dépôt officiel, test de présence des credentials silencieux.

### Added

- `tests/lint.py` : lint statique (frontmatters, longueurs, manifests, déclencheurs, inventaire `/rediger`, contrat de template).
- Baseline de déclenchement mesurée le 2026-08-04 (33 scénarios x 5 runs, grading strict) : 132/160 runs valides PASS, détail dans la table Pass/Fail de `tests/triggering.md`.
- Règle de traçabilité dans le README : toute citation ajoutée doit porter URL Legifrance + date de vérification.

## [3.0.0] — 2026-05-13

### Added

- **8 modular skills** (1 meta `legal-france` + 7 domain skills: `legal-france-civil`, `legal-france-travail`, `legal-france-penal`, `legal-france-affaires`, `legal-france-administratif`, `legal-france-numerique`, `legal-france-europeen`). Each domain skill auto-triggers on its own everyday vocabulary, dramatically improving recall on allusions like "mon proprio refuse de me rendre la caution", "j'ai été viré", "il faut un bandeau cookies ?".
- **`/rediger` command** and document drafter engine producing 10 production-grade templates:
  1. Mise en demeure générique
  2. Attestation sur l'honneur
  3. Mise en demeure restitution caution (loi 1989 art. 22)
  4. Lettre de licenciement (motif personnel ou économique)
  5. Convention de rupture conventionnelle
  6. Lettre de démission (avec calcul de préavis)
  7. Plainte simple au procureur de la République
  8. Contestation d'amende OMP (45 jours)
  9. Recours gracieux administratif (2 mois)
  10. Mentions légales + politique de confidentialité (LCEN + RGPD)
- **Judilibre API integration** for structured case-law search (Cour de cassation). Optional, configured via `PISTE_CLIENT_ID` / `PISTE_CLIENT_SECRET` env vars. Falls back transparently to Legifrance `WebSearch` when not configured.
- **Test suite** documenting triggering, drafting, and Judilibre integration scenarios (`tests/triggering.md`, `tests/redaction.md`, `tests/judilibre.md`).
- **Judilibre Protocol** section in `methodology.md`.
- **Reinforced disclaimer** appended to every generated document.

### Changed

- **Meta skill `legal-france` description** rewritten in French with 12+ verbatim everyday phrasings and a long French/English keyword bank for high-recall auto-triggering.
- **7 domain commands** (`/droit-civil`, `/droit-penal`, etc.) now route to their corresponding domain skill instead of the meta skill.
- **`/jurisprudence` command** now prefers Judilibre when PISTE credentials are present.
- **Domain references** (`civil.md`, `penal.md`, `travail.md`, `affaires.md`, `administratif.md`, `numerique.md`, `europeen.md`) moved from the meta skill into their respective domain skills. Transversal references (`codes-index.md`, `jurisprudence-cle.md`, `glossaire.md`, `sources.md`, `procedure.md`) stay in the meta.
- README expanded with PISTE setup procedure, `/rediger` documentation, and document inventory.

### Compatibility

- **No breaking changes** for end users.
- All v2 commands continue to work identically.
- Users without PISTE credentials get the v2 case-law experience (Legifrance `WebSearch`).

---

## [2.0.0] — 2026-03

### Added

- Complex Case Protocol (Template #7) for multi-domain questions with genuine cross-domain interaction.
- Mandatory Legifrance web verification.
- Progress indicators displayed during processing.
- Enriched references: ~96 landmark decisions, ~170 glossary terms, expanded domain reference files.

### Changed

- README rewritten as bilingual FR/EN.

---

## [0.1.0] — 2026-02

### Added

- Initial release. Single skill `legal-france`. 9 slash commands. 7 response templates. Embedded references for 7 domains. Citation standards. Mandatory disclaimer.
