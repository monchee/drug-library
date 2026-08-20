# DREAM ↔ SCRATCH protocol mapping — DRAFT, UNVERIFIED

Generated automatically. **Every row needs hand-verification before Phase 1 uses it.**
A script must not decide a drug identity; it only proposes one.

`match` column: `auto` = normalised name matched a page; `alias` = hand-curated guess;
`GAP` = no SCRATCH page found, needs a decision.

Proposed `id` is derived from the DREAM protocolLabel and must be unique within its page.

> **Ids need hand-choosing.** The auto-derived ids are mechanical and some are ugly —
> `1:1,000 start` becomes `1-1-000-start`. Pick readable, stable ids before migrating a page;
> once DREAM stores an id in a saved plan, changing it is a breaking change.

| DREAM drugName | DREAM category | test_type | protocolLabel | IDT | Chal | → SCRATCH slug | proposed id | match |
|---|---|---|---|--:|--:|---|---|---|
| Cis-atracurium | Muscle Relaxants | skin | IV | 1 | 0 | `cis-atracurium` | `iv` | auto |
| Rocuronium | Muscle Relaxants | skin | IV | 2 | 0 | `rocuronium` | `iv` | auto |
| Pancuronium | Muscle Relaxants | skin | IV | 2 | 0 | `pancuronium` | `iv` | auto |
| Vecuronium | Muscle Relaxants | skin | IV | 2 | 0 | `vecuronium` | `iv` | auto |
| Suxamethonium | Muscle Relaxants | skin | IV | 3 | 0 | `suxamethonium` | `iv` | auto |
| Sugammadex (Alone) | Reversal Agents | skin | Alone | 2 | 0 | `sugammadex` | `alone` | auto |
| Sugammadex (+ Rocuronium) | Reversal Agents | skin | + Rocuronium | 2 | 0 | `sugammadex` | `rocuronium` | auto |
| Penicillin Major | Penicillins | skin | PPL | 2 | 0 | `penicillin-major-ppl` | `ppl` | alias |
| Penicillin Minor | Penicillins | skin | MD | 2 | 0 | `penicillin-minor-md` | `md` | alias |
| Ampicillin | Penicillins | skin | Neat SPT | 3 | 0 | `ampicillin` | `neat-spt` | auto |
| Ampicillin | Penicillins | skin | 1:5 SPT | 3 | 0 | `ampicillin` | `1-5-spt` | auto |
| Ampicillin | Penicillins | control | Control | 3 | 0 | `ampicillin` | `control` | auto |
| Amoxycillin | Penicillins | skin | Neat SPT | 2 | 0 | `amoxicillin` | `neat-spt` | auto |
| Amoxycillin | Penicillins | skin | 1:5 SPT | 2 | 0 | `amoxicillin` | `1-5-spt` | auto |
| Benzylpenicillin | Penicillins | skin | 1:1,000 start | 2 | 0 | `benzylpenicillin` | `1-1-000-start` | auto |
| Benzylpenicillin | Penicillins | skin | 1:100 start | 3 | 0 | `benzylpenicillin` | `1-100-start` | auto |
| Benzylpenicillin | Penicillins | control | Control | 2 | 0 | `benzylpenicillin` | `control` | auto |
| Augmentin | Penicillins | skin | 1:1,000 start | 3 | 0 | `augmentin` | `1-1-000-start` | auto |
| Augmentin | Penicillins | skin | 1:100 start | 3 | 0 | `augmentin` | `1-100-start` | auto |
| Cephalexin | Penicillins | skin | IV | 3 | 0 | `cephalexin` | `iv` | auto |
| Tazocin | Penicillins | skin | IV | 2 | 0 | `tazocin` | `iv` | auto |
| Methoxybenzylpenicillin | Penicillins | skin | — | 0 | 0 | `—` | `skin` | **GAP** |
| Cefazolin | Cephalosporins | skin | IV | 2 | 0 | `cefazolin` | `iv` | auto |
| Cefepime | Cephalosporins | skin | IV | 2 | 0 | `cefepime` | `iv` | auto |
| Cefotaxime | Cephalosporins | skin | IV | 2 | 0 | `cefotaxime` | `iv` | auto |
| Ceftazidime | Cephalosporins | skin | IV | 2 | 0 | `ceftazidime` | `iv` | auto |
| Ceftriaxone | Cephalosporins | skin | IV | 2 | 0 | `ceftriaxone` | `iv` | auto |
| Cefuroxime | Cephalosporins | skin | IV | 2 | 0 | `cefuroxime` | `iv` | auto |
| Midazolam | Hypnotics | skin | IV | 1 | 0 | `midazolam` | `iv` | auto |
| Propofol | Hypnotics | skin | IV | 2 | 0 | `propofol` | `iv` | auto |
| Ketamine | Hypnotics | skin | 1:1,000 start | 3 | 0 | `ketamine` | `1-1-000-start` | auto |
| Ketamine | Hypnotics | skin | 1:100 start | 1 | 0 | `ketamine` | `1-100-start` | auto |
| Thiopental | Hypnotics | skin | 1:1,000 start | 3 | 0 | `thiopental` | `1-1-000-start` | auto |
| Thiopental | Hypnotics | skin | 1:100 start | 3 | 0 | `thiopental` | `1-100-start` | auto |
| Lignocaine | Local Anaesthetics | skin | IV | 4 | 0 | `lignocaine` | `iv` | auto |
| Mepivacaine | Local Anaesthetics | skin | Epidural | 4 | 0 | `mepivacaine` | `epidural` | auto |
| Bupivacaine | Local Anaesthetics | skin | Epidural | 4 | 0 | `bupivacaine` | `epidural` | auto |
| Ropivacaine | Local Anaesthetics | skin | Epidural Protocol 1 | 4 | 0 | `ropivacaine` | `epidural-protocol-1` | auto |
| Ropivacaine | Local Anaesthetics | skin | Epidural Protocol 2 | 2 | 0 | `ropivacaine` | `epidural-protocol-2` | auto |
| Alfentanil | Opioids | skin | IV | 2 | 0 | `alfentanil` | `iv` | auto |
| Fentanyl | Opioids | skin | IV | 2 | 0 | `fentanyl` | `iv` | auto |
| Morphine | Opioids | skin | 1:1,000 start | 2 | 0 | `morphine` | `1-1-000-start` | auto |
| Morphine | Opioids | skin | 1:100 start | 2 | 0 | `morphine` | `1-100-start` | auto |
| Remifentanil | Opioids | skin | 1:1,000 start | 2 | 0 | `remifentanil` | `1-1-000-start` | auto |
| Remifentanil | Opioids | skin | 1:100 start | 3 | 0 | `remifentanil` | `1-100-start` | auto |
| Oxycodone | Opioids | skin | IV | 2 | 0 | `oxycodone` | `iv` | auto |
| Chlorhexidine | Antiseptics | skin | 0.02% | 1 | 0 | `chlorhexidine` | `0-02` | auto |
| Povidone Iodine | Antiseptics | skin | 1:1,000 start | 3 | 0 | `povidone-iodine` | `1-1-000-start` | auto |
| Povidone Iodine | Antiseptics | skin | 1:100 start | 3 | 0 | `povidone-iodine` | `1-100-start` | auto |
| Esomeprazole | Proton Pump Inhibitors | skin | — | 0 | 0 | `esomeprazole` | `skin` | auto |
| Lansoprazole | Proton Pump Inhibitors | skin | — | 0 | 0 | `lansoprazole` | `skin` | auto |
| Omeprazole | Proton Pump Inhibitors | skin | — | 0 | 0 | `omeprazole` | `skin` | auto |
| Pantoprazole | Proton Pump Inhibitors | skin | IV | 3 | 0 | `pantoprazole` | `iv` | auto |
| Rabeprazole | Proton Pump Inhibitors | skin | — | 0 | 0 | `rabeprazole` | `skin` | auto |
| Actrapid (Insulin) | Others | skin | S/C | 1 | 0 | `actrapid` | `s-c` | auto |
| Azithromycin | Others | skin | IV | 3 | 0 | `azithromycin` | `iv` | auto |
| Betamethasone | Others | experimental | IV | 2 | 0 | `betamethasone` | `iv` | auto |
| Cefuroxime Suspension | Others | skin | Suspension | 1 | 0 | `cefuroxime` | `suspension` | alias |
| Ciprofloxacin | Others | skin | IV | 1 | 0 | `ciprofloxacin` | `iv` | auto |
| Clindamycin | Others | skin | IV | 2 | 0 | `clindamycin` | `iv` | auto |
| Dalteparin | Others | skin | SC | 3 | 0 | `dalteparin` | `sc` | auto |
| Dexamethasone | Others | skin | IV | 2 | 0 | `dexamethasone` | `iv` | auto |
| Doxycycline | Others | skin | 1:1,000 start | 3 | 0 | `doxycycline` | `1-1-000-start` | auto |
| Doxycycline | Others | skin | 1:100 start | 3 | 0 | `doxycycline` | `1-100-start` | auto |
| Droperidol | Others | skin | IV | 2 | 0 | `droperidol` | `iv` | auto |
| Enoxaparin | Others | skin | SC | 3 | 0 | `enoxaparin` | `sc` | auto |
| Fluconazole | Others | skin | IV | 3 | 0 | `fluconazole` | `iv` | auto |
| Glycopyrronium | Others | experimental | — | 2 | 0 | `glycopyrronium` | `experimental` | auto |
| Granisetron | Others | skin | IV | 2 | 0 | `granisetron` | `iv` | auto |
| Heparin | Others | skin | SC | 3 | 0 | `heparin` | `sc` | auto |
| Humulin NPH (Insulin) | Others | skin | S/C | 1 | 0 | `humulin-nph` | `s-c` | auto |
| Humulin R (Insulin) | Others | skin | S/C | 1 | 0 | `humulin-r` | `s-c` | auto |
| Hydrocortisone | Others | experimental | IV | 2 | 0 | `hydrocortisone` | `iv` | auto |
| Latex | Others | skin | — | 0 | 0 | `latex` | `skin` | auto |
| Levofloxacin | Others | skin | Tablet | 1 | 0 | `levofloxacin` | `tablet` | auto |
| Levonorgestrel | Others | skin | Oral | 1 | 0 | `levonorgestrel` | `oral` | auto |
| Medroxyprogesterone | Others | skin | Inj | 2 | 0 | `medroxyprogesterone` | `inj` | auto |
| Metacresol | Others | skin | 1:1,000 start | 1 | 0 | `metacresol` | `1-1-000-start` | auto |
| Metacresol | Others | skin | 1:100 start | 1 | 0 | `metacresol` | `1-100-start` | auto |
| Methylprednisolone | Others | experimental | IV | 3 | 0 | `methylprednisolone` | `iv` | auto |
| Metoclopramide | Others | skin | IV | 2 | 0 | `metoclopramide` | `iv` | auto |
| Metronidazole | Others | skin | IV | 2 | 0 | `metronidazole` | `iv` | auto |
| Neostigmine | Others | experimental | Inj | 2 | 0 | `neostigmine` | `inj` | auto |
| Novorapid (Insulin) | Others | skin | S/C | 1 | 0 | `novorapid` | `s-c` | auto |
| Omnipaque | Others | skin | IV Contrast | 2 | 0 | `omnipaque` | `iv-contrast` | auto |
| Ondansetron | Others | skin | IV | 2 | 0 | `ondansetron` | `iv` | auto |
| Optisulin (Insulin) | Others | skin | S/C | 1 | 0 | `optisulin` | `s-c` | auto |
| Paracetamol | Others | skin | IV | 2 | 0 | `paracetamol` | `iv` | auto |
| Parecoxib | Others | skin | IV | 1 | 0 | `parecoxib` | `iv` | auto |
| Patent Blue | Others | skin | SC | 2 | 0 | `patent-blue` | `sc` | auto |
| Protamine | Others | skin | IV | 2 | 0 | `protamine` | `iv` | auto |
| Protaphane (Insulin) | Others | skin | S/C | 1 | 0 | `protaphane` | `s-c` | auto |
| Tranexamic Acid | Others | skin | IV | 3 | 0 | `tranexamic-acid` | `iv` | auto |
| Tramadol | Others | experimental | IV | 1 | 0 | `tramadol` | `iv` | auto |
| Triamcinolone | Others | experimental | Inj | 3 | 0 | `triamcinolone` | `inj` | auto |
| Ultravist | Others | skin | IV Contrast | 2 | 0 | `ultravist` | `iv-contrast` | auto |
| Ultravist | Others | control | Control | 2 | 0 | `ultravist` | `control` | auto |
| Urografin | Others | skin | IV Contrast | 2 | 0 | `urografin` | `iv-contrast` | auto |
| Vancomycin | Others | skin | IV | 2 | 0 | `vancomycin` | `iv` | auto |
| Visipaque | Others | skin | IV Contrast | 2 | 0 | `visipaque` | `iv-contrast` | auto |
| Xylocaine | Others | skin | IV | 4 | 0 | `xylocaine` | `iv` | auto |
| Methylene Blue | Others | skin | — | 0 | 0 | `—` | `skin` | **GAP** |
| IV Contrast | Others | skin | — | 0 | 0 | `—` | `skin` | **GAP** |
| Atropine | Others | skin | — | 0 | 0 | `—` | `skin` | **GAP** |
| Amoxycillin Suspension | Others | challenge | Oral Graded Challenge | 0 | 4 | `amoxicillin` | `oral-graded-challenge` | alias |
| Amoxycillin/Clavulanic Acid | Others | challenge | Oral Graded Challenge | 0 | 4 | `augmentin` | `oral-graded-challenge` | alias |
| Cefazolin | Cephalosporins | challenge | IV Challenge | 0 | 4 | `cefazolin` | `iv-challenge` | auto |
| Cephalexin | Penicillins | challenge | Oral Graded Challenge | 0 | 4 | `cephalexin` | `oral-graded-challenge` | auto |
| Ciprofloxacin | Others | challenge | Oral Graded Challenge | 0 | 4 | `ciprofloxacin` | `oral-graded-challenge` | auto |
| Doxycycline | Others | challenge | Oral Graded Challenge | 0 | 3 | `doxycycline` | `oral-graded-challenge` | auto |
| Flucloxacillin | Penicillins | challenge | Oral Graded Challenge | 0 | 3 | `flucloxacillin` | `oral-graded-challenge` | auto |
| Lignocaine | Local Anaesthetics | challenge | Challenge | 0 | 1 | `lignocaine` | `challenge` | auto |
| Meloxicam | Others | challenge | Graded Challenge | 0 | 2 | `—` | `graded-challenge` | **GAP** |
| Trimethoprim/Sulfamethoxazole | Others | challenge | Oral Graded Challenge | 0 | 3 | `bactrim` | `oral-graded-challenge` | alias |
| Trimethoprim | Others | challenge | Oral Graded Challenge | 0 | 3 | `bactrim` | `oral-graded-challenge` | alias |
| Voltaren (Diclofenac) | Others | challenge | Graded Challenge | 0 | 3 | `—` | `graded-challenge` | **GAP** |

