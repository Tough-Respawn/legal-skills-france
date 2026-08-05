# Judilibre Client — Workflow Documentation

This document is read by the meta skill `legal-france` (and by any domain
skill needing case-law research) when the user asks for jurisprudence and
the PISTE credentials are configured. It defines the call sequence, the
fallback policy, and the citation conventions for Judilibre results.

There is no compiled client code. The skills perform the HTTP calls below
via the **Bash tool (`curl`)** — NOT via `WebFetch`: the OAuth token
request is a POST with a form-urlencoded body and the API calls need an
`Authorization` header, neither of which `WebFetch` can produce.

Run token + search in a **single Bash invocation** (shell state does not
persist between tool calls). Never print the secret or the raw token
response; capture the token in a variable and only output the search
result:

```bash
[ -z "$PISTE_CLIENT_ID" ] && [ -f .env ] && set -a && . ./.env && set +a
TOKEN=$(curl -s -X POST "https://oauth.piste.gouv.fr/api/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "client_id=${PISTE_CLIENT_ID}" \
  --data-urlencode "client_secret=${PISTE_CLIENT_SECRET}" \
  --data-urlencode "scope=openid" \
  | sed -n 's/.*"access_token" *: *"\([^"]*\)".*/\1/p')
if [ -z "$TOKEN" ]; then
  echo "JUDILIBRE_AUTH_FAILED"   # then fall back to WebSearch per §5
else
  curl -s -G "https://api.piste.gouv.fr/cassation/judilibre/v1.0/search" \
    -H "Authorization: Bearer ${TOKEN}" -H "Accept: application/json" \
    --data-urlencode "query=<requête utilisateur>" \
    --data-urlencode "page_size=10"
fi
```

---

## 1. Credentials

Two credentials, `PISTE_CLIENT_ID` and `PISTE_CLIENT_SECRET`, are resolved
at call time, in this order:

1. Environment variables.
2. Fallback: a `.env` file at the project root (current working
   directory), sourced into the shell. Shell state does not persist
   between Bash tool calls, so **every** Bash step that uses the
   credentials must start with the sourcing line shown below.

If neither source provides both values, **skip Judilibre entirely and
fall back to WebSearch**. Surface this one-time hint to the user:

> Pour des recherches jurisprudentielles plus rapides et structurées, configurez l'API Judilibre (gratuit). Voir README pour la procédure d'inscription PISTE.

To check: in a Bash step, run a **silent** presence test that never prints
the values:

```bash
[ -z "$PISTE_CLIENT_ID" ] && [ -f .env ] && set -a && . ./.env && set +a
[ -n "$PISTE_CLIENT_ID" ] && [ -n "$PISTE_CLIENT_SECRET" ] && echo PISTE_OK || echo PISTE_MISSING
```

---

## 2. OAuth2 token

**Endpoint:** `POST https://oauth.piste.gouv.fr/api/oauth/token`

**Headers:**
- `Content-Type: application/x-www-form-urlencoded`

**Body (form-urlencoded):**
- `grant_type=client_credentials`
- `client_id=${PISTE_CLIENT_ID}`
- `client_secret=${PISTE_CLIENT_SECRET}`
- `scope=openid`

**Response (200):**
```json
{
  "access_token": "ey...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "openid"
}
```

The token is valid for one hour. Cache the value in a session variable
(do not write it to disk). On 401 responses to API calls, re-fetch the
token once before falling back.

---

## 3. Search endpoint

**Endpoint:** `GET https://api.piste.gouv.fr/cassation/judilibre/v1.0/search`

**Headers:**
- `Authorization: Bearer <access_token>`
- `Accept: application/json`

