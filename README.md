# legal-france : Plugin Claude Code pour le droit français / French Law Plugin for Claude Code

> **FR :** Assistant juridique français pour Claude Code, 8 skills modulaires auto-déclenchants, 10 modèles de documents juridiques, intégration jurisprudence Cour de cassation (Judilibre).
> **EN:** French law assistant for Claude Code, 8 modular auto-triggering skills, 10 legal document templates, Cour de cassation case-law integration (Judilibre).

---

## Installation

```bash
claude plugin install legal-france
```

---

## Commandes / Commands

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

Le plugin détecte automatiquement votre profil et adapte sa réponse :
_The plugin auto-detects your profile and adapts its response:_

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

Invocation : `/rediger <type>` (ex : `/rediger lettre-licenciement`). Le rédacteur recueille les seuls faits décisifs absents et les pièces utiles, puis les coordonnées nécessaires. Il vérifie le régime et la version des textes applicables, expose les calculs possibles et génère le document avec une checklist. Les inconnues décisives restent visibles dans un brouillon incomplet ; aucune date ni formalité accomplie n’est inventée.

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
- `skills/legal-france/references/jurisprudence-cle.md` : 96 décisions clés / 96 landmark decisions
- `skills/legal-france/references/glossaire.md` : ~170 termes / ~170 terms
- `skills/legal-france/references/codes-index.md` : Index des codes français / Index of French legal codes
- `skills/legal-france/references/sources.md` : Sources officielles / Official sources

Tous les chemins sont relatifs à `plugins/legal-france/`.

---

## Indicateurs de progression / Progress Indicators

Le plugin affiche les étapes en temps réel pendant le traitement :
_The plugin displays real-time step indicators while processing:_

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
Python n'est requis que pour l'option API. Si ce mode est indisponible, le
skill poursuit avec les pages officielles et signale la limite.

### Étape 1 : Obtenir vos identifiants PISTE (pas-à-pas)

