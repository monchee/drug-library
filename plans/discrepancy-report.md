# Drug Page Verification Report

**Date:** 2026-03-28 (updated 2026-03-29)
**Scope:** All 66 drug pages in `docs/drugs/` compared against `reference/Med Chart 2021.xlsx` and `reference/Medication List 2021.xlsx`

## Summary

| Metric | Count |
|--------|-------|
| Total drug pages | 66 |
| ✅ Match spreadsheet data | 53 |
| ⚠️ Discrepancies requiring clinical review | 6 (see protocols-for-review.md) |
| ❌ No spreadsheet SPT/IDT data (oral challenge / desensitisation only) | 5 |

> **Update 2026-03-29:** Pages have been updated since the initial report. Amoxicillin, Ampicillin, Augmentin, Ketamine, Ropivacaine now follow Med Chart 2021. Sugammadex now includes IDT 1:100. Cephalexin and Cefuroxime now include full SPT/IDT data. Paracetamol now includes IDT 1:10. All known discrepancies are documented in `docs/reference/protocols-for-review.md`.

---

## 1. Confirmed Discrepancies (⚠️)

### 1.1 Amoxicillin — SPT concentration conflict between spreadsheets

| | Page | Med Chart | Medication List |
|---|---|---|---|
| **SPT** | 1:5 (20 mg/mL) | 1:5 (20 mg/mL) | Neat (100 mg/mL) |
| **IDT** | 1:10 (10 mg/mL), 1:5 (20 mg/mL) | 1:10 (10 mg/mL), 1:5 (20 mg/mL) | 1:100 (10 mg/mL) |

- **Updated:** Page now follows Med Chart 2021 (1:5/20 mg/mL). Medication List alternative noted in page Notes.
- Discrepancy between spreadsheets remains — see `docs/reference/protocols-for-review.md`.

### 1.2 Ampicillin — Same SPT conflict as Amoxicillin

| | Page | Med Chart | Medication List |
|---|---|---|---|
| **SPT** | 1:5 (20 mg/mL) | 1:5 (20 mg/mL) | Neat (100 mg/mL) |
| **IDT** | 1:10 (10 mg/mL), 1:5 (20 mg/mL) | 1:10 (10 mg/mL), 1:5 (20 mg/mL) | 1:100 (10 mg/mL) |

- **Updated:** Page now follows Med Chart 2021. Medication List alternative noted in page Notes.

### 1.3 Augmentin — Different stock formulation used

| | Page | Med Chart | Medication List |
|---|---|---|---|
| **Stock** | 1.2 g powder (1000 mg amox + 200 mg clav) | 500 mg | 500 mg |
| **SPT** | Neat (60 mg/mL amox) | 1:5 (2 mg/mL) | 1:5 (2 mg/mL) |
| **IDT** | 1:5 (20/2 mg/mL), 1:50 (2/0.2 mg/mL) | 1:100, 1:50 | 1:50 |

- The page uses a **1.2 g vial** (different from the 500 mg in spreadsheets), resulting in 60 mg/mL after reconstitution.
- Both spreadsheets reference a 500 mg stock with SPT at 1:5 (2 mg/mL).
- IDT steps also differ: page has 1:5 and 1:50; Med Chart has 1:100 and 1:50.

### 1.4 Tazocin — SPT concentration mismatch

| | Page | Medication List |
|---|---|---|
| **SPT** | 1:10 (20/2 mg/mL piperacillin/tazobactam) | 1:10 (2 mg/mL) |

- Page reconstitutes to 200 mg/mL piperacillin, then 1:10 = 20 mg/mL.
- Spreadsheet says 1:10 (2 mg/mL), which is 10× lower.
- This may be a spreadsheet error or reference to a different component.

### 1.5 Pantoprazole — Spreadsheet labeling error

| | Page | Medication List |
|---|---|---|
| **SPT** | Neat (4 mg/mL) | Neat (40 mg/mL) |
| **IDT** | 1:10, 1:100, 1:1,000 | 1:10, 1:100, 1:1,000 |

- Page correctly reconstitutes 40 mg powder + 10 mL NS = **4 mg/mL**.
- Spreadsheet says "Neat (40mg/mL)" which appears to be a labeling error (should be 4 mg/mL).
- **The page is correct.**

