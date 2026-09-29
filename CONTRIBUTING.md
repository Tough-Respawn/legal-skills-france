# Maintenir la source commune

| Emplacement | Rôle |
|---|---|
| `project.json` | Nom, version et métadonnées communes |
| `.env.example` | Modèle API vide, source unique |
| `src/legal-france/skills/` | Instructions, descriptions courtes, références, modèles et client API |
| `src/legal-france/lib/` | Contrats de rédaction et d'accès aux API |
| `src/legal-france/runtime.md` | Choix web/API et capacités communes, injectés dans les huit skills |
| `adapters/claude-code/` | Commandes natives et frontmatters historiques Claude |
| `scripts/claude_adapter.py` | Génération et gestion de l'installation native Claude |
| `plugins/legal-france/` | Distribution Claude générée, conservée à son emplacement historique |
| `dist/` | Archives et exports générés, exclus de Git |

Modifier les sources, puis régénérer les distributions. Ne pas corriger à la
main les copies dans `plugins/legal-france/` ou `dist/`. Le contenu juridique
est maintenu une seule fois. Chaque citation ajoutée doit être vérifiée sur
une source officielle avec son URL et sa date de vérification.

```bash
python scripts/skill.py build --force
python scripts/skill.py package --output dist/legal-france-skills.zip --force
python scripts/skill.py package-claude-ai --output dist/legal-france-claude-ai.zip --force
python scripts/skill.py export --domain civil --output dist/legal-france-civil.md --force
```

`build` génère le plugin et le marketplace depuis `project.json`, la source
commune et l'adaptateur Claude. Les sorties restent versionnées pour que le
marketplace historique puisse les installer sans étape de génération locale.
`package` et `install` pour les autres harnais lisent directement la source
commune. Les parcours API s'appuient sur le même client Python.

## Publier une version

1. Mettre à jour `version` dans `project.json` et `CHANGELOG.md`, puis
   lancer `build --force` et le lint.
2. Commiter, puis pousser un tag identique à la version : `git tag v4.2.0`
   et `git push origin v4.2.0`.
3. Le workflow `.github/workflows/release-assets.yml` vérifie que le tag
   correspond à `project.json`, relance le lint, construit
   `legal-france-skills.zip` et `legal-france-claude-ai.zip` depuis la source,
   puis les joint à la release du tag (créée si absente).

Les noms des archives ne changent pas d'une version à l'autre : les liens
`releases/latest/download/...` des guides pointent ainsi toujours vers la
dernière version. Le numéro est inscrit dans le SKILL.md de chaque archive.

## Descriptions

Les descriptions courtes sont dans les frontmatters des SKILL.md sources,
sous forme de chaînes JSON compatibles YAML. Les frontmatters Claude d'origine
sont conservés dans `adapters/claude-code/legacy-frontmatter.json` afin de ne
modifier ni leurs noms ni leurs descriptions de déclenchement sans mesure.
Cette exception de compatibilité reste explicite ; le reste du contenu est commun.

Vérifier les changements selon leur portée et les consignes de la session.
Le lint existant et la validation Claude concernent la distribution générée.
Les journaux et outils internes restent dans `evals/`, ignoré par Git.
Une génération réussie ne mesure pas le routage d'un modèle ou l'installation
native d'une application ; consigner ces résultats séparément.
