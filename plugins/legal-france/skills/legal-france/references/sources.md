# Legal Database Search Guide : France & EU

This reference covers the primary legal databases for French and European law: what each contains, how to search it, and how to cite decisions found there.

---

## 1. Légifrance

**URL:** https://www.legifrance.gouv.fr
**Operator:** Direction de l'information légale et administrative (DILA)

### What it contains
- All French legislation in force: codes, lois, ordonnances, décrets, arrêtés
- Consolidated versions of codes (with amendment history)
- Official Journal (Journal officiel de la République française : JORF)
- Case law from: Cour de cassation, Conseil d'État, cours d'appel, tribunaux administratifs, Conseil constitutionnel
- Collective labor agreements (conventions collectives)
- European texts transposed into French law

### How to search
- **Free text search:** Use the search bar at the top. Filter by category (Codes, Jurisprudence, Textes, etc.)
- **Browse a code:** Go to "Codes en vigueur" → select the code → navigate by book/title/chapter
- **Search by article number:** Enter the article number directly (e.g., "article 1240 code civil")
- **Search case law:** Go to "Jurisprudence" → filter by court, date range, or keywords
- **Search by decision number:** For Cour de cassation, use the pourvoi number; for Conseil d'État, use the requête number

### URL patterns
- Code article: `https://www.legifrance.gouv.fr/codes/article_lc/[LEGIARTI_ID]`
- Code section: `https://www.legifrance.gouv.fr/codes/section_lc/[LEGISCTA_ID]`
- Full code: `https://www.legifrance.gouv.fr/codes/id/[LEGITEXT_ID]`
- JORF text: `https://www.legifrance.gouv.fr/jorf/id/[JORFTEXT_ID]`
- Cour de cassation decision: `https://www.legifrance.gouv.fr/juri/id/[JURITEXT_ID]`

### Decision citation formats

**Cour de cassation:**
```
Cass. [chambre], [date], n° [pourvoi]
```
- Chambre abbreviations: `civ. 1re`, `civ. 2e`, `civ. 3e`, `com.`, `soc.`, `crim.`, `ass. plén.`, `ch. mixte`, `ch. réunies`
- Date format: `DD [month abbrev.] YYYY` (e.g., `12 janv. 2023`)
- Pourvoi number format: `YY-NN.NNN` (e.g., `21-12.345`)
- Full example: `Cass. civ. 1re, 12 janv. 2023, n° 21-12.345`
- Published in Bulletin: add `Bull. civ. I, n° [N]` for pre-2017 decisions

**Conseil d'État:**
```
CE, [formation], [date], n° [requête], [nom de l'affaire]
```
- Formation abbreviations: `Ass.` (Assemblée), `Sect.` (Section), `ord.` (ordonnance de référé)
- Example: `CE Ass., 20 oct. 1989, n° 108243, Nicolo`
- Published decisions add: `Rec. CE p. [page]` or `Lebon p. [page]`

**Conseil constitutionnel:**
```
Cons. const., [date], n° [year]-[number] [type]
```
- Decision types: `DC` (contrôle a priori), `QPC` (question prioritaire de constitutionnalité), `LP` (loi du pays), `L` (déclassement)
- Example (DC): `Cons. const., 16 juil. 1971, n° 71-44 DC`
- Example (QPC): `Cons. const., 28 mai 2010, n° 2010-1 QPC`

---

## 2. EUR-Lex

**URL:** https://eur-lex.europa.eu
**Operator:** Publications Office of the European Union

### What it contains
- All EU legislation: règlements (regulations), directives, décisions (decisions)
- Official Journal of the EU (OJ/JOUE): L series (legislation), C series (information/notices)
- CJEU (Court of Justice of the EU) and General Court case law
- Consolidated versions of EU acts
- Preparatory documents (COM documents, legislative proposals)
- International agreements to which the EU is a party

### How to search
- **Free text search:** Use the search bar; filter by resource type, year, author institution
- **Search by CELEX number:** Directly enter the CELEX number in the search bar
- **Browse by subject matter:** Use the EuroVoc thesaurus classification
- **Search case law:** Go to "Case law" → filter by court, year, subject
- **Search by case number:** Enter the case number (e.g., `C-311/18`)

