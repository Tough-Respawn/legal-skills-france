# Installation et compatibilité

La v4 fournit huit skills au format [Agent Skills](https://agentskills.io/specification).
Le modèle et le harnais sont deux choix distincts : les instructions peuvent
être utilisées avec le modèle configuré dans l'application. La découverte
des skills, les permissions et les outils restent propres à cette application.

## Installation personnelle par défaut

Python 3.10 ou ultérieur suffit pour l'installateur, sans paquet tiers.
Depuis le dossier téléchargé du dépôt :

```bash
python scripts/skill.py install
```

Si nécessaire, remplacer `python` par `python3` sous macOS/Linux ou par
`py -3` sous Windows, selon l'installation locale de Python.

Le menu demande les applications. En automatisation, préciser leur nom :

```bash
python scripts/skill.py install --agent codex cursor
```

La portée par défaut est **user** : tous les projets du compte utilisateur
sur cette machine, pour les applications qui découvrent ce dossier. Aucune
installation administrateur ni synchronisation vers d'autres ordinateurs.
Le script affiche les destinations. Pour les skills portables, il copie les
fichiers sans téléchargement ni modification des réglages. Pour Claude Code,
il délègue au gestionnaire natif, qui peut télécharger le plugin et actualiser
sa configuration. Aucun de ces parcours n'utilise les identifiants PISTE.

## Destinations documentées

Documentations officielles consultées le **11 septembre 2026**. `~` désigne
le dossier personnel du compte qui exécute Python, notamment
`C:\Users\Nom` sous Windows. Les chemins ci-dessous sont les choix de cet
installateur, parmi les emplacements documentés par les applications.

| Application | `--agent` | Installation personnelle | Installation de projet | Source officielle |
|---|---|---|---|---|
| Claude Code | `claude-code` | Plugin natif, portée `user` | Plugin natif, portée `project` | [Claude Code](https://code.claude.com/docs/en/discover-plugins) |
| Codex | `codex` | `~/.agents/skills/` | `.agents/skills/` | [OpenAI](https://learn.chatgpt.com/docs/build-skills) |
| Cursor | `cursor` | `~/.agents/skills/` | `.agents/skills/` | [Cursor](https://cursor.com/docs/skills) |
| GitHub Copilot | `github-copilot` | `~/.agents/skills/` | `.agents/skills/` | [GitHub](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| Gemini CLI | `gemini-cli` | `~/.agents/skills/` | `.agents/skills/` | [gemini-cli, docs/cli/skills.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md) |
| OpenCode | `opencode` | `~/.agents/skills/` | `.agents/skills/` | [OpenCode](https://opencode.ai/docs/skills/) |
| Windsurf / Cascade | `windsurf` | `~/.codeium/windsurf/skills/` | `.windsurf/skills/` | [Cascade](https://docs.devin.ai/desktop/cascade/skills) |
| Cline | `cline` | `~/.cline/skills/` | `.cline/skills/` | [Cline](https://docs.cline.bot/customization/skills) |
| Roo Code | `roo-code` | `~/.agents/skills/` | `.agents/skills/` | [Roo Code](https://roocodeinc.github.io/Roo-Code/features/skills/) |
| Amp | `amp` | `~/.agents/skills/` | `.agents/skills/` | [Amp](https://ampcode.com/docs/customize/skills) |
| DeepSeek Harness (dsh) | `deepseek-harness` | `~/.agents/skills/` | `.agents/skills/` | [deepseek-harness, docs/subsystems/skills.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md) |
| Qwen Code | `qwen-code` | `~/.agents/skills/` | `.agents/skills/` | [qwen-code, config/storage.ts](https://github.com/QwenLM/qwen-code/blob/main/packages/core/src/config/storage.ts) (code source) |

Gemini CLI documente `.agents/skills` comme alias interopérable de
`.gemini/skills`, côté utilisateur comme côté projet, et cet alias l'emporte
sur le dossier propre à Gemini en cas de doublon. L'installateur écrit donc
dans l'alias, partagé avec les autres harnais.

Qwen Code lit aussi `.agents/skills`, mais seul son code source l'établit :
sa documentation utilisateur ne cite que `~/.qwen/skills` et `.qwen/skills`.
La liste des dossiers vaut `.qwen` puis `.agents` dans
`packages/core/src/config/storage.ts`, et la fonction `getSkillsBaseDirs` de
`packages/core/src/skills/skill-manager.ts` les parcourt côté projet comme
côté utilisateur. `.qwen` l'emporte en cas de doublon. Ce comportement non
documenté peut changer sans annonce : si Qwen ne voit plus les skills,
installez-les dans `~/.qwen/skills` avec `--skills-dir`.
Sources vérifiées le 2026-10-05.

DeepSeek Harness lit six racines par rang. Les deux qui nous concernent sont
`<projet>/.agents/skills` (rang 200) et `<agentsHome>/skills` (rang 500), où
`agentsHome` vaut `$DSH_AGENTS_HOME` ou `~/.agents`. L'installateur écrit donc
aux emplacements déjà documentés, sans cible propre à DeepSeek. Ses racines
`.dsh/skills` sont prioritaires si vous y placez vos propres skills. Le harnais
n'explore pas les `SKILL.md` imbriqués : nos ressources vivent sous `resources/`
et portent le nom `protocol.md`, elles ne sont donc pas vues comme des skills.
Source vérifiée le 2026-10-05.

Les destinations communes sont dédupliquées : sélectionner Codex et Cursor
écrit une seule copie dans `.agents/skills/`. Les autres applications qui
lisent ce dossier peuvent également découvrir cette copie. Il ne s'agit pas
d'un réglage qui limite l'accès aux seuls harnais nommés dans la commande.

Un harnais peut découvrir plusieurs dossiers. Éviter de cumuler une copie
personnelle, une copie projet et un plugin contenant les mêmes skills.
Pour un utilisateur actuel du plugin Claude, le même installateur appelle la
mise à jour native dans la portée demandée. Il conserve le nom
`legal-france@legal-france` et ses commandes. Les copies autonomes détectées
dans les dossiers Claude personnels ou du projet bloquent l'ajout du plugin ;
elles ne sont pas supprimées. Une copie personnalisée dans un dossier Claude
est également refusée si le plugin est déjà installé.

Les métadonnées d'installation Claude sont lues dans le dossier de configuration
habituel ou `CLAUDE_CONFIG_DIR`, sans lire les réglages contenant des secrets.
Un marketplace du même nom pointant vers une autre source est conservé et
demande une gestion manuelle. Les autres emplacements personnalisés, profils
et environnements distants ne sont pas inventoriés automatiquement.

Claude utilise la version publiée du marketplace ; les autres harnais reçoivent
la version du dépôt téléchargé. Pour développer le plugin généré localement,
utiliser le mécanisme `--plugin-dir` de Claude. En simulation, aucune commande
Claude n'est exécutée. Si un téléchargement natif échoue, les étapes suivantes
ne sont pas lancées ; vérifier l'état dans le gestionnaire avant de reprendre.

## Projet et emplacement personnalisé

Le projet doit exister ; `--project` sélectionne explicitement cette portée :

```powershell
python scripts/skill.py install --agent cursor --project "C:\Projets\mon-projet"
```

L'option `--scope project` est aussi acceptée avec `--project`. `--scope user`
et `--project` ne peuvent pas être combinés. Pour un emplacement personnalisé,
indiquer **le parent** des huit dossiers de skills :

```bash
python scripts/skill.py install --skills-dir "~/.cursor/skills"
```

Utiliser un dossier reconnu par l'application. Un environnement distant,
un conteneur ou un agent cloud doit recevoir ses propres fichiers ; les
skills personnels du poste ne lui sont pas transférés par cet installateur.

## Écritures et mises à jour

```bash
python scripts/skill.py install --agent cursor --dry-run
python scripts/skill.py install --agent cursor --force
```

Pour les copies portables, la simulation affiche les destinations et le nombre de fichiers sans écrire.
Tous les conflits sont recherchés avant l'écriture. Les fichiers identiques
restent intacts ; un fichier différent bloque l'installation sans `--force`.
Avec `--force`, les fichiers distribués sont remplacés et les fichiers
supplémentaires conservés. Sauvegarder ses adaptations avant un remplacement.
Les liens symboliques et jonctions dans les destinations sont refusés.
Sous Windows, une destination trop longue bloque l'opération avant toute
écriture : au maximum 259 unités UTF-16 pour un chemin de fichier et 247
pour un dossier parent. Ces limites conservatrices s'appliquent aussi avec
`--force` et `--dry-run`, même si Windows autorise les chemins longs.
Elles évitent de produire des fichiers que certains harnais ne pourraient
pas lire. Choisir un dossier plus court ou la portée personnelle si ses
chemins tiennent dans ces limites. Voir les
[limites Windows](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation).
Une interruption ou erreur disque pendant l'écriture peut laisser une copie
partielle ; relancer la même version pour compléter les fichiers.

Pour mettre à jour les copies portables, télécharger la nouvelle version puis
relancer la même commande, avec `--force` si les fichiers distribués ont changé.
Ces copies ne se mettent pas à jour automatiquement ; les fichiers supplémentaires
et les autres plugins sont conservés.

Pour Claude Code, relancer `install --agent claude-code` demande la mise à jour
au gestionnaire natif. Ce parcours suit ses propres règles de téléchargement
et d'écriture ; les contrôles de longueur et de conflit ci-dessus concernent
les copies effectuées par Python. `--force` ne force pas le gestionnaire Claude.

## Paquet autonome et installation sans Python

Le mainteneur produit l'archive avec :

```bash
python scripts/skill.py package --output dist/legal-france-skills.zip
```

L'utilisateur peut décompresser cette archive et copier ses huit dossiers
directement dans un dossier de skills du tableau. Pour une installation
autonome Claude sans plugin existant, les dossiers sont `~/.claude/skills/`
ou `.claude/skills/` dans le projet. Aucun Python n'est requis
pour cette copie ni pour la lecture des instructions ; les API facultatives
continuent à demander Python 3.9 ou ultérieur et un outil d'exécution.

Chaque dossier contient son `SKILL.md`, la licence, le client API, le modèle
vide `.env.example` et les ressources nécessaires. Les références sont embarquées dans chaque dossier
pour éviter une dépendance à des skills voisins ou au dépôt téléchargé.
Cette duplication est produite automatiquement, jamais maintenue à la main.
Les protocoles embarqués portent le nom `protocol.md` pour ne pas être
découverts comme de nouveaux skills imbriqués. Les lectures restent sélectives.

La source juridique est dans `src/legal-france/`, la version dans `project.json`
et le modèle de configuration à la racine du dépôt. Le plugin Claude est
généré dans son dossier historique ; les autres distributions utilisent la
même source. Les chemins sont adaptés à la racine de chaque skill installé.
Les descriptions courtes sont dans les SKILL.md sources, sous 1 024 caractères.
Les descriptions Claude historiques sont conservées dans son adaptateur.
La préservation des textes ne démontre pas une qualité de routage identique.

## Import dans Claude.ai

```bash
python scripts/skill.py package-claude-ai --output dist/legal-france-claude-ai.zip
```

Claude.ai importe un skill par fichier ZIP, dossier du skill à la racine,
et limite la description à 200 caractères
([aide officielle](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills),
consultée le 29 septembre 2026). Les huit descriptions sources dépassent
cette limite. Cette commande produit donc un **skill unique** `legal-france`,
avec une description courte dédiée, les ressources des sept domaines et une
consigne de lecture des protocoles de domaine. Le frontmatter se limite à
`name` et `description`, et le modèle `.env.example` est retiré : les
identifiants PISTE ne sont pas utilisables dans ce parcours. Le guide
utilisateur est [CLAUDE-AI.md](CLAUDE-AI.md). L'import et le déclenchement
dans Claude.ai restent à vérifier.

## Import dans ChatGPT

```bash
python scripts/skill.py package-chatgpt --output dist/legal-france-chatgpt.zip
```

ChatGPT importe des plugins au format [Agent Plugins](https://agent-plugins.org/)
depuis Plugins > Ajouter > Importer une archive de plugin
([documentation OpenAI](https://developers.openai.com/plugins/build/plugins),
consultée le 30 septembre 2026). L'archive contient `plugin.json` à la racine,
validé contre le schéma 1.0.0, et le skill unique de l'archive Claude.ai dans
`skills/legal-france/`, avec le logo `assets/logo.png`, la catégorie
« Legal » et trois questions d'exemple. Aucune application MCP n'est incluse.

L'aide OpenAI réserve l'import de *skills* aux espaces Business, Enterprise,
Healthcare et Edu et ne précise pas les formules autorisées pour l'import de
plugins ; l'option a été constatée sur un compte personnel le 30 septembre
2026. La création de GPT personnalisés est fermée aux comptes personnels et
leur retrait est annoncé ; ils ne sont pas proposés. L'import a été vérifié
le 30 septembre 2026 ; un plugin existant se met à jour par « Modifier » avec
une version supérieure. La réponse dans une conversation reste à vérifier.

## Utilisation et export pour les interfaces sans skills

Sélectionner le skill depuis le menu de l'application ou demander :

> Utilise legal-france-civil pour analyser ce bail. Présente les faits manquants,
> les pièces utiles et les sources vérifiées.

Le skill `legal-france` traite les demandes générales, transversales et les
recherches de jurisprudence ; les sept autres couvrent les domaines nommés.
Les dix commandes slash restent propres au plugin Claude. Leurs tâches
restent accessibles en langage naturel dans les skills portables.

```bash
python scripts/skill.py export --domain civil travail --output dist/cas-juridique.md
```

Domaines : `civil`, `penal`, `travail`, `affaires`, `administratif`,
`numerique`, `europeen`, ou `all`. L'export contient les instructions,
la méthodologie, la qualification, les sources, la procédure, l'index des
codes et les références/modèles des domaines choisis. Les ressources absentes
sont signalées. Il faut fournir ce document au modèle via l'application.
Sa taille est annoncée en octets, pas en tokens ; vérifier sa fenêtre de
contexte et limiter les domaines. Aucun outil web ou exécutable n'est ajouté.

## Portée de la validation

La v4.1.0 ajoute la source commune, le modèle `.env.example`
dans chaque skill, le parcours API direct et la délégation à l'installateur
natif Claude. Les générations ont été effectuées ; aucun nouveau test de
modèle, appel API ou installation dans un profil personnel n'a été lancé.
Le gain en nombre de tours et le nouveau parcours d'installation native
ne sont donc pas encore mesurés. Les résultats ci-dessous concernent la v4.0.0.

Cette version fournit les chemins documentés et un mécanisme de distribution.
La génération du ZIP et d'un export civil a été effectuée ; les fichiers
produits ont été relus. Une revue indépendante communiquée le 12 septembre
2026 rapporte l'installation, la réinstallation, la gestion des conflits,
la conformité des huit skills et leur découverte dans Claude Code 2.1.251.
Elle rapporte aussi la lecture des ressources portables après invocation
explicite du skill civil. Le routage naturel a sélectionné un ancien plugin
global en doublon ; il ne valide donc pas le routage des descriptions courtes.

La vérification complémentaire du 12 septembre rapporte le refus des chemins
Windows trop longs avant toute écriture, y compris en simulation, ainsi que
l'installation de 304 fichiers en chemin court. Le lint et la validation du
manifest ont également réussi selon ce compte rendu.

Le journal API du 12 septembre consigne douze cas réussis sur douze sous
Windows 11 avec Python 3.12.9, dont des appels authentifiés Légifrance et
Judilibre : sélection d'articles et texte LEGI datés, bornes de version,
erreurs explicites, recherche filtrée par chambre et lecture de décision.
Le couple commun `PISTE_*` fonctionne pour les deux services dans la
configuration testée. Ces essais valident le fonctionnement technique observé.

Ces résultats proviennent des revues, sans rejeu lors de cette mise à jour
documentaire. Les autres harnais, le routage portable, les parcours complets
avec un modèle, la pagination Judilibre au-delà de la première page, le tri,
les filtres de date et les limites de débit restent à vérifier. Il ne s'agit
pas d'une validation universelle ni d'une certification des réponses juridiques.

Les références juridiques et leurs dates de vérification sont conservées.
La portabilité n'est pas une actualisation du droit. Le web reste prioritaire,
les API sont activées sur demande, et les limites des outils disponibles
doivent rester visibles dans les réponses.
