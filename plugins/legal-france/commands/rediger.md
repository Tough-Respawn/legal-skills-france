---
description: Générer un modèle de document juridique (mise en demeure, lettre de licenciement, plainte, recours, etc.)
argument-hint: "<type-de-document> (ex : mise-en-demeure-caution, lettre-licenciement, plainte-simple, ou aucun pour lister)"
allowed-tools: [Read, Glob, WebFetch, WebSearch]
---

Démarrer le workflow de rédaction documentaire.

## Workflow
1. Lire `plugins/legal-france/lib/redacteur-engine.md` pour le déroulement complet.
2. Si l'argument `<type-de-document>` est absent → lister les templates disponibles (table de la section 2 du fichier engine).
3. Si l'argument est un slug connu → charger le fichier template correspondant.
4. Si l'argument est inconnu → proposer 2-3 templates les plus proches.
5. Suivre les 6 étapes du workflow (questionnaire → vérification Legifrance → génération → disclaimer renforcé → disclaimer standard).
6. Toute citation d'article doit être vérifiée sur Legifrance avant inclusion dans le document final.
