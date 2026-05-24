---

description: "Task list for Prediction Markets vs. Polls Story"
---

# Tasks: Prediction Markets vs. Polls Story

**Input**: Design documents from `/specs/001-prediction-markets-polls/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Verification in this feature is driven by end-to-end notebook execution and output-file checks because the notebook is the primary deliverable.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3])
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the project shell and baseline dependency metadata

- [ ] T001 Create the notebook project directories in `prediction-markets-story/`, `prediction-markets-story/data/raw/`, `prediction-markets-story/data/processed/`, and `prediction-markets-story/figures/`
- [ ] T002 Create dependency pins and execution notes in `prediction-markets-story/requirements.txt`
- [ ] T003 [P] Create the project description and run instructions in `prediction-markets-story/README.md`
- [ ] T004 [P] Create placeholder keep-files for tracked empty directories in `prediction-markets-story/data/raw/.gitkeep`, `prediction-markets-story/data/processed/.gitkeep`, and `prediction-markets-story/figures/.gitkeep`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the notebook scaffolding and shared analysis rules that every story depends on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create the top-level notebook structure, imports, and narrative section headings in `prediction-markets-story/notebook.ipynb`
- [ ] T006 Implement shared configuration cells for project-relative paths, election dates, checkpoint dates, and toss-up thresholds in `prediction-markets-story/notebook.ipynb`
- [ ] T007 Implement source acquisition and raw-file caching helpers with docstrings in `prediction-markets-story/notebook.ipynb`
- [ ] T008 Implement shared normalization helpers for race definitions, source provenance, and date parsing in `prediction-markets-story/notebook.ipynb`
- [ ] T009 Implement shared checkpoint-selection and favored-side classification helpers using the non-lookahead rule in `prediction-markets-story/notebook.ipynb`
- [ ] T010 Implement shared figure-export and processed-CSV export helpers in `prediction-markets-story/notebook.ipynb`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Reproduce the full analysis notebook (Priority: P1) 🎯 MVP

**Goal**: Deliver a runnable notebook that loads all required source assets, builds the target project outputs, and can be executed from a clean clone without manual setup beyond dependency installation.

**Independent Test**: Execute `prediction-markets-story/notebook.ipynb` from top to bottom and confirm that it populates `data/raw/`, `data/processed/`, `figures/`, and the notebook narrative without any manual file downloads or path edits.

### Implementation for User Story 1

- [ ] T011 [US1] Add the introduction, methodology overview, and dependency/version notes to `prediction-markets-story/notebook.ipynb`
- [ ] T012 [US1] Implement first-run download or local-read logic for all required market and polling source assets in `prediction-markets-story/notebook.ipynb`
- [ ] T013 [US1] Implement the source inventory and inline source-documentation section in `prediction-markets-story/notebook.ipynb`
- [ ] T014 [US1] Implement the cleaned-output writer that creates one processed CSV per analytical row in `prediction-markets-story/notebook.ipynb`
- [ ] T015 [US1] Implement the notebook execution flow that creates required directories if absent and runs the full pipeline in `prediction-markets-story/notebook.ipynb`
- [ ] T016 [US1] Validate the notebook setup instructions and dependency list against the actual workflow in `prediction-markets-story/README.md`

**Checkpoint**: At this point, the notebook should run end to end and materialize the expected directory structure and output files

---

## Phase 4: User Story 2 - Compare who was favored at fixed checkpoints (Priority: P2)

**Goal**: Produce the race-level checkpoint classifications and the five-row summary table for the specified elections and chamber-control outcomes.

**Independent Test**: Run the notebook and inspect the processed CSVs plus summary table to confirm that all five analytical rows contain `yes`, `no`, or `toss-up` classifications for markets and the non-market comparison at 90 days, 30 days, and election eve.

### Implementation for User Story 2

- [ ] T017 [US2] Add the analytical row definitions for 2020 president, 2022 House control, 2022 Senate control, 2022 Pennsylvania Senate, and 2024 president in `prediction-markets-story/notebook.ipynb`
- [ ] T018 [US2] Implement market-series loading and normalization for all five analytical rows in `prediction-markets-story/notebook.ipynb`
- [ ] T019 [US2] Implement candidate-race polling-series loading and normalization for the 2020 presidential, 2022 Pennsylvania Senate, and 2024 presidential rows in `prediction-markets-story/notebook.ipynb`
- [ ] T020 [US2] Implement chamber-control forecast loading and normalization for the 2022 House control and 2022 Senate control rows in `prediction-markets-story/notebook.ipynb`
- [ ] T021 [US2] Implement per-race checkpoint extraction and favored-side classification for all rows in `prediction-markets-story/notebook.ipynb`
- [ ] T022 [US2] Implement the five-row summary table with the required columns in `prediction-markets-story/notebook.ipynb`
- [ ] T023 [US2] Verify that each file written under `prediction-markets-story/data/processed/` contains the required schema and date ordering in `prediction-markets-story/notebook.ipynb`

**Checkpoint**: At this point, the notebook should produce the complete cross-race comparison table and processed per-race datasets

---

## Phase 5: User Story 3 - Read a narrative story with race-level context (Priority: P3)

**Goal**: Turn the analysis into a readable story with per-race charts, written findings, methodological caveats, and a scoped final conclusion.

**Independent Test**: Read the rendered notebook from introduction through conclusion and confirm that each race has a chart, each race section has a short takeaway, the chamber-control methodology is explained, and the closing summary remains under 500 words.

### Implementation for User Story 3

- [ ] T024 [US3] Add the cleaning-and-alignment narrative section explaining unit differences, fallback rules, and chamber-control treatment in `prediction-markets-story/notebook.ipynb`
- [ ] T025 [US3] Implement the 2020 presidential race section, chart export, and short written finding in `prediction-markets-story/notebook.ipynb`
- [ ] T026 [US3] Implement the 2022 House control race section, chart export, and short written finding in `prediction-markets-story/notebook.ipynb`
- [ ] T027 [US3] Implement the 2022 Senate control race section, chart export, and short written finding in `prediction-markets-story/notebook.ipynb`
- [ ] T028 [US3] Implement the 2022 Pennsylvania Senate race section, chart export, and short written finding in `prediction-markets-story/notebook.ipynb`
- [ ] T029 [US3] Implement the 2024 presidential race section, chart export, and short written finding including the Polymarket concentration caveat in `prediction-markets-story/notebook.ipynb`
- [ ] T030 [US3] Implement the final findings and caveats section under 500 words in `prediction-markets-story/notebook.ipynb`

**Checkpoint**: All race sections should now be complete with figures, explanations, and a constrained final narrative

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate the complete deliverable and clean up supporting documentation

- [ ] T031 [P] Reconcile `prediction-markets-story/README.md` with the final notebook behavior, dependency pins, and output locations
- [ ] T032 Run end-to-end notebook execution and fix any reproducibility issues in `prediction-markets-story/notebook.ipynb`
- [ ] T033 Validate that all files in `prediction-markets-story/data/processed/` and `prediction-markets-story/figures/` are regenerated cleanly from notebook execution
- [ ] T034 Perform a final narrative review for terminology consistency, source traceability, and scope discipline in `prediction-markets-story/notebook.ipynb`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel if multiple contributors are available
  - Or sequentially in priority order (US1 → US2 → US3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational and establishes the runnable notebook shell
- **User Story 2 (P2)**: Starts after Foundational and depends on the notebook execution path from US1 being in place
- **User Story 3 (P3)**: Starts after Foundational and depends on US2’s analysis outputs to narrate race findings cleanly

### Within Each User Story

- Shared helpers and notebook scaffolding before story-specific sections
- Source loading before per-race normalization
- Normalization before checkpoint classification
- Classification before summary tables and written findings
- Notebook execution validation before final polish

### Parallel Opportunities

- `T003` and `T004` can run in parallel after `T001`
- `T031` can run in parallel with late-stage validation work once the notebook behavior stabilizes
- If the notebook is split into clearly separated sections during implementation, the per-race narrative tasks `T025` through `T029` can be distributed, but they should still merge into the same `prediction-markets-story/notebook.ipynb` carefully

---

## Parallel Example: User Story 3

```bash
Task: "Implement the 2020 presidential race section, chart export, and short written finding in prediction-markets-story/notebook.ipynb"
Task: "Implement the 2022 House control race section, chart export, and short written finding in prediction-markets-story/notebook.ipynb"
Task: "Implement the 2022 Senate control race section, chart export, and short written finding in prediction-markets-story/notebook.ipynb"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run the notebook end to end from a clean environment
5. Fix any reproducibility breaks before adding more analysis detail

### Incremental Delivery

1. Complete Setup + Foundational → notebook framework ready
2. Add User Story 1 → validate reproducible execution
3. Add User Story 2 → validate processed outputs and summary table
4. Add User Story 3 → validate race narratives and final conclusion
5. Finish Polish → rerun the full notebook and review outputs

### Parallel Team Strategy

With multiple contributors:

1. One contributor completes Setup + Foundational
2. One contributor stabilizes source ingestion and execution flow for US1
3. One contributor focuses on checkpoint classification logic for US2
4. One contributor drafts race narrative sections for US3 after the data outputs stabilize

---

## Notes

- [P] tasks = different files or late-stage work with no unresolved dependency on preceding tasks
- [US1], [US2], and [US3] labels map directly to the specification’s user stories
- Each user story has an explicit independent test so implementation can stop and validate incrementally
- The notebook is the primary product, so many tasks intentionally target `prediction-markets-story/notebook.ipynb`
- Chamber-control rows use a forecast source on the non-market side and must not be implemented as raw generic-ballot comparisons
