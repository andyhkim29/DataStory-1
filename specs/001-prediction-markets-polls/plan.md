# Implementation Plan: Prediction Markets vs. Polls Story

**Branch**: `001-prediction-markets-polls` | **Date**: 2026-05-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-prediction-markets-polls/spec.md`

## Summary

Build a notebook-first data-story project that downloads or reads historical
prediction-market and polling datasets, normalizes them into per-race time
series, evaluates whether each source favored the eventual winner at the 90-day,
30-day, and election-eve checkpoints, and exports reproducible processed files,
charts, and a short narrative summary.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: pandas, numpy, plotly, requests, jupyter, nbformat,
nbconvert  
**Storage**: Repository files under `prediction-markets-story/data/` and
`prediction-markets-story/figures/`  
**Testing**: End-to-end notebook execution with `jupyter nbconvert --execute`
plus output-file verification  
**Target Platform**: Local developer machine running Jupyter on macOS or Linux  
**Project Type**: Single-project notebook analysis  
**Performance Goals**: Full notebook run completes in a few minutes and
recreates all required outputs deterministically  
**Constraints**: No manual data placement; minimal justified dependencies;
checkpoint rules must be deterministic; conclusions must stay within the five
specified analytical rows  
**Scale/Scope**: One notebook, five analytical rows, multiple raw source files,
five processed CSVs, five exported figures, one summary table

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Reproducibility First**: PASS. The plan centers the deliverable on a single
  notebook with deterministic local paths and automated source acquisition.
- **Source Traceability**: PASS. The plan requires inline source URLs, raw-data
  caching, provenance fields in processed outputs, and a dedicated output
  contract.
- **Methodological Honesty**: PASS. The plan compares favored side rather than
  forcing polling averages into win probabilities.
- **Deterministic Checkpoints**: PASS. The plan fixes the checkpoint definitions
  and nearest-valid fallback rule before implementation.
- **Scoped Claims and Reviewability**: PASS. The deliverable remains a readable
  notebook with five case-study rows and a constrained final writeup.

## Project Structure

### Documentation (this feature)

```text
specs/001-prediction-markets-polls/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── data-artifacts.md
└── tasks.md
```

### Source Code (repository root)

```text
prediction-markets-story/
├── notebook.ipynb
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
└── figures/
```

**Structure Decision**: Use a single notebook analysis project under
`prediction-markets-story/` because the notebook itself is the primary
deliverable. Supporting assets live beside it so a reviewer can clone the repo,
install dependencies, and run one entrypoint.

## Phase 0: Research Outcomes

- Choose a minimal Python notebook stack rather than a larger application
  framework.
- Prefer checked-in raw source files when small enough; otherwise automate
  first-run downloads into `data/raw/`.
- Use favored-side checkpoint classification rather than converting polls into
  synthetic win probabilities.
- Use nearest-valid observations with explicit provenance when exact checkpoint
  dates are missing.
- Verify the deliverable by executing the notebook end to end and checking for
  the required files.

## Phase 1: Design Outputs

- [research.md](./research.md) records the implementation decisions and rejected
  alternatives.
- [data-model.md](./data-model.md) defines the race metadata, source assets,
  normalized time-series records, processed output rows, checkpoint evaluations,
  and figure artifacts.
- [contracts/data-artifacts.md](./contracts/data-artifacts.md) defines the
  notebook execution contract plus the output-file and classification contracts.
- [quickstart.md](./quickstart.md) defines the setup, run, and verification
  flow for a reviewer.

## Post-Design Constitution Check

- **Reproducibility First**: PASS. Quickstart and contracts enforce one-command
  reruns and deterministic cache/output paths.
- **Source Traceability**: PASS. Data model and contracts require source names,
  URLs, cache paths, and provenance fields.
- **Methodological Honesty**: PASS. Research decisions explicitly reject
  synthetic poll-to-probability conversion.
- **Deterministic Checkpoints**: PASS. Contracts define checkpoint names,
  thresholds, and fallback expectations.
- **Scoped Claims and Reviewability**: PASS. The notebook remains the canonical
  review artifact and the plan constrains conclusions to the specified races.

## Complexity Tracking

No constitution violations or exceptional complexity require justification at
this stage.
