---
description: Search French case law, landmark decisions, and jurisprudential trends
argument-hint: <search terms, article number, or legal topic>
allowed-tools: [Read, Grep, Glob, Bash, WebSearch, WebFetch]
---

Invoke the `legal-france` meta skill to research case law.

## Workflow
1. If Judilibre was explicitly chosen, read the usage section of
   `lib/judilibre-client.md` and call `skills/legal-france/scripts/legal_api.py`
   with --use-api and the supplied query or decision ID. Use the absolute script
   path from the loaded plugin. Do not search the web first or read credentials.
2. Otherwise, search and read official web sources. Credentials alone never
   activate the API.
3. If that API path is unavailable, continue with the official web sources
   and state the limitation. In ordinary web mode, do not ask for PISTE setup.
4. For Conseil d'État, Conseil constitutionnel, or EU courts, use the relevant
   official web source rather than Judilibre.
5. Read the decision before stating its reasoning as verified. Cite in French
   standard format, adding a Judilibre ID only if actually returned by the API.
6. End with the mandatory legal disclaimer.
