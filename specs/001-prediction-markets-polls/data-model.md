# Data Model: Prediction Markets vs. Polls Story

## Entity: RaceDefinition

- **Purpose**: Defines one analytical row in the story.
- **Fields**:
  - `race_id`: Stable identifier such as `pres_2020` or `pa_senate_2022`
  - `race_label`: Reader-facing race name
  - `election_date`: Official election date
  - `eventual_winner`: Winning candidate or party/control outcome
  - `eventual_loser`: Opposing candidate or party/control outcome
  - `market_source_name`: Selected market source label
  - `market_source_url`: Source location for market data
  - `poll_source_name`: Selected polling source label
  - `poll_source_url`: Source location for polling data
- **Validation rules**:
  - `race_id` MUST be unique across the notebook
  - `eventual_winner` and `eventual_loser` MUST be distinct
  - `election_date` MUST be present for checkpoint calculation

## Entity: SourceAsset

- **Purpose**: Tracks a raw input file or remote dataset used in the analysis.
- **Fields**:
  - `asset_id`: Stable source identifier
  - `source_type`: Market or poll
  - `source_name`: Human-readable source name
  - `source_url`: Remote location or canonical file reference
  - `local_path`: Cached raw file path under `data/raw/`
  - `download_mode`: Checked-in or downloaded-at-runtime
  - `retrieved_at`: Retrieval timestamp when applicable
- **Validation rules**:
  - Every analytical row MUST reference at least one market and one polling
    asset
  - Downloaded assets MUST resolve to a deterministic cache path

## Entity: TimeSeriesObservation

- **Purpose**: Represents a normalized daily or weekly source observation before
  checkpoint classification.
- **Fields**:
  - `race_id`
  - `date`
  - `source_kind`: `market` or `poll`
  - `winner_value`: Observed value for the eventual winner
  - `loser_value`: Observed value for the eventual loser
  - `signal_type`: Probability, margin, vote share, or generic ballot share
  - `source_asset_id`
- **Validation rules**:
  - `date` MUST be parseable as a calendar date
  - Winner and loser values MUST be drawn from the same source snapshot
  - Source units MUST be documented before plotting or classification

## Entity: ProcessedRaceRecord

- **Purpose**: Final cleaned row written to a per-race processed CSV.
- **Fields**:
  - `date`
  - `market_prob_winner`
  - `market_prob_loser`
  - `poll_value_winner`
  - `poll_value_loser`
  - `source_market`
  - `source_poll`
- **Validation rules**:
  - Required columns MUST match the specification exactly
  - Rows MUST be sorted by ascending `date`
  - Values MUST reflect the finest practical regular interval available for that
    race

## Entity: CheckpointEvaluation

- **Purpose**: Stores the favored-side judgment for one race, source, and
  checkpoint.
- **Fields**:
  - `race_id`
  - `checkpoint_name`: `90d`, `30d`, or `eve`
  - `checkpoint_date`
  - `source_kind`
  - `observation_date_used`
  - `classification`: `yes`, `no`, or `toss-up`
  - `fallback_rule_used`
  - `reason`
- **Validation rules**:
  - Each race MUST have one evaluation per source per checkpoint
  - `classification` MUST be one of the allowed values
  - `observation_date_used` MUST be documented when it differs from
    `checkpoint_date`

## Entity: FigureArtifact

- **Purpose**: Describes a saved chart output for one analytical row.
- **Fields**:
  - `race_id`
  - `figure_path`
  - `chart_title`
  - `checkpoint_markers`
  - `notes`
- **Validation rules**:
  - Each analytical row MUST have one exported figure
  - Figure titles and labels MUST identify the race and the comparison being
    shown

## Relationships

- One `RaceDefinition` maps to many `TimeSeriesObservation` records.
- One `RaceDefinition` maps to many `ProcessedRaceRecord` rows in a single
  per-race CSV.
- One `RaceDefinition` maps to six `CheckpointEvaluation` records: three
  checkpoints times two source types.
- One `RaceDefinition` maps to one `FigureArtifact`.
- One `SourceAsset` can support multiple races if the same raw dataset covers
  more than one analytical row.
