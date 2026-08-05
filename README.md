# legal-france — Plugin Claude Code pour le droit français / French Law Plugin for Claude Code

> **FR :** Assistant juridique français pour Claude Code — 8 skills modulaires auto-déclenchants, 10 modèles de documents juridiques, intégration jurisprudence Cour de cassation (Judilibre).
> **EN:** French law assistant for Claude Code — 8 modular auto-triggering skills, 10 legal document templates, Cour de cassation case-law integration (Judilibre).

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

- **Avocat / Magistrat** — Format consultation juridique structurée / Structured legal consultation
- **Étudiant en droit** — Cas pratique, commentaire d'arrêt / Case analysis, case commentary
- **Citoyen** _(défaut / default)_ — Langage clair, démarches pratiques / Plain language, practical steps
- **Entreprise** — Conformité, analyse de documents / Compliance, document analysis

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

Invocation : `/rediger <type>` (ex : `/rediger lettre-licenciement`). Le rédacteur pose 5 à 15 questions ciblées, vérifie les articles cités sur Legifrance, puis génère le document avec une checklist de vérifications à effectuer avant envoi.

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
- `skills/legal-france/references/jurisprudence-cle.md` — 96 décisions clés / 96 landmark decisions
- `skills/legal-france/references/glossaire.md` — ~170 termes / ~170 terms
- `skills/legal-france/references/codes-index.md` — Index des codes français / Index of French legal codes
- `skills/legal-france/references/sources.md` — Sources officielles / Official sources

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

## Configuration Judilibre (optionnelle) / Judilibre setup (optional)

> **FR :** Pour des recherches jurisprudentielles structurées via l'API officielle de la Cour de cassation. Gratuit. Sans cette config, le plugin retombe automatiquement sur les recherches web Legifrance.
> **EN:** For structured case-law search via the official Cour de cassation API. Free of charge. Without this setup, the plugin transparently falls back to Legifrance web search.

### Étape 1 — Obtenir vos identifiants PISTE (pas-à-pas)

