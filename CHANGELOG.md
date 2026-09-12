# Changelog : legal-france

All notable changes to this project are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/), and this project adheres
to [Semantic Versioning](https://semver.org/).

---

## [4.0.0] - 2026-09-12

### Added

- Installateur Python 3.10+ sans dépendance tierce, inspiré d'accounting :
  portée personnelle par défaut, sélection d'un ou plusieurs harnais, portée
  projet facultative et emplacement personnalisé. Destinations communes
  dédupliquées, simulation, refus des conflits sans remplacement explicite.
- Génération d'une archive de huit skills autonomes et d'exports Markdown
  par domaines. Les références et les modèles partagés, les contrats API,
  le client Python et la licence sont inclus dans chaque skill installé.
- Matrice de compatibilité : chemins personnels et de projet documentés
  pour dix applications, distinction entre installation, outils et modèle.

### Changed

- Présentation du projet indépendante d'un harnais. L'installation et les
  commandes du plugin Claude restent disponibles pour les utilisateurs actuels.
- Dépôt renommé `legal-skills-france`, liens d'installation et description
  publique actualisés. Les noms du plugin et du marketplace restent `legal-france`.
- Les paquets portables ont des descriptions sous 1 024 caractères, des
  chemins internes résolus depuis leur SKILL.md et des instructions adaptées
  aux capacités de l'application. La source juridique et les descriptions
  historiques Claude ne sont pas dupliquées ni modifiées à la main.
- Documentation PISTE : une application commune abonnée à plusieurs API,
  configuration utilisée pour Légifrance et Judilibre lors de la validation,
  ou applications séparées avec couples spécifiques. Priorité des identifiants
  et refus des couples incomplets explicités dans le README et le modèle `.env`.
- Les versions des deux manifests sont alignées sur 4.0.0, publiée sans statut
  de préversion. Les limites de validation par harnais restent documentées.

### Fixed

- Refus des destinations Windows trop longues avant toute écriture :
  contrôle des chemins de fichiers et de leurs dossiers parents en unités
  UTF-16, y compris avec `--force` et en simulation. Une destination plus
  courte est demandée pour éviter l'installation partielle signalée en revue.
- Exclusion Git étendue aux variantes `.env.*`, dont les sauvegardes et les
  fichiers locaux, avec exception pour le modèle versionné `.env.example`.

### Validation

- Génération du ZIP et d'un export civil effectuée, relecture des artefacts
  et contrôles statiques. La revue indépendante communiquée le 12 septembre
  rapporte des vérifications de l'installation et des huit skills, leur
  découverte dans Claude Code 2.1.251 et une invocation explicite du skill
  civil avec lecture de ses ressources. Le routage naturel était perturbé
  par un ancien plugin global en doublon.
- Vérification complémentaire du 12 septembre : refus des chemins Windows
  trop longs avant toute écriture, en installation et simulation ; installation
  en chemin court de 304 fichiers. Lint et validation du manifest réussis,
  d'après le compte rendu fourni.
- Douze cas API réussis sur douze, consignés dans le journal local du
  12 septembre : appels authentifiés Légifrance et Judilibre, sélection datée,
  bornes de version, erreurs explicites, recherche filtrée et lecture de
  décision. Le couple commun `PISTE_*` sert les deux API dans la configuration
  testée. Contrôle des six fichiers de sortie : aucune valeur d'identifiant
  détectée, selon le compte rendu. Aucun rejeu lors de la mise à jour documentaire.
- Les autres harnais, le routage portable, les parcours complets avec un modèle,
  la pagination Judilibre au-delà de la première page, le tri, les filtres de
  date et les limites de débit restent à vérifier. Ces essais techniques ne
  valident pas une conclusion juridique ni une actualisation complète du fonds.

## [3.1.0-beta.1] - 2026-09-11

À la publication de cette bêta, les appels API avec des identifiants valides
et la régression complète restaient à vérifier. Les essais API du 12 septembre
sont consignés dans la section v4 ci-dessus.

### Added

- Contrat commun de qualification, chargé par les huit skills : objectif,
  urgence, faits décisifs, pièces utiles, contradictions, hypothèses explicites,
  version temporelle applicable et calcul traçable des délais. Questions
  conditionnelles par domaine ; identité demandée après les faits juridiques.
- Client Python standard commun : consultation Légifrance d'articles et
  textes LEGI à une date explicite, recherche et lecture Judilibre.
  Activation par `--use-api`, OAuth en mémoire, erreurs structurées et repli
  web. Identifiants communs PISTE ou couples spécifiques à chaque API.
- Méthodes de recherche KALI, BOSS/Urssaf, ANIL et BODACC. Les journaux de
  vérification et l'outillage d'évaluation restent locaux dans `evals/`.

### Changed

- Recherche et lecture web prioritaires pour tous les utilisateurs. L'API
  nécessite une demande ou une préférence de session explicite ; la présence
  d'identifiants seule n'active plus Judilibre. Aucune configuration imposée
  au parcours web.
- Ancien workflow Judilibre Bash/curl remplacé par le client Python portable.
- Runner, tests du runner, quinze scénarios et deux journaux déplacés de
  `tests/` vers `evals/`, déjà ignoré. Scénarios manuels et lint existants
  conservés dans le dépôt ; liens publics vers les fichiers locaux retirés.
- Fins de ligne des fichiers modifiés uniformisées en LF, convention ajoutée
  dans `.gitattributes` ; quatre cadratins réintroduits remplacés par des
  deux-points dans les modèles et le moteur.
- Les dix modèles commencent par le régime applicable, les dates et les
  preuves ; distinction entre faits à recueillir, identité, champs facultatifs
  et résultats à calculer. Les inconnues décisives restent visibles dans un
  brouillon incomplet. Les deux avertissements sont conservés.
- Les réponses vulgarisées exposent aussi les hypothèses et lacunes de preuve
  déterminantes. Vérification des sources décisives à l'usage ; les dates
  historiques du fonds ne sont pas actualisées en bloc.
- Lint étendu aux quatre sections du contrat, aux champs/conditions déclarés,
  aux listes de textes et à l'accès au protocole commun. Versions des deux
  manifests synchronisées à 3.1.0-beta.1 ; descriptions de déclenchement inchangées.

### Fixed

- Option `--env-file` acceptée avant le service, au niveau du service et
  après l'opération, en préservant la valeur fournie aux niveaux précédents.
  README clarifié sur la portée historique de la vérification du client curl.
- Dépôt de garantie : remise des clés, conformité des états des lieux,
  retenues, immeuble collectif, nouvelle adresse et majoration conditionnelle.
- Travail : protection du salarié, calendrier de procédure, préavis à partir
  de la notification et suppression des affirmations de régularité inventées.
- Amendes et recours administratifs : suppression des délais universels et de
  la prorogation automatique ; contrôle des actes et régimes spéciaux.
- Plainte, attestation et confidentialité : pas de fait, pièce, formalité ou
  conformité inventés pour compléter le document. Charge de la preuve et
  recevabilité des preuves illicites corrigées dans les exemples concernés.
- Corrections issues des exécutions : contrôle des assertions dans le corps
  même de l'acte, chronologie d'entretien non présumée, qualité du destinataire
  de l'amende à établir, réserve neutre dans le recours et tableau de collecte
  pour les traitements non inventoriés.

### Validation

- Lint, huit tests hors ligne et validation du manifest réussis. Après
  autorisation de l'utilisateur, smoke C1/NEG2 réussi avec Claude Code 2.1.251
  et `claude-fable-5-1[1m]`. Trente-deux exécutions comportementales valides
  réparties en quatre séries ; quinze cas disposent d'un PASS ciblé après
  corrections, dont le parcours complet F1. Les échecs et réserves sont
  conservés localement dans `evals/`. Ce bilan du 10 septembre précède le
  changement de priorité web/API ; il ne valide pas la version finale ni une
  absence de régression sur les 33 scénarios.
- Passe du 11 septembre : documentation technique consultée et code relu,
  sans tests ni appels authentifiés des nouveaux clients, à la demande de
  l'utilisateur. Aucun succès API en production revendiqué.
- Le protocole juridique est neutre ; la distribution reste celle du plugin
  existant. Adaptateurs supplémentaires et descriptions conformes à la limite
  Agent Skills de 1 024 caractères restent à traiter dans une autre passe.

## [3.0.3] - 2026-08-05

### Security

- Le fichier `.env` n'est plus sourcé (exécutable) mais lu par extraction textuelle des deux clés PISTE uniquement : un `.env` malveillant livré par un dépôt tiers ne peut plus exécuter de code lors d'un appel Judilibre. L'extraction retire aussi guillemets et retours chariot Windows qui cassaient l'authentification en silence. Bloc validé en réel (token OAuth Production obtenu le 2026-08-05).

## [3.0.2] - 2026-08-05

### Added

- Credentials PISTE : support d'un fichier `.env` à la racine du projet (fallback des variables d'environnement), `.env.example` fourni avec le plugin.
- README : tutoriel pas-à-pas d'obtention des clés PISTE, vérifié en conditions réelles le 2026-08-05 (consentement CGU, application Production, identifiants OAuth).

