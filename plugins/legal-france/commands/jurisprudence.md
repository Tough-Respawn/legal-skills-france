---
description: Search French case law, landmark decisions, and jurisprudential trends
argument-hint: <search terms, article number, or legal topic>
allowed-tools: [Read, Grep, Glob, Bash, WebSearch, WebFetch]
---

Invoke the `legal-france` meta skill to research case law.

## Workflow
1. Search and read the relevant official web sources by default.
2. If the user explicitly requests Judilibre, or has already chosen that mode
   in the session, read `lib/judilibre-client.md` and use the portable client.
   Credentials alone never activate the API.
3. If that API path is unavailable, continue with the official web sources
   and state the limitation. In ordinary web mode, do not ask for PISTE setup.
4. For Conseil d'État, Conseil constitutionnel, or EU courts, use the relevant
   official web source rather than Judilibre.
5. Read the decision before stating its reasoning as verified. Cite in French
   standard format, adding a Judilibre ID only if actually returned by the API.
6. End with the mandatory legal disclaimer.
