# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary users are the immunology and allergy nurses at Royal Prince Alfred Hospital (RPAH) — user-confirmed, and consistent with the repository's site attribution "RPAH Allergy Nurses". Their job in using SCRATCH: look up drug concentrations, dilution series, and testing protocols before and during drug allergy testing encounters (skin prick tests, intradermal tests, oral challenges).

Doctors are users "sometimes" (user-confirmed) — an occasional audience, not the primary one. Whether doctors need any distinct content, views, or workflows is undecided.

## Product Purpose

SCRATCH is the clinical protocol reference handbook for the Department of Clinical Immunology and Allergy at RPAH. It is the department's lookup tool for allergy testing: while the companion tool DREAM is where the encounter is documented, SCRATCH is where the procedure is looked up.

User-confirmed success: all clinicians primarily rely on SCRATCH. How "primarily rely" would be measured is undecided.

## Positioning

SCRATCH is the department's own reference for its drug allergy testing protocols, built from the department's 2021 spreadsheets and kept reviewable through the flagged-protocols log. Its confirmed companion relationship: DREAM (Drug Reaction Evaluation and Anaesthetic Management) is the nurse-led real-time documentation platform for perioperative drug allergy testing encounters at RPAH — "while SCRATCH is your reference, DREAM is where you record the encounter." No external competitive positioning is confirmed.

## Operating Context

- Used at RPAH by the clinical immunology and allergy team before and during drug allergy testing: SPT, IDT, and oral challenges.
- Static web handbook (MkDocs / Material for MkDocs) deployed to Cloudflare Pages at https://scratch.pages.dev. DREAM is accessible from any modern browser on any ward device and is a progressive web app (PWA) at https://dream.yuson.au.
- Companion workflow (per docs/testing.md): REDCap (patient background) → DREAM (real-time encounter documentation) → eMR (clinical note). Neither SCRATCH nor DREAM stores patient-identifiable data independently; patient data is managed in REDCap under SLHD privacy and governance frameworks.
- Mandatory before any testing, per the handbook: written consent documented, baseline vital signs recorded, adrenaline 0.5 mg/mL (1:1000) on standby, positive (histamine 10 mg/mL) and negative (normal saline) controls for SPT; IDT volume 0.05 mL unless otherwise specified; oral challenge intervals are 20 minutes.
- Changelog entries are authored by "RPAH Allergy Nurses".

## Capabilities and Constraints

Confirmed capabilities (from the repository):

- 94 drug protocol pages across 17 clinical categories (penicillins, cephalosporins, other antibiotics, antiemetics, anticoagulants, corticosteroids, hormonal contraceptives, hypnotics/sedatives, insulins, local anaesthetics, neuromuscular blocking agents, neuromuscular reversal agents, NSAIDs/analgesics, opioids, proton pump inhibitors, contrast media, other).
- Reference pages: anaphylaxis management, mixing & dilution guide, protocols-for-review, tags index, changelog.
- Site features: full-text search, dark/light themes, print, per-session announcement bar linking to the protocols-for-review page, tag browsing, search-engine blocking (robots.txt, X-Robots-Tag, per-page noindex), link-preview meta descriptions.

Constraints:

- The 2021 reference spreadsheets — `reference/Med Chart 2021.xlsx` ("Spreadsheet 1") and `reference/Medication List 2021.xlsx` ("Spreadsheet 2") — are binding until clinical review decides otherwise (user-confirmed; "binded" interpreted as "binding").
- Six protocols currently carry discrepancies or calculation concerns flagged for clinical review: amoxicillin/ampicillin, augmentin, tazocin, pantoprazole, ketamine, ropivacaine. Pages follow the flagged source and record alternatives in Notes rather than resolving unilaterally.
- Open/undecided: how the binding status of the 2021 spreadsheets changes after clinical review completes; the "Suggest an edit" link currently points to a `FORM_URL_PLACEHOLDER`, so the real feedback form URL is undecided.

## Brand Commitments

- Product name: SCRATCH (the site description expands it as "Skin & Challenge Reference for Allergy Testing").
- Attribution: site author "RPAH Allergy Nurses"; copyright "Department of Clinical Immunology and Allergy - Royal Prince Alfred Hospital".
- Institutional visual signals already in the handbook: test-tube logo and favicon in SLHD Navy, SLHD Red accent border on navigation.
- No other binding brand, voice, or personality commitments were made.

## Evidence on Hand

- Binding reference spreadsheets: `reference/Med Chart 2021.xlsx`, `reference/Medication List 2021.xlsx`.
- `docs/reference/protocols-for-review.md` — the six flagged protocols, current page status, and required actions.
- `docs/reference/changelog.md` — release history (current version 0.6).
- 94 drug protocol pages in `docs/drugs/`, each carrying review metadata (`reviewed_by: RPAH Clinical Immunology & Allergy`, `last_reviewed`, `version`).
- `docs/testing.md` — the DREAM relationship and the REDCap → DREAM → eMR workflow.
- Absences that future work must not fabricate: no user research transcripts, testimonials, usage analytics, or usage statistics exist in the repository; "all clinicians primarily rely on SCRATCH" is a stated success goal, not a measured fact.

## Product Principles

1. Clinical truth over presentation: the 2021 spreadsheets are binding until clinical review decides otherwise; never invent a concentration, dilution, or interval.
2. Flag, don't silently correct: discrepancies are logged in protocols-for-review.md with current page status and required action until the clinical team decides.
3. Safety procedures are invariant: written consent, baseline vitals, adrenaline on standby, and controls appear for every applicable procedure.
4. SCRATCH references, DREAM records: preserve the division of roles and the absence of patient-identifiable data on either side.
5. Trust is the success measure: success is all clinicians primarily relying on SCRATCH; future work must serve that outcome rather than dilute the reference.

## Accessibility & Inclusion

No accessibility standard was confirmed for this product. Repository facts: dark/light theme support exists, and contrast was recalibrated for the slate (dark) theme. Whether a formal standard (e.g., WCAG) applies is open.