## [3.0.1] - 2026-08-04

### Fixed

- **Citations juridiques corrigées après audit externe**, chacune vérifiée sur Legifrance avec URL + date dans les fichiers : bloc CJA de `administratif.md` (numérotation entièrement réattribuée : L211-1, L111-1, R311-1, L3, L211-2, L213-1, L231-1 ; entrées inattribuables supprimées), CRPA L100-2 et L211-1 (textes réels restaurés), CRPA « silence vaut acceptation » L.131-1 → L.231-1 (`codes-index.md`), mise en demeure générique 1231-5 → 1344/1344-1 (1344-1 et intérêts moratoires désormais conditionnels au montant), lettre de démission L.1234-1 retiré.
- Frontmatter YAML invalide de `commands/rediger.md` (`claude plugin validate plugins/legal-france` passe).
- Versions marketplace/plugin désynchronisées (2.0.0 vs 3.0.0).
- Méta-skill recentré sur le transversal/multi-domaines pour réduire la compétition avec les 7 skills de domaine ; descriptions numerique et administratif ramenées sous la limite de 1 536 caractères.
- Judilibre : appels documentés via Bash `curl` (WebFetch ne peut pas faire le POST OAuth), exemple exécutable en une invocation sans exposer le secret, pagination 0-indexed vérifiée sur le dépôt officiel, test de présence des credentials silencieux.

