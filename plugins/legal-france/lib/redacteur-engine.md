# Rédacteur Engine : Workflow Documentation

This document is read by any skill that needs to produce a legal document
(letter, mise en demeure, plainte, recours, statuts, etc.). It defines the
six-step workflow, the template contract, and the reinforced disclaimer.

There is no compiled engine code. Skills perform the workflow by reading
templates and asking the user questions.

---

## 1. Trigger

Drafting is triggered by either:

- The `/rediger <type>` slash command (preferred : explicit).
- An implicit phrasing like "rédige-moi", "écris-moi", "fais-moi un
  modèle de", "j'ai besoin d'une lettre pour…", followed by a document
  type the matcher recognizes.

When triggered without an explicit `<type>`, list the available templates
to the user grouped by domain, then resume once they pick one.

---

## 2. Template inventory

| `<type>` slug | Domain skill | Template file path |
|---|---|---|
| `mise-en-demeure-generique` | meta | `skills/legal-france/templates/mise-en-demeure-generique.md` |
| `attestation-honneur` | meta | `skills/legal-france/templates/attestation-honneur.md` |
| `mise-en-demeure-caution` | civil | `skills/legal-france-civil/templates/mise-en-demeure-caution.md` |
| `lettre-licenciement` | travail | `skills/legal-france-travail/templates/lettre-licenciement.md` |
| `rupture-conventionnelle` | travail | `skills/legal-france-travail/templates/rupture-conventionnelle.md` |
| `lettre-demission` | travail | `skills/legal-france-travail/templates/lettre-demission.md` |
| `plainte-simple` | penal | `skills/legal-france-penal/templates/plainte-simple.md` |
| `contestation-amende` | penal | `skills/legal-france-penal/templates/contestation-amende.md` |
| `recours-gracieux` | administratif | `skills/legal-france-administratif/templates/recours-gracieux.md` |
| `mentions-legales-et-confidentialite` | numerique | `skills/legal-france-numerique/templates/mentions-legales-et-confidentialite.md` |

---

## 3. Template contract

Each template file has YAML frontmatter with:

- `type` : the slug shown above.
- `domain` : `meta` | `civil` | `travail` | `penal` | `affaires` | `administratif` | `numerique` | `europeen`.
- `short_description` : one-line summary shown to the user.
- `required_fields` : list of field names the user must provide.
- `optional_fields` : list of field names the engine asks about but accepts skipping.
- `applicable_law` : list of statute citations the engine MUST verify on Legifrance before output.
- `disclaimer_level` : `standard` | `high`. `high` adds the reinforced disclaimer (used for all v3 templates).

Below the frontmatter, three required sections:

1. `## Questionnaire` : numbered list of questions to ask, in order. Each
   question can be ALL CAPS to indicate a required field, or italicized to
   indicate optional. Conditional questions begin with `*Si…* :`.
2. `## Template` : the document body using `{{field_name}}` placeholders
   and conditional blocks `{{#if optional_field}}…{{/if}}`.
3. `## Vérifications juridiques avant envoi` : checklist of points to
   verify against Legifrance + practical advice (delays, send-by method,
   pièces jointes).

---

## 4. Workflow

### Step 1 : Resolve template

If `/rediger` invoked without args → list available templates.
If invoked with an unknown slug → suggest 2-3 closest matches.
Once resolved, `Read` the template file.

### Step 2 : Ask the questionnaire

Iterate the `## Questionnaire` items one at a time. Wait for the user's
answer before asking the next. Keep questions short and concrete. If an
answer is ambiguous, ask one short follow-up before continuing.

For numerical or date fields, repeat back the parsed value before
proceeding ("J'ai compris : montant = 1 500 €, date = 12 mars 2026.
C'est correct ?").

### Step 3 : Verify cited law

For each entry in `applicable_law`, run a `WebFetch legifrance.gouv.fr`
to confirm the article is still in force and that any numerical thresholds
in the template (délais, plafonds) match the current version. If a
modification is detected → adjust the template's delay/threshold values
and signal it to the user before generating.

### Step 4 : Generate the document

Replace `{{field_name}}` placeholders with collected values. Resolve
`{{#if …}}` conditionals based on whether the optional field was filled.

A template body may use placeholders that are not declared in the
frontmatter `required_fields` / `optional_fields`. Three categories of
such placeholders exist; handle them as follows:

- **Auto-derived from context** (`{{date_du_jour}}`, `{{ville_expediteur}}`,
  `{{ville_locataire}}`, `{{ville_salarie}}`, `{{ville_contrevenant}}`,
  `{{ville_requerant}}`, `{{ville_plaignant}}`, `{{ville_signature}}`,
  `{{date_signature}}`) : derive from the current date or from the city
  part of an address already collected. No new question needed.
- **Derived from another collected field** (`{{duree_preavis}}`,
  `{{date_debut_preavis}}`, `{{date_fin_preavis}}`, `{{delai_legal}}`,
  `{{tribunal_competent_ville}}`, `{{tribunal_adresse}}`,
  `{{adresse_omp_indique_sur_avis}}`, `{{titre_autorite}}`,
  `{{situation_vehicule}}`) : compute from the user's earlier answers,
  the convention collective indicated, or from the document the user
  is contesting/responding to. Confirm the computed value with the user
  before insertion.
- **Free-text follow-ups** (`{{employeur_signataire_nom}}`,
  `{{employeur_signataire_fonction}}`, `{{recherche_reclassement_detail}}`,
  `{{justification_locataire}}`) : ask one short follow-up question for
  each, in the natural flow after the related questionnaire item.

Output the final document inside a Markdown code block prefixed and
suffixed by a line of dashes for visual separation:

```
----- DOCUMENT GENERATED -----
<final document text>
----- END DOCUMENT -----
```

Below the document, output the verification checklist (the
`## Vérifications juridiques avant envoi` content from the template, with
context-specific notes added).

### Step 5 : Reinforced disclaimer

For `disclaimer_level: high` templates (all v3 templates), append this
block after the verification checklist:

> Ce document est un modèle généré automatiquement à titre indicatif. Faites-le relire par un avocat avant tout envoi, particulièrement pour les délais et les motifs invoqués. La validité juridique du contenu dépend des circonstances précises de votre situation. L'envoi recommandé avec accusé de réception est conseillé pour conserver une preuve juridique.

### Step 6 : Final standard disclaimer

End with the mandatory plugin-wide disclaimer (FR or EN per detected
language), per `skills/legal-france/SKILL.md`.

---

## 5. Failure modes

- **User refuses to provide a required field** → cannot generate; explain
  why and abort gracefully.
- **Legifrance verification fails (no network, ambiguous result)** → warn
  the user clearly:
  > Je n'ai pas pu vérifier en ligne la version en vigueur de <article>. Le modèle utilise les références embarquées. Vérifiez sur legifrance.gouv.fr avant envoi.
- **Cited article amended since embedded reference** → use the current
  version values and flag:
  > Note : <article> a été modifié depuis la dernière mise à jour des références. Le modèle utilise la version en vigueur consultée sur Legifrance.
