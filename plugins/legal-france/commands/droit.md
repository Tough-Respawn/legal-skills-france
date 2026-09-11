---
description: Ask any question about French law, routes to the right domain automatically
argument-hint: <your legal question>
allowed-tools: [Read, Grep, Glob, Bash, WebSearch, WebFetch]
---

Invoke the `legal-france` meta skill to route the user's question.

## Workflow
1. Detect the legal domain from the question keywords (civil, pénal, travail, affaires, administratif, numérique, européen). If the question is genuinely multi-domain or transversal, stay in the meta skill.
2. If a single domain is identified, load `plugins/legal-france/skills/legal-france-<domain>/references/<domain>.md` (the references now live with each domain skill since v3).
3. Also load `plugins/legal-france/skills/legal-france/references/codes-index.md` for cross-cutting article lookup.
4. Apply the response template matching the user's role (see `plugins/legal-france/skills/legal-france/methodology.md`).
5. Verify the applicable official sources through web search and page reading by default. Use an API only when the user requests it or has already chosen that mode in the session: `lib/legifrance-client.md` for dated texts, `lib/judilibre-client.md` for judicial case law.
6. Cite all sources precisely (article numbers, decision references).
7. End with the mandatory legal disclaimer.
