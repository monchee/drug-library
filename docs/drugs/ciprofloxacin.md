---
title: Ciprofloxacin
tags: [spt, oral, iv]
reviewed_by: RPAH Clinical Immunology & Allergy
last_reviewed: 2026-03-28
version: 1.2
dream:
  category: Others
protocols:
  - id: iv
    label: 'IV'
    test_type: skin
    presentation: '200mg/100mL'
    diluent: '0.9% sodium chloride'
    spt:
      dilution: 'Neat'
      concentration: '2mg/mL'
    idt:
      - dilution: '1:100'
        concentration: '0.04mg/mL'
    under_review: false
    review_note: ''
  - id: oral-graded-challenge
    label: 'Oral Graded Challenge'
    test_type: challenge
    presentation: 'Oral suspension'
    diluent: ''
    spt:
    challenge:
      steps:
        - dose: '50mg'
          volume: '1 mL'
          cumulative: '50mg'
        - dose: '125mg'
          volume: '2.5 mL'
          cumulative: '175mg'
        - dose: '250mg'
          volume: '5 mL'
          cumulative: '425mg'
        - dose: '500mg'
          volume: '10 mL'
          cumulative: '925mg'
    under_review: false
    review_note: ''
---

# Ciprofloxacin

## Overview
| Field | Detail |
|---|---|
| Drug class | Fluoroquinolone antibiotic |
| Stock formulation | 200 mg/100 mL IV (2 mg/mL) or 50 mg/mL Suspension |
| Reconstituted conc. | N/A (Ready to use) |
| Storage | Room temp |

---

## Preparation (IV Testing)

!!! info "Before you start"
    Check the formulation. IV Ciprofloxacin is usually pre-filled at **2 mg/mL**. No dilutions are typically required for SPT.

### Equipment needed
- 1 × Ciprofloxacin 2 mg/mL IV bag/vial
- Normal saline (NS) — for controls
- 1 mL syringes × 2
- 25 G needles

### Step 1 — Prepare the SPT solution (2 mg/mL — neat)
1. Draw up **0.5–1 mL** of the stock (2 mg/mL) into a 1 mL syringe.
2. Label: **"Ciprofloxacin SPT 2 mg/mL"**.

---

## Skin prick test (SPT)
<!-- scratch:spt:iv -->

**Interpretation:** Wheal ≥3 mm vs negative control = positive.

---

## Intradermal test (IDT)

### Dilution series

<!-- scratch:idt:iv -->

**Inject:** 0.05 mL intradermal. Read at 15–20 minutes.

---

---

## Oral Graded Challenge (OGC)
*Preferred for evaluating delayed hypersensitivity or confirming tolerance.*

!!! info "Suspension Preparation"
    Use **Ciprofloxacin 50 mg/mL Suspension** for precise dosing in oral challenges.

### Protocol
<!-- scratch:challenge:oral-graded-challenge -->
**Interval:** 20 minutes between steps.
**Final Step:** Consider a full therapeutic dose (e.g., 500 mg tablet) if earlier steps are negative.
