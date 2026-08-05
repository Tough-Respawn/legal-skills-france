# Judilibre Test Scenarios : legal-france v3

These scenarios verify the Judilibre integration behaviour. To run: configure
credentials (or unset them, depending on the test), then invoke
`/jurisprudence <query>` in a fresh Claude Code session.

---

## Scenario J1 : Auth success path

**Preconditions:**
- `PISTE_CLIENT_ID` and `PISTE_CLIENT_SECRET` are valid.

**Query:** `/jurisprudence harcèlement moral employeur`

**Expected:**
- Response cites 3-5 Cass. soc. decisions.
- Each citation has the format `Cass. soc., <date>, n° <pourvoi> (Judilibre: <id>)`.
- No fallback hint in the footer.

---

## Scenario J2 : Auth missing path

**Preconditions:**
- `PISTE_CLIENT_ID` and `PISTE_CLIENT_SECRET` are unset.

**Query:** `/jurisprudence harcèlement moral employeur`

**Expected:**
- Response uses Legifrance-style citations (no Judilibre ID).
- Response footer contains the one-time hint:
  > Pour des recherches jurisprudentielles plus rapides et structurées, configurez l'API Judilibre (gratuit). Voir README pour la procédure d'inscription PISTE.

---

## Scenario J3 : Auth invalid creds

**Preconditions:**
- `PISTE_CLIENT_ID` set to a bogus value (e.g., `INVALID`).
- `PISTE_CLIENT_SECRET` set to a bogus value.

**Query:** `/jurisprudence harcèlement moral employeur`

**Expected:**
- One auth attempt fails (401), one retry fails too.
- Response falls back to Legifrance.
- Footer contains:
  > Note : impossible d'authentifier sur Judilibre, vérifiez vos identifiants PISTE.

---

## Scenario J4 : Decision lookup by pourvoi

**Preconditions:**
- Valid credentials.

**Query:** `/jurisprudence Cass. soc. 25 novembre 2020 n° 19-13.340`

**Expected:**
- Single decision returned via `/search?query=19-13.340` then `/decision?id=...`.
- Response includes the decision summary, the solution (rejet/cassation), and the visa.

---

## Scenario J5 : Out-of-scope jurisdiction (Conseil d'État)

**Preconditions:**
- Valid credentials.

**Query:** `/jurisprudence CE 8 avril 2009 Mme Betrisey`

**Expected:**
- Skill recognizes this is Conseil d'État.
- Uses `WebFetch conseil-etat.fr` (not Judilibre).
- Response cites in `CE, date, n° req, nom` format (no Judilibre ID).

---

## Pass/Fail record

| Date | Scenario | Pass/Fail | Notes |
|---|---|---|---|
| _ | _ | _ | _ |