Parcours complet vérifié en conditions réelles le 2026-08-05. Comptez 10 minutes. Référence générale : [guide officiel PISTE](https://piste.gouv.fr/help-center/guide).

1. **Créer un compte** sur [piste.gouv.fr](https://piste.gouv.fr/registration), activer via le lien reçu par mail, se connecter.
2. **Accepter les CGU Judilibre** : menu **API → Consentement CGU API** → chercher « Judilibre » → accepter pour l'environnement **PRODUCTION**. Ne sautez pas cette étape : tant que les CGU ne sont pas validées, la case Judilibre reste grisée à l'étape 4 (c'est la cause n° 1 des blocages, [confirmée par la FAQ de l'API Légifrance](https://www.legifrance.gouv.fr/contenu/pied-de-page/foire-aux-questions-api) qui suit le même mécanisme). L'ancienne URL directe `/api-fr/consentement-cgu-api-fr` citée par de vieilles docs renvoie une 404 : passez par le menu.
3. **Créer une application de PRODUCTION** : menu **APPLICATIONS → Créer une application**. N'utilisez pas l'application `APP_SANDBOX_<votre-email>` créée automatiquement à l'inscription : le plugin appelle les URL Production (`oauth.piste.gouv.fr`), une app Sandbox échouera avec `invalid_client`.
4. **Souscrire à Judilibre** : sur votre application → « Modifier l'application » → dans la liste des API, cocher la ligne **JUDILIBRE / environnement PRODUCTION** → « Appliquer les modifications ».
5. **Générer et lire les identifiants OAuth** : onglet **Authentification** de l'application, section **« Identifiants Oauth »** (PAS la section « API Keys » au-dessus : autre méthode d'authentification, inutilisée par le plugin). Si le tableau est vide, cliquez « Générer » (type « Confidentiel », URL de rappel et certificat X.509 laissés vides). Puis :
   - **Client ID** = la valeur affichée dans la colonne « Client ID » du tableau ;
   - **Client Secret** = la valeur cachée derrière « **Consulter le client secret** » sur la même ligne.

   Attention à ne pas inverser les deux : un couple mélangé (ou pris pour moitié sur les API Keys) donne `invalid_client` sur `oauth.piste.gouv.fr`.

### Étape 2 — Définir deux variables d'environnement

**Choisissez l'option qui correspond à votre setup** — une seule des trois suffit :

##### Option A — Fichier `.env` à la racine du projet (le plus simple à gérer)

Créez un fichier nommé `.env` **directement dans le dossier que vous ouvrez avec Claude Code** : peu importe lequel, c'est simplement le dossier de travail de votre session (celui affiché quand vous lancez `claude`). Un modèle est fourni avec le plugin (`.env.example`). Contenu, deux lignes :

```bash
PISTE_CLIENT_ID=votre_client_id
PISTE_CLIENT_SECRET=votre_client_secret
```

Ajoutez `.env` à votre `.gitignore` si le dossier est un dépôt Git. Le client Judilibre lit automatiquement les deux clés quand les variables d'environnement sont absentes (extraction textuelle uniquement, le fichier n'est jamais exécuté).

> **Piège Windows** : en enregistrant depuis le Bloc-notes, choisissez « Tous les fichiers » comme type, sinon le fichier s'appelle `.env.txt` et ne sera pas trouvé.

##### Option B — Settings Claude Code (persiste, marche dans tous les projets)

Ouvrez `~/.claude/settings.json` (Linux/macOS) ou `%USERPROFILE%\.claude\settings.json` (Windows) et ajoutez le bloc `env` :

```json
{
  "env": {
    "PISTE_CLIENT_ID": "votre_client_id",
    "PISTE_CLIENT_SECRET": "votre_client_secret"
  }
}
```

Si le fichier contient déjà d'autres clés, fusionnez le bloc `env` avec l'existant. Pas besoin de relancer le terminal — relancez juste la session Claude Code.

##### Option C — Variables d'environnement système (persistent globalement, utile si vous utilisez les creds avec d'autres outils)

**Linux / macOS** — ajoutez à la fin de `~/.bashrc`, `~/.zshrc` ou `~/.profile` :
```bash
export PISTE_CLIENT_ID="votre_client_id"
export PISTE_CLIENT_SECRET="votre_client_secret"
```
Puis `source ~/.bashrc` (ou rouvrez votre terminal).

**Windows** — méthode graphique :
1. Touche Windows → tapez "variables d'environnement" → ouvrir.
2. Cliquez "Variables d'environnement" → section "Variables utilisateur" → "Nouveau".
3. Créez `PISTE_CLIENT_ID` et `PISTE_CLIENT_SECRET` avec vos valeurs.
4. Rouvrez Claude Code (les variables sont lues au démarrage).

### Étape 3 — Vérifier

Invoquez `/jurisprudence harcèlement moral`. Si les citations sortent au format `Cass. soc., date, n° pourvoi (Judilibre: id)`, c'est bon. Sinon le footer indique pourquoi (variables non détectées, erreur d'auth, app Sandbox au lieu de Production).

> **Sécurité** : ne commitez jamais vos credentials dans un repo Git. PISTE recommande de régénérer le `client_secret` tous les 3 mois.

---

## Versions

| Version | Date | Description |
|---------|------|-------------|
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

7 contrôles : frontmatters YAML, longueur des descriptions de skills (≤ 1 536 caractères), manifests JSON + versions synchronisées, mots-clés déclencheurs, motifs interdits (citations corrigées), inventaire `/rediger` ↔ fichiers templates, contrat de template (clés + 3 sections obligatoires).

**2. Validation du manifest / Manifest validation**

```bash
claude plugin validate plugins/legal-france
```

Note : la validation de la racine du marketplace échoue sur Claude Code ≤ 2.1.104 (`Unrecognized keys: "$schema", "description"`) ; ces clés sont conservées volontairement car acceptées par les versions plus récentes.

**3. Scénarios de déclenchement / Triggering scenarios**

`tests/triggering.md` définit 33 scénarios (positifs, négatifs, borderline, multi-domaines) : chaque phrase est posée en session fraîche et on vérifie quel skill se déclenche. Le déclenchement étant stochastique, mesurez des **taux** sur plusieurs runs plutôt qu'un run unique, et enregistrez modèle, version CLI, version plugin et date avec les résultats. La baseline mesurée du 2026-08-04 (5 runs par scénario) est consignée dans la table Pass/Fail de `tests/triggering.md`.

Scénarios manuels complémentaires : `tests/redaction.md` (10 modèles), `tests/judilibre.md` (API).

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

MIT — Copyright (c) 2026 Amine Harrak
