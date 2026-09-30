# legal-france : skills de droit français pour plusieurs harnais / Portable French law skills

> **FR :** Assistant juridique français, 8 skills modulaires et 10 modèles de documents. Installation personnelle pour plusieurs harnais, avec le plugin Claude Code conservé. Recherche web prioritaire ; API Légifrance (textes datés) et Judilibre (jurisprudence judiciaire) facultatives.
> **EN:** French law assistant with 8 modular skills and 10 legal document templates. User-level installation for multiple agent applications, alongside the existing Claude Code plugin. Web search by default; optional Légifrance and Judilibre APIs.

**Version : [v4.3.0](https://github.com/Tough-Respawn/legal-skills-france/releases/tag/v4.3.0).**
Import sans installation dans Claude.ai et ChatGPT, avec des guides grand
public, et archives construites automatiquement à chaque version.

**Configuration API facultative : [.env.example](.env.example)**, à la racine
du dépôt. Le même modèle vide est inclus dans chaque skill portable généré.

Les destinations d'installation sont documentées pour dix applications.
La validation technique du 12 septembre 2026 compte douze cas API réussis,
dont des appels authentifiés à Légifrance et Judilibre. Le chargement et le
comportement dans les autres harnais, le routage portable et la régression
complète restent à vérifier.
Voir les sources et limites dans [COMPATIBILITY.md](COMPATIBILITY.md).
_Installation locations are documented for ten applications. Twelve API cases
passed on September 12, including authenticated calls to both services. Other
hosts, portable routing and full regression validation remain pending._

---

## Sans installation, dans Claude.ai ou ChatGPT / No install

**Vous n'êtes pas développeur ?** Utilisez legal-france directement dans
votre assistant : un fichier à télécharger et à importer, sans terminal.

- **Claude.ai** (formule gratuite comprise) : guide [CLAUDE-AI.md](CLAUDE-AI.md).
- **ChatGPT** (import de plugin, selon votre compte) : guide [CHATGPT.md](CHATGPT.md).

_Not a developer? Upload one ZIP file to Claude.ai or ChatGPT._

---

## Installation pour tous vos projets / Install across your projects

Téléchargez le dépôt (bouton **Code → Download ZIP** sur GitHub), décompressez-le
et ouvrez un terminal dans son dossier. Avec **Python 3.10 ou ultérieur**,
sans paquet supplémentaire :

```bash
python scripts/skill.py install
```

Selon votre installation de Python, utilisez `python3` sous macOS/Linux ou
`py -3` sous Windows à la place de `python`.

Choisissez une ou plusieurs applications dans le menu. Pour Claude Code,
l'installateur utilise son gestionnaire natif : il installe ou met à jour le
plugin publié, avec ses commandes habituelles. Pour les autres applications,
il copie les huit skills depuis le dépôt téléchargé vers votre dossier personnel.
La portée par défaut couvre tous vos projets. Les applications utilisant le
même dossier de skills partagent une copie. Rechargez ensuite les skills ou
ouvrez une nouvelle session.

Pour indiquer directement les applications :

```bash
python scripts/skill.py install --agent codex cursor
```

**Vous utilisez déjà le plugin Claude Code ?** Vous pouvez le sélectionner
dans le même installateur : sa mise à jour passe par le gestionnaire natif,
sans ajouter de copie autonome. Les noms du plugin et des commandes restent
inchangés. Si des skills Claude autonomes sont déjà présents, l'installateur
signale le conflit et les conserve ; leur migration demande un choix explicite.

L'installation par projet reste facultative :

```powershell
python scripts/skill.py install --agent cursor --project "C:\Projets\mon-projet"
```

Le dossier de projet doit exister. `list` affiche les applications et leurs
destinations ; `--dry-run` simule les écritures. Un fichier différent n'est
remplacé qu'avec `--force`, après sauvegarde de vos adaptations éventuelles.
Pour les copies portables sous Windows, une destination trop longue est refusée avant toute écriture :
choisissez alors un dossier plus court. Les limites sont précisées dans
[COMPATIBILITY.md](COMPATIBILITY.md#écritures-et-mises-à-jour).
Pour mettre à jour, télécharger la nouvelle version et relancer la même
commande, avec `--force` pour remplacer les fichiers portables modifiés.
Pour Claude, le gestionnaire natif conserve la gestion de sa configuration
et télécharge la version publiée du marketplace. Le mode `--dry-run` affiche
ses commandes sans les lancer. Voir [COMPATIBILITY.md](COMPATIBILITY.md).

**Sans Python :** télécharger [legal-france-skills.zip](https://github.com/Tough-Respawn/legal-skills-france/releases/latest/download/legal-france-skills.zip)
puis décompresser et copier ses huit dossiers dans le dossier personnel de skills de
votre application. Les chemins et les instructions de préparation de cette
archive sont dans [COMPATIBILITY.md](COMPATIBILITY.md).

_The Python installer defaults to user scope, across all projects. Select one or
more hosts interactively or with `--agent`. Use `--project` only for a project
installation. The generated ZIP also supports manual installation without Python._

## Plugin Claude Code / Claude Code plugin

L'installateur commun prend maintenant en charge ce parcours. Les commandes
natives suivantes restent disponibles pour les utilisateurs qui les préfèrent.

Avec Claude Code installé, exécutez ces deux commandes dans votre terminal :
ajoutez d'abord le marketplace du projet, puis installez le plugin.
_With Claude Code installed, run these two commands in your terminal: add the
project's marketplace first, then install the plugin._

```bash
claude plugin marketplace add Tough-Respawn/legal-skills-france
claude plugin install legal-france@legal-france
```

Ouvrez ensuite une nouvelle session Claude Code pour charger le plugin.
_Then start a new Claude Code session to load the plugin._

[Documentation d'installation / Installation documentation](https://code.claude.com/docs/en/discover-plugins)

---

## Commandes / Commands

Les commandes suivantes appartiennent au plugin Claude Code. Dans les autres
harnais, sélectionner le skill ou demander la tâche en langage naturel, par
exemple : « Utilise legal-france-civil pour rédiger une mise en demeure de
restitution du dépôt de garantie ». Les huit skills conservent les domaines,
la méthodologie et les dix modèles. Les noms de commandes du plugin ne sont
pas ajoutés aux menus des autres applications.

| Commande | Description (FR) | Description (EN) |
|----------|-------------------|-------------------|
| `/droit <question>` | Routage automatique vers le bon domaine | Auto-routes to the right domain |
| `/jurisprudence <recherche>` | Recherche de jurisprudence et décisions clés | Case law search and landmark decisions |
| `/droit-civil <question>` | Contrats, responsabilité, famille, succession | Contracts, liability, family, inheritance |
| `/droit-penal <question>` | Infractions, peines, procédure pénale | Offenses, penalties, criminal procedure |
| `/droit-travail <question>` | Emploi, licenciement, négociation collective | Employment, dismissal, collective bargaining |
| `/droit-affaires <question>` | Sociétés, commercial, PI, concurrence | Companies, commercial law, IP, competition |
| `/droit-administratif <question>` | Administration, juridictions administratives | Public administration, administrative courts |
| `/droit-numerique <question>` | RGPD, CNIL, protection des données | GDPR, CNIL, data protection |
| `/droit-europeen <question>` | Traités, directives, règlements, CJUE | Treaties, directives, regulations, CJEU |
| `/rediger <type>` | Générer un modèle de document juridique (10 modèles disponibles) | Generate a legal document template (10 templates available) |

---

## Profils utilisateur / User Profiles

Les instructions prévoient d'identifier votre profil et d'adapter la réponse :
_The skills instruct the assistant to identify your profile and adapt its response:_

- **Avocat / Magistrat** : Format consultation juridique structurée / Structured legal consultation
- **Étudiant en droit** : Cas pratique, commentaire d'arrêt / Case analysis, case commentary
- **Citoyen** _(défaut / default)_ : Langage clair, démarches pratiques / Plain language, practical steps
- **Entreprise** : Conformité, analyse de documents / Compliance, document analysis

---

## Documents disponibles / Available documents

Le rédacteur génère 10 modèles de documents prêts à personnaliser :

| # | Document | Domaine |
|---|---|---|
| 1 | Mise en demeure générique | Transversal |
| 2 | Attestation sur l'honneur | Transversal |
| 3 | Lettre de licenciement | Travail |
| 4 | Convention de rupture conventionnelle | Travail |
| 5 | Lettre de démission | Travail |
| 6 | Mise en demeure restitution caution | Civil / Bail |
| 7 | Plainte simple au procureur | Pénal |
| 8 | Contestation d'amende (OMP) | Pénal |
| 9 | Recours gracieux administratif | Administratif |
| 10 | Mentions légales + politique de confidentialité | Numérique |

Dans Claude Code : `/rediger <type>` (ex : `/rediger lettre-licenciement`). Dans les autres harnais : demander le document au skill, par exemple « Utilise legal-france-travail pour rédiger une lettre de démission ». Le rédacteur recueille les seuls faits décisifs absents et les pièces utiles, puis les coordonnées nécessaires. Il vérifie le régime et la version des textes applicables, expose les calculs possibles et génère le document avec une checklist. Les inconnues décisives restent visibles dans un brouillon incomplet ; aucune date ni formalité accomplie n’est inventée.

---

## Formats de réponse / Response Formats

7 modèles structurés alignés sur la méthodologie juridique française :
_7 structured templates aligned with French legal methodology:_

1. **Consultation juridique** / Legal Consultation
2. **Cas pratique** / Practical Case Analysis
3. **Commentaire d'arrêt** / Case Commentary
4. **Recherche de jurisprudence** / Case Law Research
5. **Analyse de document** / Document Analysis
6. **Explication vulgarisée** / Plain Language Explanation
7. **Cas complexe** / Complex Case Analysis _(v2.0)_

---

## Domaines couverts / Domains Covered

| Domaine | Domain | Skill auto-déclenchant | Fichier de référence |
|---------|--------|------------------------|----------------------|
| Droit civil | Civil law | `legal-france-civil` | `skills/legal-france-civil/references/civil.md` |
| Droit pénal | Criminal law | `legal-france-penal` | `skills/legal-france-penal/references/penal.md` |
| Droit du travail | Labor law | `legal-france-travail` | `skills/legal-france-travail/references/travail.md` |
| Droit des affaires | Business law | `legal-france-affaires` | `skills/legal-france-affaires/references/affaires.md` |
| Droit administratif | Administrative law | `legal-france-administratif` | `skills/legal-france-administratif/references/administratif.md` |
| Droit numérique | Digital law (GDPR) | `legal-france-numerique` | `skills/legal-france-numerique/references/numerique.md` |
| Droit européen | EU law | `legal-france-europeen` | `skills/legal-france-europeen/references/europeen.md` |
| Procédure | Procedural law | `legal-france` (meta) | `skills/legal-france/references/procedure.md` |

Références transversales / Cross-cutting references (méta skill `legal-france`) :

- `skills/legal-france/references/qualification.md` : Faits décisifs, pièces utiles, hypothèses et délais / Decisive facts, supporting documents, assumptions and deadlines
- `skills/legal-france/references/jurisprudence-cle.md` : 96 décisions clés / 96 landmark decisions
- `skills/legal-france/references/glossaire.md` : ~170 termes / ~170 terms
- `skills/legal-france/references/codes-index.md` : Index des codes français / Index of French legal codes
- `skills/legal-france/references/sources.md` : Sources officielles / Official sources

Les chemins de cet inventaire sont relatifs à `plugins/legal-france/` dans
le dépôt. Les paquets portables contiennent leurs propres références sous
`resources/`, accessibles depuis la racine de chaque skill installé.

---

## Indicateurs de progression / Progress Indicators

Les instructions prévoient des étapes visibles pendant le traitement,
si l'interface et le format de sortie le permettent :
_The skills request progress indicators when the interface and output format allow them:_

> **[1/5]** Identification du domaine juridique...
> **[2/5]** Chargement des références...
> **[3/5]** Vérification sur Legifrance...
> **[4/5]** Analyse et recoupement des sources...
> **[5/5]** Rédaction de la réponse...

---

## Sources

- [Legifrance](https://legifrance.gouv.fr)
- [EUR-Lex](https://eur-lex.europa.eu)
- [Conseil constitutionnel](https://www.conseil-constitutionnel.fr)
- [CNIL](https://www.cnil.fr)
- [Service-public.fr](https://www.service-public.fr)

---

## Sources web et API facultatives / Web sources and optional APIs

> **FR :** La recherche et la lecture des pages officielles restent le mode par défaut, sans compte ni configuration. Légifrance (textes datés) et Judilibre (jurisprudence judiciaire) sont des options activées à votre demande. Des identifiants présents ne suffisent pas à activer une API.
> **EN:** Official web search and page reading remain the default, with no account or setup. Légifrance and Judilibre APIs are optional and used only when you choose them.

Pour utiliser le web, posez simplement votre question. Si vous choisissez une
API, configurez PISTE ci-dessous puis indiquez par exemple : « Utilise l'API
Légifrance pour consulter cet article au 1er janvier 2020 » ou « Utilise
Judilibre pour cette recherche ». Une préférence exprimée dans la session
reste valable jusqu'à ce que vous demandiez de revenir au web.

Les deux clients sont réunis dans
[legal_api.py](plugins/legal-france/skills/legal-france/scripts/legal_api.py).
Ils utilisent Python 3.9 ou ultérieur, sans paquet tiers, Bash, sed ni curl.
Après installation des skills, Python n'est requis à l'usage que pour
l'option API. Si ce mode est indisponible, le skill poursuit avec les pages
officielles et signale la limite.

### Une application PISTE commune ou des applications séparées ?

Un même compte PISTE peut gérer plusieurs applications. Ici, une application
PISTE est la configuration qui porte les abonnements aux API et son couple
OAuth Client ID / Client Secret. Elle peut servir plusieurs harnais.

| Organisation | Abonnements dans PISTE | Identifiants à configurer |
|---|---|---|
| **Une application commune, le plus simple** | La même application de production est abonnée à Légifrance et Judilibre | Un seul couple `PISTE_CLIENT_ID` / `PISTE_CLIENT_SECRET` |
| **Deux applications séparées** | Une application de production abonnée à Légifrance, une autre à Judilibre | Un couple `LEGIFRANCE_CLIENT_ID` / `LEGIFRANCE_CLIENT_SECRET` et un couple `JUDILIBRE_CLIENT_ID` / `JUDILIBRE_CLIENT_SECRET` |

**Nous utilisons l'application commune** : cette configuration a servi aux
appels authentifiés des deux API lors de la validation du 12 septembre.
Les applications séparées permettent de gérer leurs identifiants et leurs
accès indépendamment. Un seul compte PISTE suffit pour les gérer.

Dans les deux cas, accepter les CGU et souscrire à **chaque API souhaitée**
pour l'application qui l'appellera. Un abonnement Judilibre seul ne donne
pas accès à Légifrance. Ce client prend en charge ces deux services ; pour
d'autres API juridiques, il faut également un client adapté.
Voir le [guide PISTE](https://piste.gouv.fr/help-center/guide).

### Étape 1 : Obtenir vos identifiants PISTE (pas-à-pas)

Le parcours d'inscription PISTE et d'abonnement Judilibre a été vérifié le 2026-08-05 avec l'ancien client curl. L'ajout de Légifrance a été documenté le 2026-09-11. Le 2026-09-12, les clients Python ont été vérifiés par des appels authentifiés aux deux API, notamment avec une application abonnée aux deux services et le couple commun `PISTE_*`. Référence générale : [guide officiel PISTE](https://piste.gouv.fr/help-center/guide).

1. **Créer un compte** sur [piste.gouv.fr](https://piste.gouv.fr/registration), activer via le lien reçu par mail, se connecter.
2. **Accepter les CGU de l’API choisie** : menu **API → Consentement CGU API** → chercher « Judilibre » ou « Légifrance » → accepter pour l’environnement **PRODUCTION**. Ne sautez pas cette étape : tant que les CGU ne sont pas validées, la case Judilibre reste grisée à l'étape 4 (c'est la cause n° 1 des blocages, [confirmée par la FAQ de l'API Légifrance](https://www.legifrance.gouv.fr/contenu/pied-de-page/foire-aux-questions-api) qui suit le même mécanisme). L'ancienne URL directe `/api-fr/consentement-cgu-api-fr` citée par de vieilles docs renvoie une 404 : passez par le menu.
3. **Créer votre ou vos applications de PRODUCTION** : menu **APPLICATIONS → Créer une application**. Créez une application pour partager le couple OAuth, ou deux pour séparer les services. N'utilisez pas l'application `APP_SANDBOX_<votre-email>` créée automatiquement à l'inscription : le plugin appelle les URL Production (`oauth.piste.gouv.fr`), une app Sandbox échouera avec `invalid_client`.
4. **Souscrire aux API choisies** : sur chaque application → « Modifier l’application » → dans la liste des API, cocher **JUDILIBRE** et/ou **Légifrance stable**, en **PRODUCTION** → « Appliquer les modifications ». Pour une application commune, cochez les deux API ; pour deux applications séparées, cochez le service correspondant sur chacune. Une seule souscription suffit si vous n'utilisez qu'une API.
5. **Générer et lire les identifiants OAuth** : onglet **Authentification** de l'application, section **« Identifiants Oauth »** (PAS la section « API Keys » au-dessus : autre méthode d'authentification, inutilisée par le plugin). Si le tableau est vide, cliquez « Générer » (type « Confidentiel », URL de rappel et certificat X.509 laissés vides). Puis :
   - **Client ID** = la valeur affichée dans la colonne « Client ID » du tableau ;
   - **Client Secret** = la valeur cachée derrière « **Consulter le client secret** » sur la même ligne.

   Attention à ne pas inverser les deux : un couple mélangé (ou pris pour moitié sur les API Keys) donne `invalid_client` sur `oauth.piste.gouv.fr`.

### Ajouter Légifrance si vous choisissez cette API

Si votre application est déjà configurée pour Judilibre, vous pouvez accepter
les CGU Légifrance et ajouter **Légifrance stable / PRODUCTION** aux accès de
cette même application : votre couple commun reste utilisable pour les deux
services. Vous pouvez aussi créer une application séparée et renseigner son
couple `LEGIFRANCE_*`. Un compte PISTE ou un abonnement Judilibre seul ne donne
pas nécessairement accès à Légifrance. La DILA décrit l'accès sur sa
[page API officielle](https://www.legifrance.gouv.fr/contenu/pied-de-page/open-data-et-api).

### Étape 2 : Définir les identifiants facultatifs

**Le fichier `.env` est facultatif.** Si les identifiants sont déjà définis
dans les variables d'environnement de votre session, vous pouvez utiliser
l'API sans créer ce fichier. Les variables d'environnement ont priorité
sur les valeurs du `.env`.

Choisissez l'une des trois méthodes ci-dessous : une seule suffit.
Les noms de variables dépendent du choix d'application, quelle que soit la
méthode. Les exemples Settings et variables système montrent le couple commun ;
pour deux applications séparées, utilisez les quatre variables spécifiques
présentées dans l'option A.

##### Option A : Fichier `.env` à la racine du projet (le plus simple à gérer)

Le modèle vide est à la racine du dépôt : **[.env.example](.env.example)**.
Dans un skill portable installé, il se trouve à côté de son `SKILL.md`.
Dans le plugin Claude, la copie historique `plugins/legal-france/.env.example`
reste fournie. Si votre explorateur masque les fichiers commençant par un
point, utilisez le lien ci-dessus ou activez leur affichage.

Copiez ce modèle sous le nom `.env` **dans le dossier de travail de votre
session**, puis renseignez-le localement. Conservez tout `.env` déjà présent.
Pour un autre emplacement, indiquez son chemin afin que le client utilise
`--env-file`. Le client peut aussi utiliser les variables d'environnement,
sans fichier `.env`.

**Avec une seule application abonnée aux deux API**, renseignez uniquement :

```bash
PISTE_CLIENT_ID=votre_client_id
PISTE_CLIENT_SECRET=votre_client_secret
```

**Avec deux applications séparées**, renseignez à la place :

```bash
LEGIFRANCE_CLIENT_ID=client_id_application_legifrance
LEGIFRANCE_CLIENT_SECRET=client_secret_application_legifrance
JUDILIBRE_CLIENT_ID=client_id_application_judilibre
JUDILIBRE_CLIENT_SECRET=client_secret_application_judilibre
```

Laissez les couples inutilisés vides ou absents, dans le fichier comme dans
l'environnement. Le couple spécifique au service est prioritaire sur
`PISTE_*`. S'il est partiellement renseigné, le client refuse la configuration
et ne complète pas la valeur manquante avec celle d'une autre application.
Renseignez toujours les deux valeurs issues de la même application.

Ajoutez `.env` et `.env.*` à votre `.gitignore` si le dossier est un dépôt Git,
avec `!.env.example` pour conserver le modèle. Après activation explicite du
mode API, le client lit les clés manquantes dans l'environnement depuis ce
fichier, textuellement et sans l'exécuter.

> **Piège Windows** : en enregistrant depuis le Bloc-notes, choisissez « Tous les fichiers » comme type, sinon le fichier s'appelle `.env.txt` et ne sera pas trouvé.

##### Option B : Settings Claude Code (persiste, marche dans tous les projets)

Ouvrez `~/.claude/settings.json` (Linux/macOS) ou `%USERPROFILE%\.claude\settings.json` (Windows) et ajoutez le bloc `env` :

```json
{
  "env": {
    "PISTE_CLIENT_ID": "votre_client_id",
    "PISTE_CLIENT_SECRET": "votre_client_secret"
  }
}
```

Si le fichier contient déjà d'autres clés, fusionnez le bloc `env` avec l'existant. Pas besoin de relancer le terminal : relancez juste la session Claude Code.

##### Option C : Variables d'environnement système (persistent globalement, utile si vous utilisez les creds avec d'autres outils)

**Linux / macOS** : ajoutez à la fin de `~/.bashrc`, `~/.zshrc` ou `~/.profile` :
```bash
export PISTE_CLIENT_ID="votre_client_id"
export PISTE_CLIENT_SECRET="votre_client_secret"
```
Puis `source ~/.bashrc` (ou rouvrez votre terminal).

**Windows** : méthode graphique :
1. Touche Windows → tapez "variables d'environnement" → ouvrir.
2. Cliquez "Variables d'environnement" → section "Variables utilisateur" → "Nouveau".
3. Créez `PISTE_CLIENT_ID` et `PISTE_CLIENT_SECRET` avec vos valeurs.
4. Rouvrez votre application et son terminal pour qu'ils reçoivent les nouvelles variables.

### Étape 3 : Choisir l'API à l'usage

Demandez explicitement le mode API dans votre conversation. Le skill peut
ensuite appeler le client avec `--use-api`. Sans ce drapeau, le programme
retourne `API_NOT_REQUESTED` avant de lire les secrets ou d'accéder au réseau.
Les exemples suivants supposent un terminal à la racine de ce dépôt :

```text
python plugins/legal-france/skills/legal-france/scripts/legal_api.py --use-api legifrance article --id LEGIARTI000006307920 --date 2021-04-15
python plugins/legal-france/skills/legal-france/scripts/legal_api.py --use-api judilibre search --query "harcèlement moral employeur" --chamber soc
```

Pour un plugin installé ailleurs, le skill utilise le chemin réel du script.
Le fichier `.env` est lu dans le dossier courant ; `--env-file` permet de
préciser son chemin avant le service, entre le service et l'opération, ou
après l'opération et ses arguments. Les secrets ne doivent pas
figurer dans la commande ni dans la conversation.

La date Légifrance est obligatoire. Le client distingue l'identifiant d'une
version de l'identifiant commun de l'article et refuse les sélections absentes
ou ambiguës. Les dispositions transitoires et le champ d'application restent
à analyser. Le client consulte des articles et textes LEGI ; les recherches
KALI, JORF et autres fonds restent sur le web.

Contrats détaillés : [Légifrance](plugins/legal-france/lib/legifrance-client.md)
et [Judilibre](plugins/legal-france/lib/judilibre-client.md). La validation
technique du 12 septembre 2026 a enregistré **12 cas réussis sur 12** sous
Windows 11 avec Python 3.12.9 : articles et texte LEGI datés, bornes de version,
erreurs explicites, recherche Judilibre filtrée par chambre et lecture d'une
décision. Le couple commun sert les deux API dans la configuration testée.
Ces essais ne valident pas une conclusion juridique ni un parcours complet
avec un modèle. La pagination au-delà de la première page, le tri, les filtres
de date Judilibre et les limites de débit restent à vérifier.

> **Sécurité** : ne commitez jamais vos identifiants ; `.env` et ses variantes `.env.*` sont ignorés par Git. Le modèle `.env.example` reste versionné.

---

## Versions

| Version | Date | Description |
|---------|------|-------------|
| **[v4.3.0](https://github.com/Tough-Respawn/legal-skills-france/releases/tag/v4.3.0)** | Septembre 2026 | Plugin ChatGPT importable (skill unique, logo LSF), guide grand public |
| **[v4.2.0](https://github.com/Tough-Respawn/legal-skills-france/releases/tag/v4.2.0)** | Septembre 2026 | Import dans Claude.ai sans installation (skill unique), guide grand public, archives générées à chaque tag |
| **[v4.1.0](https://github.com/Tough-Respawn/legal-skills-france/releases/tag/v4.1.0)** | Septembre 2026 | Source commune et distributions générées, installateur unique gérant aussi le plugin Claude natif, accès API direct sur demande |
| **[v4.0.0](https://github.com/Tough-Respawn/legal-skills-france/releases/tag/v4.0.0)** | Septembre 2026 | Installation personnelle pour plusieurs harnais, paquets de skills autonomes et exports documentaires ; plugin Claude conservé |
| **[v3.1.0-beta.1](https://github.com/Tough-Respawn/legal-skills-france/releases/tag/v3.1.0-beta.1)** | Septembre 2026 | Bêta : qualification commune, dix modèles révisés, API Légifrance datée et client Judilibre portable facultatifs |
| **v3.0.3** | Août 2026 | Durcissement : `.env` lu par extraction textuelle, jamais exécuté / Hardening: `.env` parsed textually, never executed |
| **v3.0.2** | Août 2026 | Credentials PISTE via fichier `.env` (+ `.env.example`), tutoriel pas-à-pas d'obtention des clés vérifié en réel / PISTE credentials via `.env` file (+ `.env.example`), step-by-step key setup tutorial verified end-to-end |
| **v3.0.1** | Août 2026 | Citations corrigées et sourcées (audit externe), lint statique, baseline de déclenchement mesurée, workflow Judilibre curl / Verified citations, static lint, measured triggering baseline, curl-based Judilibre workflow |
| **v3.0.0** | Mai 2026 | 8 skills modulaires (1 méta + 7 domaines), 10 modèles de documents, intégration API Judilibre, suite de tests / 8 modular skills, 10 document templates, Judilibre API integration, test suite |
| **v2.0.0** | Mars 2026 | Références enrichies, protocole cas complexes, vérification web obligatoire / Enriched references, complex case protocol, mandatory web verification |
| **v0.1.0** | Février 2026 | Version initiale / Initial release |

---

## Qualité et tests / Quality & tests

> **FR :** Trois niveaux de vérification. **EN:** Three verification layers.

**1. Lint statique / Static lint**

```bash
python tests/lint.py
```

8 contrôles : frontmatters YAML, longueur des descriptions de skills (≤ 1 536 caractères, règle historique du dépôt), manifests JSON + versions synchronisées, mots-clés déclencheurs, motifs interdits (citations corrigées), inventaire `/rediger` ↔ fichiers templates, contrat de template (quatre sections, champs et conditions déclarés), accès à la qualification commune depuis les huit skills. Cette limite historique ne valide pas la conformité au plafond Agent Skills de 1 024 caractères.

**2. Validation du manifest / Manifest validation**

```bash
claude plugin validate plugins/legal-france
```

Note : la validation de la racine du marketplace échoue sur Claude Code ≤ 2.1.104 (`Unrecognized keys: "$schema", "description"`) ; ces clés sont conservées volontairement car acceptées par les versions plus récentes.

**3. Scénarios de déclenchement / Triggering scenarios**

`tests/triggering.md` définit 33 scénarios (positifs, négatifs, borderline, multi-domaines) : chaque phrase est posée en session fraîche et on vérifie quel skill se déclenche. Le déclenchement étant stochastique, mesurez des **taux** sur plusieurs runs plutôt qu'un run unique, et enregistrez modèle, version CLI, version plugin et date avec les résultats. La baseline mesurée du 2026-08-04 (5 runs par scénario) est consignée dans la table Pass/Fail de `tests/triggering.md`.

Scénarios manuels complémentaires : [rédaction](tests/redaction.md) et
[jurisprudence](tests/judilibre.md). Les outils internes d'évaluation,
les quinze scénarios automatisés, leurs tests et les journaux de revue sont
conservés localement dans `evals/`, exclu de Git. Ils ne font pas partie du
plugin distribué ni du dépôt public.

Les résultats ciblés du 10 septembre 2026 précèdent les changements d'accès
aux API. Ils ne démontrent ni une absence de régression du routage sur les
33 scénarios, ni la fiabilité des nouveaux clients. Aucun test n'a été lancé
pour cette passe du 11 septembre, conformément au périmètre choisi.

La v4 ajoute une distribution portable générée depuis la source commune.
Le ZIP et un export civil ont été générés et leurs fichiers relus. Une revue
indépendante communiquée le 12 septembre rapporte des vérifications de
l'installateur et des huit skills, ainsi qu'un chargement et une invocation
explicite dans Claude Code 2.1.251. Ces résultats n'ont pas été rejoués ici.
La vérification complémentaire du 12 septembre rapporte le refus des chemins
Windows trop longs sans fichier partiel, y compris en simulation, et
l'installation de 304 fichiers en chemin court. Elle rapporte aussi la
réussite du lint et de la validation du manifest après ces modifications.
Les douze cas API sont consignés dans le journal local de validation.
Les descriptions du plugin Claude restent inchangées ; celles des paquets
portables sont courtes et leur routage reste à évaluer sans plugin concurrent.
Les autres harnais n'ont pas encore été testés.
Voir [COMPATIBILITY.md](COMPATIBILITY.md) pour les limites par application.

## Chat, API et modèles locaux

Choisissez le harnais qui exécute votre modèle (DeepSeek, Qwen ou autre).
Une interface sans chargeur de skills peut recevoir un export documentaire :

```bash
python scripts/skill.py export --domain civil --output dist/legal-france-civil.md
```

Fournissez le fichier à votre application comme document ou contexte, selon
ses possibilités. L'export ne fournit aucun outil web ni accès à vos fichiers.
Limitez les domaines et vérifiez la capacité de contexte de votre application.

---

## Contribuer / Contributing

La source commune est dans `src/legal-france/`, les métadonnées et la version
dans `project.json`. Modifier ces sources, puis générer le plugin avec
`python scripts/skill.py build --force`. Le dossier `plugins/legal-france/`
est une distribution générée conservée pour les utilisateurs Claude.
Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour le cycle de génération.

**Règle de traçabilité / Traceability rule :** toute citation juridique ajoutée dans `references/` doit être vérifiée sur Legifrance et accompagnée de l'URL de l'article et de la date de vérification (voir le format dans `legal-france-administratif/references/administratif.md`). _Any legal citation added to `references/` must be verified on Legifrance and carry the article URL + verification date._

Pour enrichir les références :
- **Référence d'un domaine spécifique** : ajoutez dans `src/legal-france/skills/legal-france-<domaine>/references/<domaine>.md`.
- **Référence transversale** (procédure, jurisprudence clé, glossaire, codes-index, sources) : ajoutez dans `src/legal-france/skills/legal-france/references/<fichier>.md`.

_To enrich references:_
- _Domain-specific: add to `src/legal-france/skills/legal-france-<domain>/references/<domain>.md`._
- _Cross-cutting: add to `src/legal-france/skills/legal-france/references/<file>.md`._

---

## Avertissement / Disclaimer

> **FR :** Ces informations sont fournies à titre indicatif et ne constituent pas un avis juridique. Les lois et la jurisprudence évoluent constamment. Consultez un avocat qualifié pour votre situation particulière.

> **EN:** This information is provided for educational and research purposes only. It does not constitute legal advice. Laws and case law evolve constantly. Always consult a qualified legal professional for specific situations.

---

## Licence / License

MIT : Copyright (c) 2026 Amine Harrak