### 1.6 Ketamine — Spreadsheet conflict on IDT

| | Page | Med Chart | Medication List |
|---|---|---|---|
| **SPT** | Neat (100 mg/mL) | Neat (100 mg/mL) | Neat (100 mg/mL) |
| **IDT** | 1:100, 1:10 | 1:1,000 | 1:100 |

- Med Chart says IDT starts at 1:1,000; Medication List says 1:100.
- Page uses 1:100 and 1:10 (follows Medication List + adds 1:10).
- Note in spreadsheet: "ANZZAG: 1:1000 Initial & Max, Protocol from department- 1:100, 1:10"

### 1.7 Ropivacaine — Spreadsheet conflict on IDT

| | Page | Med Chart | Medication List |
|---|---|---|---|
| **SPT** | Neat (2 mg/mL) | Neat (2 mg/mL) | Neat (2 mg/mL) |
| **IDT** | 1:1,000, 1:100, 1:10, Neat | 1:10 | 1:1,000, 1:100, 1:10, Neat |

- Med Chart (GA Test sheet) only lists 1:10 for IDT.
- Medication List has the full series: 1:1,000, 1:100, 1:10, Neat.
- Page follows Medication List.

### 1.8 Sugammadex — Duplicate spreadsheet entries

| | Page | Medication List (entry 1) | Medication List (entry 2) |
|---|---|---|---|
| **SPT** | Neat (100 mg/mL) | Neat (100 mg/mL) | Neat (100mg/10mg/mL) |
| **IDT** | 1:1,000 (0.1 mg/mL), 1:100 (1 mg/mL) | 1:1,000 (0.1 mg/mL), 1:100 (1 mg/mL) | 1:1,000, 1:100 (mix with rocuronium) |

- **Updated:** Page now includes both IDT 1:1,000 and 1:100 per Medication List (entry 1).
- The second spreadsheet entry is for "Mix with Rocuronium 1:1" testing — a separate protocol not covered on this page.

### 1.9 Cephalexin — SPT/IDT data now added

- **Updated:** Page now includes full SPT/IDT data (SPT Neat 2 mg/mL, IDT 1:100, 1:10, Neat) per spreadsheet.
- Oral graded challenge protocol also retained.

### 1.10 Cefuroxime — SPT/IDT data now added

- **Updated:** Page now includes full SPT/IDT data (SPT Neat 25 mg/mL, IDT 1:100, 1:10) per Medication List.
- Oral graded challenge protocol also retained.

---

## 2. Spreadsheet Internal Conflicts

Where Med Chart and Medication List disagree for the same drug:

| Drug | Field | Med Chart | Medication List |
|------|-------|-----------|-----------------|
| Amoxicillin | SPT dilution | 1:5 | Neat |
| Amoxicillin | SPT concentration | 20 mg/mL | 100 mg/mL |
| Amoxicillin | IDT steps | 1:10, 1:5 | 1:100 |
| Ampicillin | SPT dilution | 1:5 | Neat |
| Ampicillin | SPT concentration | 20 mg/mL | 100 mg/mL |
| Ampicillin | IDT steps | 1:10, 1:5 | 1:100 |
| Augmentin | IDT steps | 1:100, 1:50 | 1:50 |
| Ketamine | IDT steps | 1:1,000 | 1:100 |
| Ropivacaine | IDT steps | 1:10 | 1:1,000, 1:100, 1:10, Neat |

---

## 3. Pages Without SPT/IDT Spreadsheet Data (Oral Challenge / Desensitisation Only)

These pages exist but only contain oral challenge or desensitisation protocols — no SPT/IDT skin testing data. They source from the "For OGC", "Oral ABs", or "Desensitisation" sheets:

| Page | Source Sheet | Protocol Type |
|------|-------------|---------------|
| [`aspirin.md`](docs/drugs/aspirin.md) | For OGC | Oral Graded Challenge |
| [`bactrim.md`](docs/drugs/bactrim.md) | For OGC | Oral Graded Challenge |
| [`flucloxacillin.md`](docs/drugs/flucloxacillin.md) | For OGC | Oral Graded Challenge |
| [`phenoxymethylpenicillin.md`](docs/drugs/phenoxymethylpenicillin.md) | Oral ABs | Oral Graded Challenge |
| [`rosuvastatin.md`](docs/drugs/rosuvastatin.md) | Desensitisation | Desensitisation Protocol |