### CELEX number format
```
[Sector][Year][Document type][Number]
```
- Sector: `1` = Treaties, `2` = International agreements, `3` = Secondary legislation, `6` = EU case law (CJ, Tribunal, ex-Tribunal de la fonction publique), `7` = National transposition measures, `8` = National case law (les anciens « 7 = General Court, 8 = Civil Service Tribunal » étaient faux, vérifié le 2026-08-05)
- Document types for sector 3: `R` = regulation, `L` = directive, `D` = decision (l'ancienne ligne définissait « L » deux fois ; vérifié le 2026-08-05)
- Example (regulation): `32016R0679` = GDPR (Regulation 2016/679)
- Example (directive): `31995L0046` = Data Protection Directive 95/46/EC
- Example (CJEU judgment): `62017CJ0673` = Planet49, Case C-673/17 (sector 6, year of filing 2017, CJ = Court of Justice judgment ; l'ancien exemple « 62018CJ0673 » contredisait le numéro d'affaire)

### Citation format : CJEU decisions
```
CJUE [or CJCE pre-Lisbon], [date], [name], aff. [C-/T-number]
```
- CJCE = Cour de justice des Communautés européennes (pre-1 Dec 2009)
- CJUE = Cour de justice de l'Union européenne (post-1 Dec 2009)
- Example: `CJCE, 5 févr. 1963, Van Gend en Loos, aff. 26/62`
- Example: `CJUE, 16 juil. 2020, Schrems II, aff. C-311/18`

---

## 3. Conseil constitutionnel

**URL:** https://www.conseil-constitutionnel.fr

### What it contains
- All decisions (DC, QPC, L, LP, FNR, I, ELEC, REF, AN, SEN)
- Press releases and dossiers documentaires for major decisions
- QPC transmissions and filtering decisions from Cour de cassation and Conseil d'État
- Commentaries in the Cahiers du Conseil constitutionnel (official doctrinal notes)
- Constitution of 4 October 1958 and the bloc de constitutionnalité texts

### How to search
- **By decision number:** Use the search field with the format `[year]-[number] DC` or `[year]-[number] QPC`
- **By theme:** Use the classification by subject or keyword
- **QPC tracker:** Dedicated section showing pending and decided QPCs
- **Chronological browsing:** Filter by year and decision type

### Key URL pattern
`https://www.conseil-constitutionnel.fr/decision/[year]/[number][type].htm`
Example: `https://www.conseil-constitutionnel.fr/decision/1971/7144DC.htm`

---

## 4. CNIL

**URL:** https://www.cnil.fr
**Operator:** Commission nationale de l'informatique et des libertés

### What it contains
- Délibérations (deliberations): formal decisions, authorizations, recommendations, sanctions
- Referential documents (guides, fiches pratiques) on GDPR compliance
- Sanctions and formal notices (mises en demeure)
- Annual reports
- Guidelines on specific topics (cookies, health data, AI, etc.)
- Standard simplified norms (now mostly replaced by GDPR guidelines)

### How to search
- **Sanctions:** Go to "Espace professionnel" → "Les sanctions de la CNIL" for the full list of sanctioned entities
- **Deliberations:** Use the search bar with keywords + filter by document type "Délibération"
- **By registration number:** Délibérations are numbered as `n° [year]-[NNN]` (e.g., `n° 2019-001`)
- **Guides:** Browse by theme (e.g., "cookies et traceurs", "sous-traitance", "droits des personnes")

### Citation format
```
CNIL, [date], délibération n° [year]-[NNN], [name/subject]
```
Example: `CNIL, 21 janv. 2019, délibération n° 2019-001, Google LLC`

---

## 5. Service-public.fr

**URL:** https://www.service-public.gouv.fr (nouveau domaine officiel, constaté le 2026-08-05)
**Operator:** DILA (Direction de l'information légale et administrative)

### What it contains
- Plain-language explanations of administrative procedures for individuals and businesses
- Step-by-step guides for legal procedures (divorce, succession, contract disputes, etc.)
- Official forms (cerfa) and downloadable documents
- Information on rights and obligations in everyday situations
- Links to competent administrative authorities

### How to search
- Use the search bar with everyday language (e.g., "licenciement", "contester une amende")
- Browse by theme: "Particuliers", "Professionnels", "Associations"
- Direct links to competent tribunals and administrative bodies
- Note: Not a primary legal source, use for orientation and procedure steps, not for legal argument

---

## 6. Conseil d'État

**URL:** https://www.conseil-etat.fr

### What it contains
- Full text of Conseil d'État decisions (Assemblée, Section, sous-sections réunies, ordonnances de référé)
- Avis contentieux and avis consultatifs
- Annual reports and études (policy studies)
- Legal guides on administrative law
- Database of administrative case law (searchable by keyword, date, requête number)

### How to search
- **By requête number:** Use the search tool with the 6-digit requête number (e.g., `108243`)
- **By keywords:** Full-text search across all decisions
- **Lebon tables:** The annual Recueil Lebon tables are available online for published decisions
- **Arianeweb:** The integrated jurisprudence search tool at `https://www.conseil-etat.fr/decisions-de-justice/jurisprudence/rechercher-une-decision-arianeweb`

### Citation format
See Légifrance section above. The requête number is the key identifier.

---

## 7. Cour de cassation

**URL:** https://www.courdecassation.fr

### What it contains
- Full text of all Cour de cassation decisions (published and unpublished)
- Bulletin civil and Bulletin criminel (published/selected decisions with headnotes)
- Avis de la Cour de cassation
- Rapports annuels
- Communiqués de presse for major decisions
- Judicial committee reports (rapports de conseiller, avis d'avocat général)

### How to search
- **By pourvoi number:** Use the dedicated search; enter the pourvoi number in format `YY-NN.NNN`
- **By ECLI:** European Case Law Identifier format `ECLI:FR:CCASS:[YEAR]:[CHAMBER][NUMBER]`
- **Advanced search:** Filter by chambre, date range, publication status (P = publié au Bulletin, R = mentionné, D = diffusé)
- **Publication indicators:**
  - `P` (or `B`) = published in the Bulletin (leading decision)
  - `R` = mentioned in the Bulletin tables
  - `D` = diffusé (available online but not in Bulletin)
  - `I` = inédit (unpublished, internal use)

### Citation format
See Légifrance section above. For published decisions, the Bulletin reference adds authority:
```
Cass. civ. 1re, 12 janv. 2023, n° 21-12.345, Bull. civ. I, n° 5
```

---

## Cross-database search tips

| Goal | Primary source | Secondary source |
|------|---------------|-----------------|
| Find current text of a French code article | Légifrance (consolidated codes) | Service-public.fr (plain language) |
| Find a Cour de cassation decision by pourvoi | courdecassation.fr | Légifrance |
| Find a Conseil d'État decision | conseil-etat.fr (Arianeweb) | Légifrance |
| Find a QPC decision | conseil-constitutionnel.fr | Légifrance |
| Find an EU regulation or directive | EUR-Lex | Légifrance (transposition) |
| Find a CJEU judgment | EUR-Lex | EUR-Lex case law section |
| Find a CNIL sanction | cnil.fr | Légifrance (if published in JORF) |
| Check administrative procedure steps | service-public.fr | Code de justice administrative on Légifrance |

---

## Domain-specific search tips

### Droit civil

**Best Légifrance filters:** Category "Codes en vigueur" → Code civil, Code de la consommation, Code des assurances. For case law, filter by "Cour de cassation" → chambres civiles (civ. 1re for obligations/contrats/personnes, civ. 2e for responsabilité/procédure civile, civ. 3e for immobilier/baux).

**Specialized databases:**
- **Cour de cassation : Bulletin civil:** For leading published decisions, filter publication status `P` (publié). Pre-2017 decisions are organized in Bull. civ. I through IV by chamber.
- **Service-public.fr:** Useful for plain-language summaries of family law, succession, and consumer protection procedures.

**Example searches:**
- Légifrance: `"article 1240" responsabilité délictuelle` in Jurisprudence → Cour de cassation → civ. 2e
- Légifrance code browser: Code civil → Livre III → Titre III → Sous-titre II (La responsabilité extracontractuelle, arts. 1240 à 1254 ; pas de réforme d'ensemble en 2025, seulement les lois 2025-568 et 2025-391)
- Cour de cassation advanced search: chamber = `civ. 1re`, keyword = `vice du consentement`, publication = `P`

### Droit pénal

**Best Légifrance filters:** Category "Codes en vigueur" → Code pénal, Code de procédure pénale. For case law, filter by "Cour de cassation" → chambre criminelle (`crim.`). Date range filters are critical for tracking changes in sentencing policy.

**Specialized databases:**
- **Cour de cassation : Bulletin criminel:** Filter by `crim.` chamber and publication status `P` for landmark criminal decisions.
- **Conseil constitutionnel : QPC:** Many QPC decisions concern criminal law (principes de légalité, proportionnalité des peines). Search by keyword on conseil-constitutionnel.fr.
- **CEDH/ECHR (HUDOC):** For challenges based on Article 6 (fair trial) or Article 7 (no punishment without law) of the Convention.

**Example searches:**
- Légifrance: `"article 121-3" faute non intentionnelle` in Jurisprudence → Cour de cassation → crim.
- Légifrance code browser: Code pénal → Livre II → Titre II (Atteintes à la personne humaine)
- Conseil constitutionnel: keyword `proportionnalité des peines` filtered by decision type `QPC`

### Droit du travail

**Best Légifrance filters:** Category "Codes en vigueur" → Code du travail. For case law, filter by "Cour de cassation" → chambre sociale (`soc.`). Also search in "Conventions collectives" for sector-specific rules.

**Specialized databases:**
- **Convention collective search on Légifrance:** Dedicated search at "Accords collectifs et conventions collectives", filter by IDCC number (identifiant de convention collective) or by sector.
- **DARES (Direction de l'animation de la recherche, des études et des statistiques):** For labor market statistics cited in policy arguments.
- **Rapports du Conseil d'État et Cour de cassation:** Annual reports often include thematic studies on labor law topics (e.g., contrat de travail, temps de travail).

**Example searches:**
- Légifrance: `licenciement économique motif réel et sérieux` in Jurisprudence → Cour de cassation → soc.
- Conventions collectives: IDCC `0016` (Transports routiers) or keyword search `télétravail`
- Légifrance: `"article L.1232-1" entretien préalable` in Codes → Code du travail

### Droit des affaires

**Best Légifrance filters:** Category "Codes en vigueur" → Code de commerce, Code monétaire et financier. For case law, filter by "Cour de cassation" → chambre commerciale (`com.`). For IP disputes, also check civ. 1re and tribunal judiciaire de Paris.

**Specialized databases:**
- **INPI (Institut national de la propriété industrielle):** https://www.inpi.fr, Search trademark, patent, and design registrations. The INPI database (`bases-brevets.inpi.fr`, `bases-marques.inpi.fr`) provides registration details and oppositions.
- **AMF (Autorité des marchés financiers):** https://www.amf-france.org, Decisions, sanctions, and regulations on financial markets.
- **ADLC (Autorité de la concurrence):** https://www.autoritedelaconcurrence.fr, Decisions on anticompetitive practices, mergers.
- **Registre du commerce (Infogreffe):** https://www.infogreffe.fr, Company filings, financial statements, insolvency proceedings.

**Example searches:**
- Légifrance: `concurrence déloyale parasitisme` in Jurisprudence → Cour de cassation → com.
- INPI: trademark name search in `bases-marques.inpi.fr` to check prior registrations
- AMF: sanctions search filtered by year and type (manquement d'initié, manipulation de cours)

### Droit administratif

**Best Légifrance filters:** Category "Jurisprudence administrative" → filter by court (Conseil d'État, cours administratives d'appel, tribunaux administratifs). Use "Textes" section to search décrets, arrêtés, and circulaires.

**Specialized databases:**
- **Arianeweb (Conseil d'État):** https://www.conseil-etat.fr/decisions-de-justice/jurisprudence/rechercher-une-decision-arianeweb, The primary advanced search tool for all administrative case law. Filters by formation de jugement, rapporteur public, and Lebon publication status.
- **Circulaires et instructions (Legifrance) :** l'ancien site circulaires.gouv.fr redirige vers la recherche Circulaires de legifrance.gouv.fr (constaté le 2026-08-05). Repository of government circulars and instructions, useful for understanding how ministries interpret legislation.
- **Recueil Lebon:** The official compendium of selected administrative law decisions. On Arianeweb, filter by `Recueil Lebon` or `Tables du Recueil Lebon` for published decisions.

**Example searches:**
- Arianeweb: formation = `Assemblée`, keyword = `responsabilité sans faute`, period = 2020-2026
- Légifrance: `excès de pouvoir annulation` in Jurisprudence administrative → Conseil d'État
- Legifrance (section Circulaires) : keyword search for a specific ministerial instruction (e.g., `instruction fiscale BOI-CF`)

### Droit du numérique

**Best Légifrance filters:** Relevant codes include Code des postes et des communications électroniques, and provisions in Code pénal (cyber offences, art. 323-1 et seq.) and Code civil (droit à l'image, art. 9). For EU texts, use EUR-Lex to find the GDPR (Règlement 2016/679), the Digital Services Act, the AI Act.

**Specialized databases:**
- **CNIL : Délibérations et sanctions:** https://www.cnil.fr/fr/les-sanctions-prononcees-par-la-cnil, Full list of sanctions with deliberation numbers. Filter by theme (cookies, données de santé, vidéosurveillance, IA).
- **CNIL : Lignes directrices:** Thematic guides on GDPR compliance (e.g., cookies, sous-traitance, AIPD/DPIA).
- **ANSSI (Agence nationale de la sécurité des systèmes d'information):** https://cyber.gouv.fr (l'ancien ssi.gouv.fr redirige, constaté le 2026-08-05), Cybersecurity standards and regulatory frameworks.
- **EDPB (European Data Protection Board):** https://edpb.europa.eu, Guidelines, opinions, and consistency decisions on GDPR interpretation across the EU.

**Example searches:**
- CNIL: sanction search filtered by theme `cookies et traceurs` or `transferts de données`
- Légifrance: `"article 323-1" système de traitement automatisé` in Jurisprudence → Cour de cassation → crim.
- EUR-Lex: CELEX `32016R0679` for GDPR full text; keyword `intelligence artificielle` in secondary legislation

### Droit européen

**Best Légifrance filters:** Use the "Droit européen" section on Légifrance for EU texts transposed into French law. For ECHR-related case law, search in Jurisprudence → filter by references to the Convention européenne des droits de l'homme.

**Specialized databases:**
- **CURIA (CJUE):** https://curia.europa.eu, Full search engine for Court of Justice and General Court decisions. Filter by type of procedure (renvoi préjudiciel, recours en annulation, recours en manquement), chamber, and subject matter.
- **HUDOC (CEDH/ECHR):** https://hudoc.echr.coe.int, Complete database of European Court of Human Rights judgments and decisions. Filter by respondent state (`France`), article of the Convention, and importance level.
- **EUR-Lex:** See dedicated section below. For consolidated versions of directives and regulations, use the "Consolidated text" tab.
- **EU Official Journal (JOUE):** Available on EUR-Lex. L series = legislation; C series = information and notices.

**Example searches:**
- CURIA: procedure type = `Renvoi préjudiciel`, keyword = `protection des données`, year = 2023-2026
- HUDOC: respondent = `France`, article = `Article 8` (vie privée), importance = `Key cases`
- EUR-Lex: browse JOUE L series for a specific regulation publication date

### Droit de la procédure

**Best Légifrance filters:** Category "Codes en vigueur" → Code de procédure civile, Code de procédure pénale, Code de justice administrative. For case law, filter by "Cour de cassation" → civ. 2e (procédure civile), crim. (procédure pénale), or by "Conseil d'État" for administrative procedure.

**Specialized databases:**
- **Cour de cassation : civ. 2e:** The second civil chamber handles most procedural appeals (délais, voies de recours, exécution des jugements).
- **Service-public.fr : Procédures:** Step-by-step guides for saisine du tribunal, référé, injonction de payer, aide juridictionnelle.
- **Annuaire des juridictions:** https://www.justice.fr, Find the competent court by location and subject matter.

**Example searches:**
- Légifrance: `"article 700" frais irrépétibles` in Jurisprudence → Cour de cassation → civ. 2e
- Légifrance code browser: Code de procédure civile → Livre I → Titre XVI (Mesures d'exécution forcée)
- Service-public.fr: `saisir le tribunal judiciaire` for step-by-step procedural guidance

---

## EU Sources : Advanced Guide

### EUR-Lex : Advanced search

**URL:** https://eur-lex.europa.eu/advanced-search-form.html

EUR-Lex advanced search allows precise filtering across the entire EU legal corpus:

- **By document type:** Regulation, directive, decision, recommendation, opinion, international agreement, CJEU case law.
- **By CELEX number:** Enter the sector-year-type-number code directly (e.g., `32016R0679` for GDPR).
- **By date:** Filter by date of document, date of effect, or transposition deadline.
- **By EuroVoc descriptor:** Use the controlled thesaurus to filter by subject (e.g., `protection des données`, `marché intérieur`, `concurrence`).
- **By author institution:** European Commission, Council, Parliament, or joint authorship.
- **Consolidated texts:** Tick the "Consolidated version" box to see legislation as amended, rather than the original text.
- **National transposition measures:** For directives, the "National transposition" tab lists implementing measures by Member State, filter by `France` to see how a directive was transposed.
- **Legal basis search:** Filter by Treaty article to find all secondary legislation adopted under a given legal basis (e.g., Article 114 TFUE for internal market harmonization).

### CURIA : Court of Justice of the EU (CJUE)

**URL:** https://curia.europa.eu/juris/recherche.jsf?language=fr

CURIA is the official search engine for the case law of the Court of Justice (CJUE), the General Court (Tribunal), and historical decisions of the Civil Service Tribunal.

- **Search by case number:** Enter the case number in format `C-NNN/YY` (Court of Justice) or `T-NNN/YY` (General Court).
- **Search by ECLI:** Use the European Case Law Identifier format `ECLI:EU:C:[year]:[number]`.
- **Filter by procedure type:** Renvoi préjudiciel (preliminary reference), recours en annulation (action for annulment), recours en manquement (infringement proceedings), recours en carence (failure to act), pourvoi (appeal from General Court).
- **Filter by subject matter:** Use the subject-matter classification (e.g., "Rapprochement des législations", "Politique sociale", "Environnement").
- **Advocate General opinions:** Search separately for conclusions de l'avocat général, these are often cited as persuasive authority and may signal future jurisprudential shifts.
- **Pending cases:** The "Affaires introduites" section tracks newly filed cases and pending references, useful for monitoring emerging legal questions.

**Citation format:**
```
CJUE, [date], [name], aff. C-[number]/[year], EU:C:[year]:[number]
```
Example: `CJUE, 16 juil. 2020, Schrems II, aff. C-311/18, EU:C:2020:559`

### HUDOC : European Court of Human Rights (CEDH/ECHR)

**URL:** https://hudoc.echr.coe.int

HUDOC provides access to the full case law of the European Court of Human Rights, the European Commission of Human Rights (historical), and the Committee of Ministers' resolutions.

- **Search by application number:** Enter the application number in format `NNNNN/YY` (e.g., `36769/08`).
- **Filter by respondent State:** Select `France` to find all cases against France.
- **Filter by Convention article:** Select one or more articles (e.g., Article 6, droit à un procès équitable, Article 8, droit au respect de la vie privée, Article 10, liberté d'expression).
- **Filter by importance level:** `Key cases` (highest doctrinal significance), `Case Reports` (selected for official reports), and others.
- **Filter by violation found:** Narrow to cases where the Court found a violation, a non-violation, or struck the case out.
- **Legal summaries:** HUDOC provides case summaries (fiches thématiques) organized by Convention article, helpful for identifying leading ECHR case law on a topic.

**Citation format:**
```
CEDH, [date], [name] c. [State], req. n° [number]
```
Example: `CEDH, 26 juin 2014, Mennesson c. France, req. n° 65192/11`

### EU Official Journal (JOUE)

**URL:** https://eur-lex.europa.eu/oj/direct-access.html

The Official Journal of the European Union (JOUE) is the official publication instrument for EU law and information:

- **L series (Législation):** Binding legislative acts, regulations, directives, decisions. An act enters into force only upon publication in the L series (or on the date specified therein).
- **C series (Communications et informations):** Non-binding acts, notices, information from EU institutions, including opinions, recommendations, and European Parliament resolutions.
- **Browse by date:** Direct access by year, month, and day of publication.
- **Search by OJ reference:** Enter the series, number, and page (e.g., `JOUE L 119, 4.5.2016, p. 1` for the GDPR).
- **E-only publication:** Since 1 July 2013, the electronic edition of the JOUE is the sole authentic version (Regulation (EU) No 216/2013).