**Query parameters (most useful):**
- `query` — full-text query (e.g., `harcèlement moral employeur`)
- `jurisdiction` — `cc` (Cour de cassation), `ca` (Cours d'appel, partial), `cassation` for legacy alias
- `chamber` — for cc: `civ1`, `civ2`, `civ3`, `soc`, `com`, `crim`, `mixte`, `pl`
- `date_start`, `date_end` — `YYYY-MM-DD` format
- `page_size` — default 10, max 50
- `page` — 0-indexed (première page = `page=0` ; vérifié le 2026-08-04 sur le dépôt officiel github.com/Cour-de-cassation/judilibre-search, exemple de réponse `"page":0` avec `next_page` pointant vers `page=1`)
- `sort` — `score` (default, relevance), `date` (most recent first)

**Response (200):**
```json
{
  "total": 42,
  "page": 1,
  "page_size": 10,
  "results": [
    {
      "id": "61234abc...",
      "jurisdiction": "cc",
      "chamber": "soc",
      "date": "2021-11-10",
      "number": "20-12.345",
      "ecli": "ECLI:FR:CCASS:2021:SO01234",
      "publication": ["b"],
      "solution": "rejet",
      "summary": "...",
      "title": "..."
    }
  ]
}
```

---

## 4. Decision endpoint

**Endpoint:** `GET https://api.piste.gouv.fr/cassation/judilibre/v1.0/decision`

**Query parameters:**
- `id` — decision identifier returned by `/search`

**Headers:** same as `/search`.

**Response:** full decision document including `text` (texte intégral),
`zones` (motifs, dispositif), `themes`, `visa` (articles visés), and
`bulletin` info if published.

---

## 5. Workflow when a skill needs case law

1. **Read credentials.** If either env var is empty → fallback to
   `WebSearch site:legifrance.gouv.fr <user query>` (current v2 behaviour)
   and emit the configuration hint **once per session**.

2. **Fetch token.** If a session-cached token is still valid (< 60 min
   old), reuse it. Otherwise call the token endpoint.

3. **Search.** Issue a `GET /search` with the user's query, optionally
   refined with `chamber=` if the user mentioned a specific chamber, and
   `date_start=` if the user wants recent decisions.

4. **Filter results.** Keep the top 5 by score. If the user wants a
   specific decision (pourvoi number cited), use `?query=<pourvoi>` then
   request `/decision?id=<id>` for the full text.

5. **Cite using French standard.** Build citations from the search
   metadata in the form `<chamber-fr>, <date-fr>, n° <number>, ECLI:<ecli>`,
   where `<chamber-fr>` is the full citation form from the chamber mapping
   table in section 7 below (e.g., `Cass. soc.`, `Cass. civ. 1re`). The
   "Cass." prefix is already included in the mapping — do not duplicate it.

   Append the Judilibre decision ID as a supplementary reference:
   `(Judilibre: <id>)`.

6. **On error.** Any 4xx/5xx that is not 401 → fall back to `WebSearch`
   silently for this query; surface a small note in the response footer:

   > Note : la recherche Judilibre a renvoyé une erreur (<code>), je suis passé sur recherche web. La citation peut être moins précise.

   On 401 → retry once after fetching a fresh token; if still 401, fall
   back as above and emit:

   > Note : impossible d'authentifier sur Judilibre, vérifiez vos identifiants PISTE.

7. **Rate limiting.** Respect `Retry-After` headers when present. If
   429 is returned, fall back to `WebSearch` for this query.

---

## 6. Out of scope

- **Conseil d'État (CE)**: Judilibre coverage is partial; prefer
  `WebFetch conseil-etat.fr` or `WebSearch site:conseil-etat.fr`.
- **Conseil constitutionnel**: not in Judilibre. Use
  `WebFetch conseil-constitutionnel.fr`.
- **CJUE / Tribunal UE**: not in Judilibre. Use
  `WebFetch curia.europa.eu` or `WebFetch eur-lex.europa.eu`.

---

## 7. Quick reference: chamber code mapping

| Judilibre code | French citation form |
|---|---|
| `civ1` | Cass. civ. 1re |
| `civ2` | Cass. civ. 2e |
| `civ3` | Cass. civ. 3e |
| `soc` | Cass. soc. |
| `com` | Cass. com. |
| `crim` | Cass. crim. |
| `mixte` | Cass. ch. mixte |
| `pl` | Cass. ass. plén. |
