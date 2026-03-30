# Changelog

All significant updates to SCRATCH are recorded here in plain language. Entries are listed in reverse chronological order, with the most recent at the top.

---

## 31 March 2026 — Version 0.6

**Author:** RPAH Allergy Nurses
**Change:** DREAM integration page and adrenaline wording correction.

- **DREAM Page:** Added a new Testing tab linking to the DREAM app (Drug Reaction Evaluation and Anaesthetic Management), the nurse-led platform for real-time documentation of allergy testing encounters. The page explains the REDCap → DREAM → eMR workflow and the complementary relationship between SCRATCH and DREAM.
- **Adrenaline Wording:** Corrected adrenaline safety language across 5 pages (home, anaphylaxis reference, mixing guide, amoxicillin, augmentin) to reflect that adrenaline is available on standby — not pre-drawn into a syringe before procedures.

---

## 29 March 2026 — Version 0.5

**Author:** RPAH Allergy Nurses
**Change:** Site hardening — search engine blocking, announcement bar, and UI fixes.

- **Search Engine Blocking:** Added `robots.txt` (`Disallow: /`) and Cloudflare Pages `_headers` (`X-Robots-Tag: noindex, nofollow`) to prevent public indexing. All pages also carry a `<meta name="robots" content="noindex, nofollow">` tag for complete coverage.
- **Announcement Bar:** Persistent banner on all pages linking to the Protocols for Review page, noting that some protocols are under clinical review. Dismissible per user session.
- **Link Preview Descriptions:** All drug pages now include a default meta description for internal sharing via Teams or email.
- **Double Border Fix:** Corrected a visual bug where two SLHD Red border lines appeared at the top of the page on desktop due to both the header and tabs bar carrying a `border-bottom` style.

---

## 29 March 2026 — Version 0.4

**Author:** RPAH Allergy Nurses
**Change:** Major content expansion — 28 new drug protocols, data corrections, UI refinements, and complete navigation.

- **28 New Drug Pages:** Added protocol pages for azithromycin, betamethasone, celestone-chronodose, droperidol, gentamicin, glycopyrronium, granisetron, medroxyprogesterone, metoclopramide, neostigmine, ondansetron, protamine, tramadol, triamcinolone, actrapid, humulin-nph, humulin-r, novorapid, optisulin, protaphane, metacresol, urografin, cyproterone-ethinylestradiol, drospirenone-ethinylestradiol, ethinylestradiol-levonorgestrel, ethinylestradiol-norethisterone, levonorgestrel, and xylocaine (94 total).
- **10 Drug Pages Corrected:** Updated conflicting drug pages to match the Spreadsheet 1 reference spreadsheet. Fixed internal inconsistencies in Ketamine, Paracetamol, and Tazocin pages.
- **Protocols for Review:** Created a new reference page (`reference/protocols-for-review.md`) listing 6 protocols with calculation concerns flagged for clinical team review.
- **Home Page Redesign:** Expanded home table from 12 rows (44 drugs) to 17 rows (all 94 drugs), organized by clinical category with Material icons for quick visual scanning.
- **Navigation Overhaul:** Restructured sidebar navigation to match home table categories (17 categories), ensuring all 94 drugs are discoverable in the sidebar menu.
- **Branding:** Added test tube logo to header (Material Design icon) and favicon (custom SVG in SLHD Navy).
- **Tags Index:** Configured tags plugin to populate the Tags reference page for protocol browsing by tag.

---

## 28 March 2026 — Version 0.3

**Author:** RPAH Allergy Nurses
**Change:** Branding and metadata finalization.

- **Authorship Update:** Standardized all site-wide attribution to "RPAH Allergy Nurses".
- **Top Bar Style:** Enabled `primary` topbar style for increased clinical visibility.
- **Dark Mode Fix:** Recalibrated colors for the Slate theme to resolve link readability and background contrast.
- **Navigation Rail:** Added a 3px SLHD Red bottom border to the tab navigation for institutional alignment.
- **Manual Cleanup:** Removed automated Git-based authorship metadata to ensure clinical anonymity.

---

## 28 March 2026 — Version 0.2

**Author:** RPAH Allergy Nurses
**Change:** Clinical workflow & QA upgrades.

- **Macros:** Configured standard macros for injecting unified text/warnings.
- **Tooltips:** Configured glossary and acronym hover tooltips natively.
- **Offline Reliability:** Built-in offline caching service-worker generated for ward use.
- **Print Version:** Whole library export endpoint `/print_page` implemented.
- **Governance:** Implemented site-wide clinical disclaimers and localized feedback loops.

---

## 28 March 2026 — Version 0.1

**Author:** RPAH Allergy Nurses
**Change:** First published version of SCRATCH.

This version includes individual drug pages for all agents currently tested by the department, covering the following groups:

- **Penicillins** — Amoxicillin, Ampicillin, Augmentin, Benzylpenicillin, Flucloxacillin, Penicillin Major (PPL), Penicillin Minor (MD), Phenoxymethylpenicillin
- **Cephalosporins** — Cefazolin, Cefepime, Cefotaxime, Ceftazidime, Ceftriaxone, Cefuroxime, Cephalexin
- **Muscle relaxants** — Cisatracurium, Pancuronium, Rocuronium, Suxamethonium, Vecuronium
- **Opioids** — Alfentanil, Fentanyl, Morphine, Oxycodone, Remifentanil
- **Anaesthetic agents** — Ketamine, Midazolam, Propofol, Thiopental
- **Local anaesthetics** — Bupivacaine, Lignocaine, Mepivacaine, Ropivacaine
- **Proton pump inhibitors** — Esomeprazole, Lansoprazole, Omeprazole, Pantoprazole, Rabeprazole
- **NSAIDs and analgesics** — Aspirin, Paracetamol, Parecoxib
- **Contrast media** — Omnipaque, Ultravist, Visipaque
- **Anticoagulants** — Dalteparin, Enoxaparin, Heparin
- **Other antibiotics** — Bactrim, Ciprofloxacin, Doxycycline, Levofloxacin, Metronidazole
- **Miscellaneous** — Chlorhexidine, Dexamethasone, Fluconazole, Latex, Patent Blue, Povidone Iodine, Rosuvastatin, Sugammadex, Tranexamic Acid

Each drug page includes a stock concentration overview, skin prick test (SPT) protocol, intradermal test (IDT) dilution series, and where applicable, an oral or intravenous challenge protocol. Clinical data was sourced from the department's internal reference spreadsheets (*Spreadsheet 2* and *Spreadsheet 1*).

Reference pages are also included for anaphylaxis emergency management and a general mixing and dilution guide.