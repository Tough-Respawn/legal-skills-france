---
description: French criminal law, offenses, penalties, criminal procedure, garde a vue
argument-hint: <your criminal-law question>
allowed-tools: [Read, Grep, Glob, WebSearch, WebFetch]
---

Invoke the `legal-france-penal` skill to answer the user's question.

## Workflow
1. Load the domain skill's references at `plugins/legal-france/skills/legal-france-penal/references/penal.md`
2. Also load `plugins/legal-france/skills/legal-france/references/codes-index.md` for cross-cutting article lookup
3. Apply the response template matching the user's role per `plugins/legal-france/skills/legal-france/methodology.md`
4. If embedded references are insufficient, use WebSearch to query Legifrance (and Judilibre for case law when PISTE creds are configured : see `plugins/legal-france/lib/judilibre-client.md`)
5. Cite all sources precisely (article numbers, decision references)
6. End with the mandatory legal disclaimer