### Added

- **Revue juridique étendue et traçable du corpus (2026-08-04/05)** : les 12 fichiers de `references/` (dont les 96 décisions de `jurisprudence-cle.md`, l'index des codes, le glossaire et les sources) et les 10 templates ont été passés en revue contre Legifrance/EUR-Lex/curia/CNIL (~600 entrées passées en revue, décomptes détaillés dans les rapports d'audit de session). La revue n'est PAS exhaustive : `procedure.md` porte une note d'audit partiel et certaines décisions des sections jurisprudence restent sous avertissement de non-vérification individuelle. Corrections majeures : références fabriquées neutralisées (arrêts « Stoïkoff », « Société Labbé », CE 390867, pourvois introuvables), délais dangereux corrigés (opposition ordonnance pénale 45 j, appel administratif 2 mois, abus de confiance 5 ans), réformes récentes intégrées (loi SREN 2024, loi 2025-1057 viol/consentement, CSRD, recodification CPP 2029, divorce 1 an), renumérotations post-réformes (LIL 2019, arbitrage 2011, sûretés 2021). Chaque entrée vérifiée porte URL + date.
- `tests/lint.py` : lint statique (frontmatters, longueurs, manifests, déclencheurs, inventaire `/rediger`, contrat de template).
- Baselines de déclenchement (33 scénarios x 5 runs, grading strict), détail dans la table Pass/Fail de `tests/triggering.md` : baseline DIAGNOSTIQUE du 2026-08-04 (132/160 runs exploitables PASS), puis baseline de RÉFÉRENCE 3.0.1 avec harnais durci (138/165 runs exploitables PASS, zéro régression entre les deux). « Exploitable » = l'invocation du skill a été observée ; 126 des 165 sessions sont volontairement tronquées par `--max-turns` après cette observation.
- Règle de traçabilité dans le README : toute citation ajoutée doit porter URL Legifrance + date de vérification.

## [3.0.0] - 2026-05-13

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

## [2.0.0] - 2026-03

### Added

- Complex Case Protocol (Template #7) for multi-domain questions with genuine cross-domain interaction.
- Mandatory Legifrance web verification.
- Progress indicators displayed during processing.
- Enriched references: ~96 landmark decisions, ~170 glossary terms, expanded domain reference files.

### Changed

- README rewritten as bilingual FR/EN.

---

## [0.1.0] - 2026-02

### Added

- Initial release. Single skill `legal-france`. 9 slash commands. 7 response templates. Embedded references for 7 domains. Citation standards. Mandatory disclaimer.
