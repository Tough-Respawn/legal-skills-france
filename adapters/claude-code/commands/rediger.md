---
description: Générer un modèle de document juridique (mise en demeure, lettre de licenciement, plainte, recours, etc.)
argument-hint: "<type-de-document> (ex : mise-en-demeure-caution, lettre-licenciement, plainte-simple, ou aucun pour lister)"
allowed-tools: [Read, Glob, Bash, WebFetch, WebSearch]
---

For an explicitly chosen API lookup, follow the direct API route at the start
of `skills/legal-france/SKILL.md` before the general research workflow below.

Démarrer le workflow de rédaction documentaire.

## Workflow
1. Lire `lib/redacteur-engine.md` pour le déroulement complet.
2. Si l'argument `<type-de-document>` est absent → lister les templates disponibles (table de la section 2 du fichier engine).
3. Si l'argument est un slug connu → charger le fichier template correspondant.
4. Si l'argument est inconnu → proposer 2-3 templates les plus proches.
5. Suivre les 6 étapes du workflow (qualification et pièces → vérification de la version applicable et calculs → génération → disclaimer renforcé → disclaimer standard).
6. Vérifier les sources officielles dans la version applicable aux faits avant finalisation. Une inconnue décisive impose une question ciblée ou un brouillon explicitement incomplet.