Le parcours d'inscription PISTE et d'abonnement Judilibre a été vérifié le 2026-08-05, avec l'ancien client curl. Cette vérification historique ne valide pas les clients Python actuels. L'ajout de Légifrance a été documenté le 2026-09-11, sans appel métier authentifié. Référence générale : [guide officiel PISTE](https://piste.gouv.fr/help-center/guide).

1. **Créer un compte** sur [piste.gouv.fr](https://piste.gouv.fr/registration), activer via le lien reçu par mail, se connecter.
2. **Accepter les CGU de l’API choisie** : menu **API → Consentement CGU API** → chercher « Judilibre » ou « Légifrance » → accepter pour l’environnement **PRODUCTION**. Ne sautez pas cette étape : tant que les CGU ne sont pas validées, la case Judilibre reste grisée à l'étape 4 (c'est la cause n° 1 des blocages, [confirmée par la FAQ de l'API Légifrance](https://www.legifrance.gouv.fr/contenu/pied-de-page/foire-aux-questions-api) qui suit le même mécanisme). L'ancienne URL directe `/api-fr/consentement-cgu-api-fr` citée par de vieilles docs renvoie une 404 : passez par le menu.
3. **Créer une application de PRODUCTION** : menu **APPLICATIONS → Créer une application**. N'utilisez pas l'application `APP_SANDBOX_<votre-email>` créée automatiquement à l'inscription : le plugin appelle les URL Production (`oauth.piste.gouv.fr`), une app Sandbox échouera avec `invalid_client`.
4. **Souscrire à l’API choisie** : sur votre application → « Modifier l’application » → dans la liste des API, cocher **JUDILIBRE** et/ou **Légifrance stable**, en **PRODUCTION** → « Appliquer les modifications ». Une seule souscription suffit si vous n’utilisez qu’une API.
5. **Générer et lire les identifiants OAuth** : onglet **Authentification** de l'application, section **« Identifiants Oauth »** (PAS la section « API Keys » au-dessus : autre méthode d'authentification, inutilisée par le plugin). Si le tableau est vide, cliquez « Générer » (type « Confidentiel », URL de rappel et certificat X.509 laissés vides). Puis :
   - **Client ID** = la valeur affichée dans la colonne « Client ID » du tableau ;
   - **Client Secret** = la valeur cachée derrière « **Consulter le client secret** » sur la même ligne.

   Attention à ne pas inverser les deux : un couple mélangé (ou pris pour moitié sur les API Keys) donne `invalid_client` sur `oauth.piste.gouv.fr`.

### Ajouter Légifrance si vous choisissez cette API

Si votre application est déjà configurée pour Judilibre, acceptez aussi
les CGU Légifrance et ajoutez **Légifrance stable / PRODUCTION** aux accès
de votre application. Un compte PISTE ou un abonnement Judilibre seul ne donne
pas nécessairement cet accès. La DILA décrit l'accès sur sa
[page API officielle](https://www.legifrance.gouv.fr/contenu/pied-de-page/open-data-et-api).

### Étape 2 : Définir les identifiants facultatifs

**Le fichier `.env` est facultatif.** Si les identifiants sont déjà définis
dans les variables d'environnement de votre session, vous pouvez utiliser
l'API sans créer ce fichier. Les variables d'environnement ont priorité
sur les valeurs du `.env`.

Choisissez l'une des trois méthodes ci-dessous : une seule suffit.

##### Option A : Fichier `.env` à la racine du projet (le plus simple à gérer)

Créez un fichier nommé `.env` **directement dans le dossier que vous ouvrez avec Claude Code** : peu importe lequel, c'est simplement le dossier de travail de votre session (celui affiché quand vous lancez `claude`). Un modèle est fourni avec le plugin (`.env.example`). Contenu, deux lignes :

```bash
PISTE_CLIENT_ID=votre_client_id
PISTE_CLIENT_SECRET=votre_client_secret
```

Ajoutez `.env` à votre `.gitignore` si le dossier est un dépôt Git. Après activation explicite du mode API, le client lit les clés manquantes dans l’environnement depuis ce fichier, textuellement et sans l’exécuter. Si les deux API partagent la même application, ce couple commun suffit. Sinon, utilisez les couples spécifiques `LEGIFRANCE_CLIENT_ID` / `LEGIFRANCE_CLIENT_SECRET` et `JUDILIBRE_CLIENT_ID` / `JUDILIBRE_CLIENT_SECRET` du modèle `.env.example`. Renseignez les deux valeurs de chaque couple utilisé.

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
4. Rouvrez Claude Code (les variables sont lues au démarrage).

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
et [Judilibre](plugins/legal-france/lib/judilibre-client.md). Le fonctionnement
des clients Python avec des identifiants valides n'est pas encore démontré.
Les vérifications de cas d'erreur ou sur données synthétiques ne remplacent
pas cette validation.

> **Sécurité** : ne commitez jamais vos identifiants ; le fichier `.env` est ignoré par Git.

---

## Versions

| Version | Date | Description |
|---------|------|-------------|
| **v3.1.0-beta.1** | Septembre 2026 | Bêta : qualification commune, dix modèles révisés, API Légifrance datée et client Judilibre portable facultatifs |
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

Le protocole juridique et le client Python ne dépendent pas d'un modèle.
La distribution reste celle du plugin existant ; aucun support universel
des harnais n'est revendiqué et les descriptions restent inchangées.

---

## Contribuer / Contributing

**Règle de traçabilité / Traceability rule :** toute citation juridique ajoutée dans `references/` doit être vérifiée sur Legifrance et accompagnée de l'URL de l'article et de la date de vérification (voir le format dans `legal-france-administratif/references/administratif.md`). _Any legal citation added to `references/` must be verified on Legifrance and carry the article URL + verification date._

Pour enrichir les références :
- **Référence d'un domaine spécifique** : ajoutez dans `plugins/legal-france/skills/legal-france-<domaine>/references/<domaine>.md` (par exemple `legal-france-travail/references/travail.md`).
- **Référence transversale** (procédure, jurisprudence clé, glossaire, codes-index, sources) : ajoutez dans `plugins/legal-france/skills/legal-france/references/<fichier>.md`.

_To enrich references:_
- _Domain-specific: add to `plugins/legal-france/skills/legal-france-<domain>/references/<domain>.md`._
- _Cross-cutting (procedure, key case law, glossary, codes-index, sources): add to `plugins/legal-france/skills/legal-france/references/<file>.md`._

---

## Avertissement / Disclaimer

> **FR :** Ces informations sont fournies à titre indicatif et ne constituent pas un avis juridique. Les lois et la jurisprudence évoluent constamment. Consultez un avocat qualifié pour votre situation particulière.

> **EN:** This information is provided for educational and research purposes only. It does not constitute legal advice. Laws and case law evolve constantly. Always consult a qualified legal professional for specific situations.

---

## Licence / License

MIT : Copyright (c) 2026 Amine Harrak