## Summary

- DREAM protocol records: **116**
- Mapped to a SCRATCH page: **110**
- Unmapped (`dream-only` or missing page): **6**

### DREAM records with no SCRATCH page — decide per drug

Either author a SCRATCH page, or mark the record `dream-only` and keep it in `DREAM_ONLY_PROTOCOLS`.

- [ ] Atropine
- [ ] IV Contrast
- [ ] Meloxicam
- [ ] Methoxybenzylpenicillin
- [ ] Methylene Blue
- [ ] Voltaren (Diclofenac)

### SCRATCH pages with no DREAM record — decide per page

Either add it to DREAM's testing panel with a `dream.category`, or omit the `dream:` key so the exporter excludes it.

- [ ] `aspirin`
- [ ] `celestone-chronodose`
- [ ] `cyproterone-ethinylestradiol`
- [ ] `drospirenone-ethinylestradiol`
- [ ] `ethinylestradiol-levonorgestrel`
- [ ] `ethinylestradiol-norethisterone`
- [ ] `gentamicin`
- [ ] `phenoxymethylpenicillin`
- [ ] `rosuvastatin`

### Multi-variant drugs — HIGHEST RISK, verify each variant individually

DREAM currently selects these by array position. Assigning an id to the wrong variant re-points a saved clinical plan at a different dose. Check the actual doses, not just the label.

