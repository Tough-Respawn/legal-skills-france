# Changelog : legal-france

All notable changes to this project are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/), and this project adheres
to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

## [4.5.0] - 2026-10-20

### Added

- Outil local `tools/legal-anonymiser/` : pseudonymisation d'un contrat
  (DOCX, PDF, numérisation) sur le poste de l'utilisateur, sans réseau,
  avant toute analyse par un modèle. Identifiants masqués par règles,
  structure du contrat, reconnaissance des noms (spaCy `fr_core_news_lg`) et
  propagation ; seconde passe sur le texte masqué ; arbitrage dans
  `ajustements.txt` ; validation humaine obligatoire (fenêtre native ou
  terminal interactif, aucune option ne publie) ; publication avec empreinte
  au registre (`verifier`) ; inspection technique du fichier (texte caché,
  caractères piégés, révisions, champs, macros, objets, JavaScript, mises à
  jour incrémentales, signature partielle, métadonnées, texte adressé à une
  IA) ; réidentification locale du rapport. Commandes `traiter`, `relancer`,
  `valider`, `verifier`, `reidentifier`. Seule exception à la règle « Python
  standard » du dépôt (pypdf, Pillow, spaCy, Tesseract installés par
  l'utilisateur) ; les 8 skills et les trois archives restent sans dépendance.
- Anonymiseur, verrou Claude Code : hook `PreToolUse` en Python standard
  (`python -m legal_anonymiser.verrou --coffre <racine>`) qui refuse `Read`,
  `Edit`, `Write`, `NotebookEdit` sur un original inscrit ou le coffre,
  `Grep` et `Glob` lancés depuis un dossier qui les contient (dossier
  personnel compris), `Bash` et `PowerShell` dont la commande cite le coffre,
  un original ou son nom ; chemins pris sous la forme que Claude Code ouvrira
  (`~`, `/c/...`, `\\?\`), motif `Glob` absolu coupé au dernier séparateur
  avant un joker, entrée lue en UTF-8 (chemins accentués) ; refus par
  décision JSON `deny` (le modèle ne voit ni chemin ni ligne de commande),
  erreur interne comprise (raison générique) ; code 2 seulement si la
  décision ne peut pas être écrite. Auto-protection : paquet, dossiers de
  l'interpréteur (venv, Python de base, site-packages de l'utilisateur),
  réglages `.claude/settings*.json`, commandes `uninstall-hook`. Commandes `install-hook` et `uninstall-hook`
  (`~/.claude/settings.json` par défaut, `--settings` sinon) : refus avec une
  version de Claude Code antérieure à 2.1.295 (code 6) ou sur des réglages
  non JSON (code 7), sauvegarde `settings.json.legal-france.bak`, écriture
  atomique (cible d'un lien symbolique), BOM accepté, une seule entrée, seul
  notre hook retiré, `"onFailure": "block"`, interpréteur lancé avec `-P` en
  Python 3.11 ou plus. Limites documentées : script, motif générique ou
  variables dans `Bash` ou `PowerShell`, outils MCP, réglages non JSON
  ignorés sans avertissement par Claude Code.
- Anonymiseur, dialogue de validation natif : `TaskDialogIndirect` sous
  Windows, `osascript` sous macOS, puis `tkinter`, puis terminal ;
  « Abandonner » par défaut, fermeture = abandon ; une erreur d'`osascript`
  autre que l'annulation passe au repli suivant.
- Quatre grilles de relecture d'ordre public dans les références des
  domaines : bail d'habitation (civil), contrat de travail (travail),
  contrat de consommation et contrat entre professionnels (affaires).
  Chaque point porte son fondement, l'URL Légifrance et sa date de
  vérification (2026-10-20) ; les éléments non confirmés sont marqués
  `NON VÉRIFIÉ`.
- Workflow de relecture de contrat `lib/relecture-engine.md`, sélectionné
  dans tous les harnais par `runtime.md`, et commande Claude Code `/relire`.
  Garde d'entrée : `legal-anonymiser verifier "<fichier>"` avant toute
  lecture d'un contrat fourni en fichier, même quand la question n'est pas
  une relecture (règle dans `runtime.md`, le protocole de recherche et le
  format Analyse de document), lecture sur `publie` seulement, refus sur `modifie`, contrat brut
  lu seulement sur consentement explicite après avertissement. Analyse en six
  étapes appuyée sur les grilles, rapport en huit parties avec placeholders,
  réidentification locale (`legal-anonymiser reidentifier`). Le contenu du
  document reste une donnée ; les requêtes de recherche n'en contiennent
  aucun extrait.
- Lint : contrôle 9 « relecture : grilles et renvois » (point numéroté avec
  fondement, sourcé avec date `vérifié le AAAA-MM-JJ` ou `NON VÉRIFIÉ`,
  renvois de `lib/relecture-engine.md` existants).

### Fixed

- Commandes Claude Code : chemins `lib/...` et `skills/...` préfixés par
  `${CLAUDE_PLUGIN_ROOT}/`. Sans base, le modèle cherchait les fichiers sur
  le disque, une fois jusqu'à parcourir le contrat masqué avant la garde.
- Relecture : aucune recherche (Glob, Grep, Select-String) sur le fichier ou
  son dossier avant `verifier` ; sections d'inspection absentes du fichier
  masqué signalées « inspection non disponible », sans inférence.

### Fixed

- Anonymiseur, relecture finale de branche (2026-10-20) : sortie Tesseract
  normalisée en LF à la source (plus de `\r` dans la détection) ; une forme
  connue en tête d'un nom est rognée quelle que soit la casse (une ligne de
  signature lue par l'OCR ne fusionne plus deux parties, un nom recollé à la
  ligne suivante garde son placeholder) ; une colonne de montants
  (`850\n120\n970`) n'est plus masquée comme numéro ; la seconde passe signale
  les initiales isolées (`initiales` : « ED », « J.K. ») ; le modèle spaCy
  absent est annoncé sur la console ; `bind`/`listen`/`accept` coupés par le
  filet réseau ; le coffre n'est créé qu'après un fichier choisi. Round 2 :
  en casse mixte, un tiers dont le nom suit un prénom connu (« Paul Avril »)
  n'est plus coupé ; un IBAN ou SIREN valide sur plusieurs lignes reste
  masqué. Docs : le clic humain « Publier » a été exécuté le 2026-10-19 à
  23:28 (README, `CLAUDE.md`, résultats).

---

## [4.4.0] - 2026-10-05

### Added

- Cible d'installation `deepseek-harness`. Le harnais scanne
  `<projet>/.agents/skills` et `~/.agents/skills`, déjà écrits par
  l'installateur : la cible nomme un emplacement existant au lieu d'ajouter
  une copie, et reste dédupliquée avec les autres harnais du même dossier.
  Racines et valeur par défaut d'`agentsHome` vérifiées le 2026-10-05 dans
  `docs/subsystems/skills.md` du dépôt `deepseek-ai/deepseek-harness`.
- Cible d'installation `qwen-code`, dédupliquée dans `.agents/skills`.
  Qwen Code lit `.qwen` puis `.agents` côté projet et utilisateur : établi
  par le code source (`config/storage.ts`, `skills/skill-manager.ts`),
  pas par sa documentation utilisateur. Vérifié le 2026-10-05.

### Changed

- Source officielle de Gemini CLI corrigée vers la documentation du dépôt
  `google-gemini/gemini-cli`, qui confirme `.agents/skills` comme alias
  interopérable prioritaire sur `.gemini/skills`. La destination écrite par
  l'installateur était déjà la bonne.

---

## [4.3.0] - 2026-09-30

### Added

- Import dans ChatGPT : commande `package-chatgpt` produisant
  `legal-france-chatgpt.zip`, plugin au format Agent Plugins (`plugin.json`
  validé contre le schéma 1.0.0) contenant le skill unique de l'archive
  Claude.ai, avec logo, catégorie « Legal » et trois questions d'exemple.
- Guide grand public [CHATGPT.md](CHATGPT.md), dont la procédure de mise à
  jour d'un plugin importé.
- Logo LSF (`assets/logo.png`), Tenor Sans aux couleurs du drapeau.
- Le workflow `release-assets` construit et joint aussi l'archive ChatGPT.

### Validation

- Import dans ChatGPT réussi le 30 septembre 2026 sur un compte personnel :
  logo, catégorie « Legal », questions d'exemple, version et skill affichés.
  Un nouvel import de la même version est refusé tant que le plugin existe ;
  la mise à jour passe par « Modifier » avec une version supérieure.
  Réponse du plugin dans une conversation pas encore testée.

## [4.2.0] - 2026-09-29

### Added

- Import dans Claude.ai sans installation, formule gratuite comprise :
  commande `package-claude-ai` produisant `legal-france-claude-ai.zip`, un
  skill unique regroupant les huit, avec une description de 174 caractères
  (limite Claude.ai : 200 ; les descriptions sources la dépassent).
  Version inscrite dans le SKILL.md, `.env.example` retiré de ce parcours.
- Guide grand public [CLAUDE-AI.md](CLAUDE-AI.md) : téléchargement, activation,
  import, questions en langage courant, autorisation durable des sites
  officiels consultés.
- Workflow `release-assets` : à chaque tag `vX.Y.Z` conforme à `project.json`,
  lint puis construction des deux archives et ajout à la release.

### Changed

- Liens de téléchargement vers `releases/latest/download/...`, noms
  d'archives stables d'une version à l'autre.

### Validation

- Import de l'archive dans Claude.ai réussi le 29 septembre 2026 : compétence
  chargée, ressources lues, vérification sur service-public.fr, réponse
  sourcée avec avertissement. Test manuel sur une question de dépôt de
  garantie, pas une mesure du routage. Workflow vérifié en local (contrôle
  du tag, lint, génération), pas encore sur GitHub avant ce tag.

## [4.1.0] - 2026-09-12

### Changed

- Source commune dans `src/legal-france/`, version dans `project.json` et
  particularités Claude dans son adaptateur. Le plugin généré conserve son
  emplacement, ses noms, ses commandes et ses descriptions de déclenchement.
- Un seul installateur : gestion native du plugin pour Claude, copies autonomes
  pour les autres harnais. Détection des doublons dans les emplacements Claude
  connus ; aucune suppression automatique des installations existantes.
- Accès API direct lorsque le service est explicitement choisi et que les
  paramètres utiles sont présents. Le web reste le mode par défaut et le repli
  explicite ; les références juridiques sont chargées selon l'analyse demandée.
- Modèle `.env.example` visible à la racine, conservé dans le plugin historique
  et inclus dans chaque skill portable. Le fichier d'identifiants `.env` de
  l'utilisateur n'est ni lu ni modifié par la génération ou l'installation.

### Validation

- Génération du plugin, du ZIP et de l'export documentaire, avec relecture
  statique. Aucun test de modèle, appel API ou installation dans les profils
  personnels dans cette passe. L'accélération des appels et l'installation
  native commune restent à mesurer ; les résultats v4.0.0 restent historiques.

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
