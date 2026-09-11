# Rédacteur Engine : Workflow Documentation

This document is read by any skill that needs to produce a legal document
(letter, mise en demeure, plainte, recours, statuts, etc.). It defines the
qualification and drafting workflow, the template contract, and the reinforced disclaimer.

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

Each template has YAML frontmatter with:

- `type`, `domain`, `short_description`: identity and routing.
- `qualification_fields`: facts to establish when relevant to selecting the
  legal regime, checking a deadline or substantiating the document.
- `required_fields`: information needed to personalize the selected document.
- `optional_fields`: information used only when applicable.
- `derived_fields`: conclusions, dates, amounts or passages derived from
  collected facts and verified law; never guessed or treated as user evidence.
- `applicable_law`: texts to verify in the version applicable to the situation.
- `disclaimer_level`: `high` preserves both mandatory disclaimers below.

The body contains `## Qualification préalable`, `## Questionnaire`,
`## Template` and `## Vérifications juridiques avant envoi`.
Qualification defines the supported situation, useful pieces and cases
requiring a different procedure before using the document body.

Placeholders use `{{field_name}}`. A condition tests the established value,
not merely the presence of a nonempty string: « non », « inconnu » and
« non vérifié » must not activate a positive branch. Every placeholder and
condition must refer to a declared field. Only supported branches are rendered.

---

## 4. Workflow

### Step 1 : Qualify the request and resolve the template

Apply `skills/legal-france/references/qualification.md`. Identify the user's
objective and any urgent deadline; read the selected template's qualification
before its body. A general information request needs no drafting questionnaire.
If the template does not cover the situation, explain the missing procedure
and continue the relevant analysis; do not force the situation into the body.

### Step 2 : Collect decisive facts and useful pieces

Start with the legal facts and dates in the questionnaire, using answers
already provided. Group related missing questions and ask follow-ups only
when an answer changes the regime or remains ambiguous. Request the useful
pieces or excerpts, allowing irrelevant personal information to be masked.
Collect identity and address details last; accept explicit placeholders for
an anonymized model. Do not block an explanation for missing identity.

Distinguish reported, corroborated, disputed and unknown facts. A missing
piece may leave a claim unproven without preventing a factual draft. Ask
for confirmation of a date or amount only if it is ambiguous, contradictory
or materially different from the user's statement.

If a missing fact determines the applicable procedure, admissibility or
whether a claimed sum is due, ask the targeted questions **before producing
the personalized act**. A request to “draft the letter” does not establish
those facts. An explicitly requested incomplete/anonymized draft may still
be supplied, using factual placeholders. Permission to use fictional names
concerns identities; it does not authorize fictional legal facts.

### Step 3 : Verify applicability and establish the result

For the selected legal regime, consult official sources, their effective
dates and transitional provisions. Check relevant agreements and exceptions.
The latest text is not automatically applicable to older facts.

Before generation, give a short assessment: supported regime, material
unknowns, evidence available, sums that can be claimed and deadlines that
can actually be determined. For each calculation state its inputs, legal
basis/version, triggering event, computation and result. If an event has
not occurred (for example first presentation of a future letter), keep the
result conditional or undetermined. Recheck arithmetic independently.

A web/API failure does not validate an embedded rule. Identify the missing
verification and its consequence. Do not label a disputed or unverified
procedure, deadline, consent, authorization or amount as established.

### Step 4 : Generate the appropriate document

Use only the branches supported by the assessment. Compute `derived_fields`
from known inputs and verified rules; ask a targeted question when a needed
input is absent. A named party's version can be expressed as its claim,
without asserting that a court has established it.

For a personalized document, resolve every material legal prerequisite.
If the user wants a draft despite an unknown, visibly mark it **BROUILLON
INCOMPLET : points à compléter**, retain explicit placeholders and list the
blocking points outside the act. Never invent a past procedural step or a
legal conclusion to finish a sentence. An unsupported scenario requires
adaptation of the workflow, not just an added disclaimer.

Keep the loaded template's structure and supported clauses; do not substitute
a more elaborate stock template from memory. Before output, review every
factual assertion **inside the act** against the supplied facts and examined
pieces. For an unsupported assertion, replace the entire assertion with a
field to complete, or omit it. A warning after an affirmative sentence, or
only in the checklist, does not make that sentence conditional. In particular,
an unknown fact is not a negative fact, an intended step is not a completed
step, and a requested document is not an attachment already available.
Keep documents still to obtain in the checklist outside the act.

Output the document in a Markdown code block. Then show the verification
checklist, distinguishing completed checks from remaining checks, and useful
attachments actually available from those still to obtain. Do not list an
unseen or unavailable document as already enclosed.

### Step 5 : Reinforced disclaimer

For `disclaimer_level: high` templates (all v3 templates), append this
block after the verification checklist:

> Ce document est un modèle généré automatiquement à titre indicatif. Faites-le relire par un avocat avant tout envoi, particulièrement pour les délais et les motifs invoqués. La validité juridique du contenu dépend des circonstances précises de votre situation. L'envoi recommandé avec accusé de réception est conseillé pour conserver une preuve juridique.

### Step 6 : Final standard disclaimer

End with the mandatory plugin-wide disclaimer (FR or EN per detected
language), per `skills/legal-france/SKILL.md`.

---

## 5. Failure modes

- **Decisive fact missing or conflicting**: ask the targeted question; a
  conditional analysis or visibly incomplete draft may continue, without a
  definite deadline or unsupported factual assertion.
- **Identity withheld**: offer anonymized placeholders for a model.
- **Unsupported regime or unmet prerequisite**: explain the needed procedure
  before finalizing the act; continue useful research and fact collection.
- **Verification unavailable**: state the exact unverified rule/version and
  its impact; use the embedded material only as provisional background.
- **Official text differs from the fund**: select the applicable version
  using the facts and transitional rules, and explain the change.
