# Judilibre Test Scenarios : legal-france v3

These scenarios verify the Judilibre integration behaviour. To run: configure
credentials when the scenario explicitly chooses the API, then invoke
`/jurisprudence <query>` in a fresh session. The web is now the default;
credentials alone do not activate Judilibre.

---

## Scenario J1 : Auth success path

**Preconditions:**
- `PISTE_CLIENT_ID` and `PISTE_CLIENT_SECRET` are valid.

**Query:** `/jurisprudence Utilise explicitement l’API Judilibre : harcèlement moral employeur`

**Expected:**
- Response cites 3-5 Cass. soc. decisions.
- Each citation has the format `Cass. soc., <date>, n° <pourvoi> (Judilibre: <id>)`.
- No fallback hint in the footer.

---

## Scenario J2 : Auth missing path

**Preconditions:**
- `PISTE_CLIENT_ID` and `PISTE_CLIENT_SECRET` are unset.

**Query:** `/jurisprudence Cass. ass. plén., 22 décembre 2023, n° 20-20.648`.

**Expected:**
- Rechercher la décision dans les sources officielles accessibles, distinguer texte consulté et extrait de recherche, signaler les limites.
- Response uses Legifrance-style citations (no Judilibre ID).
- Le mode web ne demande pas de compte ou de configuration PISTE et ne lance
  pas le client Python. Une erreur web seule ne doit pas activer l'API.

---

## Scenario J3 : Auth invalid creds

**Preconditions:**
- `PISTE_CLIENT_ID` set to a bogus value (e.g., `INVALID`).
- `PISTE_CLIENT_SECRET` set to a bogus value.

**Query:** `/jurisprudence Utilise explicitement l’API Judilibre : harcèlement moral employeur`

**Expected:**
- Échec OAuth signalé sans imprimer de secret ni de jeton, puis repli web.
- Le renouvellement unique concerne un 401 de l'appel métier après obtention
  d'un jeton, pas une boucle sur des identifiants OAuth invalides.

---

## Scenario J4 : Decision lookup by pourvoi

**Preconditions:**
- Valid credentials.

**Query:** `/jurisprudence Utilise l’API Judilibre : Cass. soc. 25 novembre 2020 n° 19-13.340`

**Expected:**
- Single decision returned via `/search?query=19-13.340` then `/decision?id=...`.
- Response includes the decision summary, the solution (rejet/cassation), and the visa.

---

## Scenario J5 : Out-of-scope jurisdiction (Conseil d'État)

**Preconditions:**
- Aucun identifiant requis pour la recherche web officielle.

**Query:** `/jurisprudence CE Ass., 20 octobre 1989, Nicolo`.

**Expected:**
- Skill recognizes this is Conseil d'État.
- Consulte une source officielle du Conseil d’État ou Légifrance ; aucun appel Judilibre pour cette juridiction.
- Response cites in `CE, date, n° req, nom` format (no Judilibre ID).

---

## Pass/Fail record

| Date | Scenario | Pass/Fail | Notes |
|---|---|---|---|
| 2026-09-10 | J2, J5 | PASS ciblé après autorisation | Deux exécutions complètes valides : sources web officielles consultées, limites signalées, aucun appel ni identifiant Judilibre inventé. Traces et revue conservées localement dans `evals/` ; mesure antérieure au nouveau client et au mode web prioritaire. |
| 2026-09-10 | J1, J3, J4 | NON EXÉCUTÉ | Aucun nouveau contrôle des appels API Judilibre avec identifiants réels ou invalides ; client Python ajouté ensuite, non exécuté. |


La vérification documentaire ne vaut pas réussite de l'intégration. Les
mesures du 10 septembre portent sur le parcours web d'alors ; le nouveau
client Python et la priorité web/API du 11 septembre n'ont pas été testés.
Les scénarios nécessitant l'API demandent une session capable d'exécuter le
client. Consigner séparément les statuts HTTP, la source effective, la citation
et les limites ; ne jamais conserver de secrets dans les traces. L'outillage
et les journaux internes restent dans `evals/`, exclu de Git.
