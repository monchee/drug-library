# SCRATCH Design Contract

Companion design contract for the SCRATCH clinical reference. This contract governs presentation only; it must never change clinical content.

## Positioning

- **Read-mode clinical reference.** SCRATCH is for reading, lookup, and print during allergy testing. Interaction is limited to navigation, search, theme toggle, and print.
- **SCRATCH references and DREAM records.** SCRATCH is the read-side reference companion; DREAM (https://dream.yuson.au) is the record/workbench side. SCRATCH links out to DREAM; DREAM never styles SCRATCH.

## Typography

- **Public Sans** for all UI text, headings, and body copy, with Inter and system font fallbacks.
- **JetBrains Mono** for data, code, drug concentrations, and dilution values.

## Surfaces and borders

- **Zero-radius surfaces and controls.** No rounded corners anywhere: surfaces, inputs, buttons, tables, admonitions, and badges use `border-radius: 0`.
- **1px borders** on all bordered surfaces, controls, and dividers.
- **8px spacing** rhythm across padding, gaps, and section margins.

## Colour

- **Navy masthead** (`#002664` light / `#001a45` dark) for header, tabs, and primary surfaces.
- **Pale NSW blue** (`#CBEDFD`) for hover/active interactions on light surfaces.
- **SLHD red** (`#D7153A`) reserved for clinical review warnings and a restrained identity edge (thin accent line); never used for decorative flair.
- **Light/dark semantic tokens** (background, foreground, card, muted, muted foreground, border, primary, interaction blue, warning red) defined per scheme; all components consume tokens, never raw values.

## Interaction

- **2px focus rings** on all keyboard-focusable elements.
- **Reduced motion:** honour `prefers-reduced-motion`; animations and transitions collapse to instant or minimal.

## Print

- **Print-first.** All content, tables, and dilution guides must print cleanly from the page without loss.
- Print output is black-on-white, full-width, with link URLs shown and interactive chrome hidden.
- The print utility is a fixed, square-cornered button with no transform, no broad shadow, and no rounded corners.

## Content integrity

- No clinical content changes are ever part of a design change.
- Design edits must not alter text, doses, dilutions, warnings, or protocols in `docs/`.
