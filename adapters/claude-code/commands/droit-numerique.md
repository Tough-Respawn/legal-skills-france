---
description: French digital law and data protection, GDPR/RGPD, CNIL, privacy, e-commerce
argument-hint: <your digital-law question>
allowed-tools: [Read, Grep, Glob, Bash, WebSearch, WebFetch]
---

For an explicitly chosen API lookup, follow the direct API route at the start
of `skills/legal-france/SKILL.md` before the general research workflow below.

Invoke the `legal-france-numerique` skill to answer the user's question.

## Workflow
1. Load the domain skill's references at `plugins/legal-france/skills/legal-france-numerique/references/numerique.md`
2. Also load `plugins/legal-france/skills/legal-france/references/codes-index.md` for cross-cutting article lookup
3. Apply the response template matching the user's role per `plugins/legal-france/skills/legal-france/methodology.md`
4. Verify the applicable official sources through web search and page reading by default. Use an API only when the user requests it or has already chosen that mode in the session: `lib/legifrance-client.md` for dated texts, `lib/judilibre-client.md` for judicial case law.
5. Cite all sources precisely (article numbers, decision references)
6. End with the mandatory legal disclaimer
