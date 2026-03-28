# Drug Page Verification Plan

## Objective
Systematically verify that all 65 drug pages in `docs/drugs/` accurately reflect the clinical data contained in the two reference Excel spreadsheets.

## Reference Sources
1. `reference/Med Chart 2021.xlsx` — Contains sheets: Drug Testing 1 Page, 2 Page Drug, Penicillins-NU, DAP-Penicillin, GA Test, Contrast, List of testing drug, Oral ABs, Drug Testing 2 Pages (2)
2. `reference/Medication List 2021.xlsx` — Contains sheets: Click This List, Local Anesthetics, Cephalosporin, Penicillin, Hypnotics, Opioids, Muscle Relaxant, PPI, Others, For OGC, For IV Challenge, For SC or IM Challenge, Desensitisation

## Data Points to Compare
For each drug, extract and compare:
- **Stock vial** concentration and form
- **SPT concentration** and dilution
- **IDT dilution series** — all steps with concentrations
- **Diluent** used
- **Oral/IV challenge protocol** if applicable

## Implementation Steps

### Step 1: Parse Reference Spreadsheets
- Use `openpyxl` to read both `.xlsx` files
- Iterate through all relevant sheets
- Extract drug names, SPT concentrations, IDT dilution series, stock info, diluents
- Normalize drug names for matching

### Step 2: Parse Drug Pages
- Read all 65 markdown files in `docs/drugs/`
- Extract structured data from each page:
  - Frontmatter metadata
  - Overview table data
  - SPT section concentration
  - IDT dilution series table
  - Challenge protocols
- Normalize drug names for matching

### Step 3: Systematic Comparison
- Match each drug page to its corresponding spreadsheet entries
- Compare all data points
- Flag discrepancies including:
  - Missing IDT steps
  - Wrong concentrations
  - Missing challenge protocols
  - Spreadsheet conflicts where the two sources disagree

### Step 4: Generate Report
- Create a markdown discrepancy report at `plans/discrepancy-report.md`
- Categories:
  1. **Page vs Spreadsheet mismatches** — data in page differs from spreadsheet
  2. **Missing drugs** — drugs in spreadsheets without pages
  3. **Orphan pages** — pages without corresponding spreadsheet entries
  4. **Spreadsheet conflicts** — where Med Chart and Medication List disagree

## Known Discrepancies Found So Far
1. **Amoxicillin**: Med Chart says SPT 1:5/20mg/mL, Medication List says SPT Neat/100mg/mL — page follows Med Chart
2. **Paracetamol**: Spreadsheet shows IDT at both 1:100 AND 1:10, but drug page only lists 1:100

## Script Location
`scripts/verify_drug_pages.py` — single script that performs all steps and outputs the report
