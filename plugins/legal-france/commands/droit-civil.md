---
description: French civil law, contracts, liability, property, family, inheritance
argument-hint: <your civil-law question>
allowed-tools: [Read, Grep, Glob, Bash, WebSearch, WebFetch]
---

Invoke the `legal-france-civil` skill to answer the user's question.

## Workflow
1. Load the domain skill's references at `plugins/legal-france/skills/legal-france-civil/references/civil.md`
2. Also load `plugins/legal-france/skills/legal-france/references/codes-index.md` for cross-cutting article lookup
3. Apply the response template matching the user's role per `plugins/legal-france/skills/legal-france/methodology.md`
4. Verify the applicable official sources through web search and page reading by default. Use an API only when the user requests it or has already chosen that mode in the session: `lib/legifrance-client.md` for dated texts, `lib/judilibre-client.md` for judicial case law.
5. Cite all sources precisely (article numbers, decision references)
6. End with the mandatory legal disclaimer