- [ ] **Amoxycillin** (2 variants): `neat-spt`, `1-5-spt`
- [ ] **Ampicillin** (3 variants): `neat-spt`, `1-5-spt`, `control`
- [ ] **Augmentin** (2 variants): `1-1-000-start`, `1-100-start`
- [ ] **Benzylpenicillin** (3 variants): `1-1-000-start`, `1-100-start`, `control`
- [ ] **Cefazolin** (2 variants): `iv`, `iv-challenge`
- [ ] **Cephalexin** (2 variants): `iv`, `oral-graded-challenge`
- [ ] **Ciprofloxacin** (2 variants): `iv`, `oral-graded-challenge`
- [ ] **Doxycycline** (3 variants): `1-1-000-start`, `1-100-start`, `oral-graded-challenge`
- [ ] **Ketamine** (2 variants): `1-1-000-start`, `1-100-start`
- [ ] **Lignocaine** (2 variants): `iv`, `challenge`
- [ ] **Metacresol** (2 variants): `1-1-000-start`, `1-100-start`
- [ ] **Morphine** (2 variants): `1-1-000-start`, `1-100-start`
- [ ] **Povidone Iodine** (2 variants): `1-1-000-start`, `1-100-start`
- [ ] **Remifentanil** (2 variants): `1-1-000-start`, `1-100-start`
- [ ] **Ropivacaine** (2 variants): `epidural-protocol-1`, `epidural-protocol-2`
- [ ] **Thiopental** (2 variants): `1-1-000-start`, `1-100-start`
- [ ] **Ultravist** (2 variants): `iv-contrast`, `control`
