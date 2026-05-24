<!--
Sync Impact Report
- Version change: template -> 1.0.0
- Modified principles:
  - placeholder -> I. Reproducibility First
  - placeholder -> II. Source Traceability
  - placeholder -> III. Methodological Honesty
  - placeholder -> IV. Deterministic Checkpoints
  - placeholder -> V. Scoped Claims and Reviewability
- Added sections:
  - Delivery Constraints
  - Working Process
- Removed sections:
  - None
- Templates requiring updates:
  - ✅ reviewed, no changes required: .specify/templates/plan-template.md
  - ✅ reviewed, no changes required: .specify/templates/spec-template.md
  - ✅ reviewed, no changes required: .specify/templates/tasks-template.md
  - ✅ reviewed, no changes required: AGENTS.md
  - ✅ reviewed, no changes required: README.md
- Follow-up TODOs:
  - None
-->

# DataStory-1 Constitution

## Core Principles

### I. Reproducibility First
Every analysis deliverable MUST run from a clean project checkout with no hidden
state, no manual file placement, and no machine-specific paths. Notebooks,
scripts, and data transformations MUST recreate the same processed outputs and
figures when rerun with the documented environment. If a source asset cannot be
stored in the repository, the project MUST automate its retrieval inside the
workflow.

### II. Source Traceability
Every published number, chart, and classification MUST be traceable to a named
source asset and a documented transformation step. Raw source files MUST remain
untouched in a raw-data location or be fetched verbatim, while cleaned outputs
MUST preserve provenance fields sufficient for another reviewer to audit the
result. Missing data, source substitutions, and cross-validation choices MUST be
explicitly documented in the analysis artifact.

### III. Methodological Honesty
The project MUST describe each comparison in terms that match what the
underlying data actually measures. When two sources capture different concepts,
the notebook and supporting materials MUST state the mismatch, justify the
comparison method, and avoid overstating equivalence. Convenience conversions
that imply more certainty than the data supports are prohibited unless the
conversion method is itself a documented analytical object of the story.

### IV. Deterministic Checkpoints
Every story that compares races across time MUST define checkpoint dates,
classification thresholds, and fallback rules before interpretation. The same
decision rules MUST be applied across all covered races unless an exception is
documented inline with a concrete reason. If an exact observation is
unavailable, the selected nearest observation rule MUST be explicit and applied
consistently.

### V. Scoped Claims and Reviewability
Conclusions MUST stay within the scope of the analyzed cases and the evidence
actually assembled. Narrative summaries MUST distinguish observed outcomes from
general claims, and caveats that materially affect interpretation MUST appear in
the final story, not only in code comments. Every major deliverable MUST remain
readable to a reviewer who is assessing the argument rather than the code.

## Delivery Constraints

The canonical deliverable for this project is a narrative notebook supported by
versioned data artifacts and exported figures. Repository structure MUST keep
raw inputs, processed outputs, notebook logic, and exported visuals clearly
separated. Dependencies MUST stay minimal and justified; non-standard packages
require an explicit reason in the notebook or project documentation. Generated
artifacts committed to the repository MUST be reproducible from source inputs
and checked for size, clarity, and relevance.

## Working Process

Each feature specification MUST define the analytical question, the deliverable,
the source set, and the acceptance criteria for reproducibility before planning
begins. Implementation plans MUST include a constitution check that confirms the
workflow preserves reproducibility, traceability, methodological honesty, and
scope discipline. Task breakdowns MUST include work for source acquisition,
cleaning, verification, narrative writeup, and output validation whenever those
concerns are part of the deliverable. Before a feature is considered complete,
the team MUST rerun the notebook or equivalent entrypoint end to end and review
whether the final written claims still match the produced evidence.

## Governance

This constitution governs project decisions that affect analysis quality,
storytelling claims, and delivery standards. All specifications, plans, tasks,
reviews, and final outputs MUST be checked against these principles. Amendments
require a documented rationale, an explicit semantic version decision, and a
sync review of affected templates or guidance files. Major version bumps apply
when a principle is removed or materially redefined, minor version bumps apply
when a new principle or mandatory section is added, and patch bumps apply to
clarifications that do not change project obligations. Compliance review occurs
at specification, planning, implementation, and final verification time, with
the current implementation plan serving as the runtime guidance document for
day-to-day execution.

**Version**: 1.0.0 | **Ratified**: 2026-05-24 | **Last Amended**: 2026-05-24