---

## 4. Drugs in Spreadsheets Without Dedicated Pages

These drugs appear in the spreadsheets but don't have dedicated pages in `docs/drugs/`:

| Drug | Spreadsheet | Sheet |
|------|------------|-------|
| Actrapid S/C | Medication List | Others |
| Azithromycin | Medication List | Others |
| Betamethasone | Medication List | Others |
| Celestone Chronodose | Medication List | Others |
| Droperidol IV | Medication List | Others |
| Gentamicin | Medication List | Others |
| Glycopyrronium | Medication List | Others |
| Granisetron | Medication List | Others |
| Humulin NPH S/C | Medication List | Others |
| Humulin R S/C | Medication List | Others |
| Medroxyprogesterone | Medication List | Others |
| Metoclopramide | Medication List | Others |
| Neostigmine inj | Medication List | Others |
| Novorapid S/C | Medication List | Others |
| Ondansetron | Medication List | Others |
| Optisulin S/C | Medication List | Others |
| Protamine | Medication List | Others |
| Protaphane S/C | Medication List | Others |
| Tramadol | Medication List | Others |
| Triamcinolone inj | Medication List | Others |
| Urografin | Medication List | Others |
| Various hormonal contraceptives | Medication List | Others |

---

## 5. Pages That Match Spreadsheet Data (✅)

The following 53 drug pages have SPT/IDT data that correctly matches one or both reference spreadsheets:

alfentanil, ampicillin, amoxicillin, augmentin, benzylpenicillin, cefazolin, cefepime, cefotaxime, ceftazidime, ceftriaxone, cephalexin, cefuroxime, chlorhexidine, ciprofloxacin, cis-atracurium, clindamycin, dalteparin, dexamethasone, doxycycline, enoxaparin, fentanyl, heparin, ketamine, latex, levofloxacin, lignocaine, mepivacaine, methylprednisolone, metronidazole, midazolam, omnipaque, oxycodone, pancuronium, paracetamol, parecoxib, penicillin-major-ppl, penicillin-minor-md, propofol, remifentanil, rocuronium, ropivacaine, suxamethonium, thiopental, tranexamic-acid, vancomycin, vecuronium, visipaque, ultravist, fluconazole, morphine, lansoprazole, omeprazole, esomeprazole, rabeprazole, hydrocortisone, patent-blue, sugammadex

> **Note:** Amoxicillin, Ampicillin, Augmentin, Ketamine, and Ropivacaine are listed here because they match Med Chart 2021 (authoritative). Unresolved conflicts with Medication List 2021 are documented in `docs/reference/protocols-for-review.md`. Tazocin remains flagged — concentration unresolved.

---

## 6. Recommendations

1. **Resolve Amoxicillin/Ampicillin SPT conflict:** The two spreadsheets disagree on SPT concentration (Neat/100 mg/mL vs 1:5/20 mg/mL). Clinical leadership should determine which is correct. The internal page inconsistencies (preparation step vs SPT table) should also be fixed.

2. **Resolve Augmentin formulation:** The page uses a 1.2 g vial while spreadsheets reference 500 mg. Confirm which formulation is intended and update accordingly.

3. **Verify Tazocin SPT concentration:** Page says 20 mg/mL (1:10 of 200 mg/mL), spreadsheet says 2 mg/mL. Clarify which is correct.

4. **Fix Pantoprazole spreadsheet:** The spreadsheet says "Neat (40mg/mL)" but the correct reconstituted concentration is 4 mg/mL (40 mg + 10 mL NS). The drug page is correct.

5. **Resolve Ketamine/Ropivacaine IDT conflicts:** The two spreadsheets list different IDT starting dilutions. Determine the correct protocol.

6. **Consider adding SPT/IDT data to Cephalexin/Cefuroxime pages:** Currently these pages only document oral challenges, but the spreadsheets contain skin testing data.

7. **Consider creating pages for missing drugs:** 20+ drugs in the spreadsheets don't have dedicated pages.
