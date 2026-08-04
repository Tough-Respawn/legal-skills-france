---
description: Search French case law, landmark decisions, and jurisprudential trends
argument-hint: <search terms, article number, or legal topic>
allowed-tools: [Read, Grep, Glob, Bash, WebSearch, WebFetch]
---

Invoke the `legal-france` meta skill to research case law.

## Workflow
1. Read `plugins/legal-france/lib/judilibre-client.md` for the call
   workflow and chamber mapping.
2. Check `PISTE_CLIENT_ID` and `PISTE_CLIENT_SECRET` environment
   variables.
3. If both are set → prefer Judilibre (call token, then search, then
   optionally decision endpoint).
4. If either is missing → fall back to `WebSearch site:legifrance.gouv.fr`
   AND emit the one-time configuration hint.
5. For Conseil d'État, Conseil constitutionnel, or CJUE results → use
   `WebFetch` against the relevant primary source (not Judilibre).
6. Always cite in French standard format; append the Judilibre decision
   ID when applicable.
7. End with the mandatory legal disclaimer.
