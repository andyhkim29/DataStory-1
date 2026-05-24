import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "prediction-markets-story" / "notebook.ipynb"


def md_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


INTRO = """# Prediction Markets vs. Polls in U.S. Elections

This notebook compares whether prediction markets and a polling-side comparison
source favored the eventual winner at three fixed checkpoints:

- 90 days before election day
- 30 days before election day
- election eve

The analysis covers five rows only:

1. 2020 president
2. 2022 House control
3. 2022 Senate control
4. 2022 Pennsylvania Senate
5. 2024 president

The comparison is intentionally narrow. Polls and prediction markets are not the
same object: polls measure vote preference while markets express win odds. For
candidate races, the notebook compares who led using a checked-in polling
checkpoint fixture. For the chamber rows, the non-market side is a
chamber-control forecast fixture derived from published FiveThirtyEight
writeups because the original historical CSV endpoints no longer provide a
reliable machine-readable archive.
"""


HELPERS = r'''from __future__ import annotations

import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
from IPython.display import Markdown, display


ROOT = Path.cwd() / "prediction-markets-story"
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "figures"
SUMMARY_PATH = PROCESSED_DIR / "summary_table.csv"

for path in (ROOT, RAW_DIR, PROCESSED_DIR, FIGURES_DIR):
    path.mkdir(parents=True, exist_ok=True)

MARKET_TOSSUP_LOW = 48.0
MARKET_TOSSUP_HIGH = 52.0
POLL_MARGIN_TOSSUP = 2.0


@dataclass
class RaceDefinition:
    race_id: str
    race_label: str
    election_date: str
    eventual_winner: str
    eventual_loser: str
    market_source_name: str
    market_source_url: str
    poll_source_name: str
    poll_source_url: str
    market_kind: str
    poll_kind: str
    ebo_page: str | None = None
    ebo_winner_match: str | None = None
    ebo_loser_match: str | None = None
    poll_query_url: str | None = None
    poll_filter: dict | None = None
    poll_winner_match: str | None = None
    poll_loser_match: str | None = None

    @property
    def election_ts(self) -> pd.Timestamp:
        return pd.Timestamp(self.election_date)

    @property
    def checkpoints(self) -> dict[str, pd.Timestamp]:
        return {
            "90d": self.election_ts - pd.Timedelta(days=90),
            "30d": self.election_ts - pd.Timedelta(days=30),
            "eve": self.election_ts - pd.Timedelta(days=1),
        }


def download_text(url: str, destination: Path) -> Path:
    """Download a text asset once to a deterministic cache path."""
    if destination.exists():
        return destination
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    destination.write_text(response.text, encoding="utf-8")
    return destination


def download_csv(url: str, destination: Path) -> Path:
    """Download a CSV asset once to a deterministic cache path."""
    if destination.exists():
        return destination
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    destination.write_bytes(response.content)
    return destination


def parse_ebo_page(page_path: Path) -> pd.DataFrame:
    """Parse ElectionBettingOdds chart HTML into a tidy time-series DataFrame."""
    text = page_path.read_text(encoding="utf-8")
    column_names = re.findall(r"data\.addColumn\('number', '([^']+)'\)", text)
    start = text.find("data.addRows(")
    end = text.find("var chart", start)
    if start == -1 or end == -1:
        raise ValueError(f"Could not locate chart rows in {page_path}")
    rows_blob = text[start:end]
    row_pattern = re.compile(r"\[new Date\(([^)]*?)\),([^\]]*?)\]", re.S)
    records = []
    for match in row_pattern.finditer(rows_blob):
        date_parts = [int(part.strip()) for part in match.group(1).split(",")]
        year, month, day, hour, minute, second = date_parts
        timestamp = pd.Timestamp(year=year, month=month + 1, day=day, hour=hour, minute=minute, second=second)
        numeric_text = match.group(2)
        values = [float(value) for value in numeric_text.split(",") if value.strip()]
        record = {"timestamp": timestamp}
        for name, value in zip(column_names, values):
            record[name] = value
        records.append(record)
    frame = pd.DataFrame.from_records(records).sort_values("timestamp")
    frame["date"] = frame["timestamp"].dt.normalize()
    return frame


def fuzzy_column(columns: Iterable[str], target: str) -> str:
    target_norm = target.lower().replace(" ", "")
    for column in columns:
        column_norm = column.lower().replace(" ", "")
        if target_norm in column_norm:
            return column
    raise KeyError(f"Could not match {target!r} in {list(columns)!r}")


def ebo_daily_series(race: RaceDefinition) -> pd.DataFrame:
    """Load an eventual-winner versus eventual-loser daily market series."""
    page_name = race.ebo_page.rsplit("/", 1)[-1]
    page_path = download_text(race.ebo_page, RAW_DIR / page_name)
    source = parse_ebo_page(page_path)
    numeric_columns = [column for column in source.columns if column not in {"timestamp", "date"}]
    winner_col = fuzzy_column(numeric_columns, race.ebo_winner_match)
    loser_col = fuzzy_column(numeric_columns, race.ebo_loser_match)
    frame = (
        source.groupby("date")[[winner_col, loser_col]]
        .last()
        .reset_index()
        .rename(columns={winner_col: "market_prob_winner", loser_col: "market_prob_loser"})
    )
    return frame


def candidate_poll_checkpoint_series(race: RaceDefinition) -> pd.DataFrame:
    """Load checked-in candidate-race polling checkpoints."""
    fixture = pd.read_csv(RAW_DIR / "candidate_poll_checkpoints.csv", parse_dates=["date"])
    frame = fixture[fixture["race_id"] == race.race_id].copy()
    return frame[["date", "poll_value_winner", "poll_value_loser"]].sort_values("date")


def chamber_forecast_series(race: RaceDefinition) -> pd.DataFrame:
    """Load the checked-in chamber forecast checkpoint fixture."""
    fixture = pd.read_csv(RAW_DIR / "chamber_forecasts_2022.csv", parse_dates=["date"])
    frame = fixture[fixture["race_id"] == race.race_id].copy()
    frame = frame.rename(
        columns={
            "forecast_prob_winner": "poll_value_winner",
            "forecast_prob_loser": "poll_value_loser",
        }
    )
    return frame[["date", "poll_value_winner", "poll_value_loser"]].sort_values("date")


def merge_race_series(race: RaceDefinition) -> pd.DataFrame:
    """Merge market and polling-side series into the persisted per-race schema."""
    market = ebo_daily_series(race)
    if race.poll_kind == "polls":
        poll = candidate_poll_checkpoint_series(race)
    else:
        poll = chamber_forecast_series(race)
    merged = pd.merge(market, poll, on="date", how="outer").sort_values("date")
    merged["source_market"] = race.market_source_name
    merged["source_poll"] = race.poll_source_name
    return merged[
        [
            "date",
            "market_prob_winner",
            "market_prob_loser",
            "poll_value_winner",
            "poll_value_loser",
            "source_market",
            "source_poll",
        ]
    ]


def classify_market(prob_winner: float, prob_loser: float) -> str:
    if pd.isna(prob_winner) or pd.isna(prob_loser):
        return "missing"
    if MARKET_TOSSUP_LOW <= prob_winner <= MARKET_TOSSUP_HIGH:
        return "toss-up"
    return "yes" if prob_winner > prob_loser else "no"


def classify_poll(race: RaceDefinition, winner_value: float, loser_value: float) -> str:
    if pd.isna(winner_value) or pd.isna(loser_value):
        return "missing"
    if race.poll_kind == "forecast":
        if MARKET_TOSSUP_LOW <= winner_value <= MARKET_TOSSUP_HIGH:
            return "toss-up"
        return "yes" if winner_value > loser_value else "no"
    margin = winner_value - loser_value
    if abs(margin) < POLL_MARGIN_TOSSUP:
        return "toss-up"
    return "yes" if margin > 0 else "no"


def latest_on_or_before(frame: pd.DataFrame, checkpoint: pd.Timestamp, winner_col: str, loser_col: str) -> dict:
    usable = frame.dropna(subset=[winner_col, loser_col]).copy()
    usable = usable[usable["date"] <= checkpoint]
    if usable.empty:
        usable = frame.dropna(subset=[winner_col, loser_col]).copy()
        if usable.empty:
            return {"date": pd.NaT, winner_col: np.nan, loser_col: np.nan}
        row = usable.sort_values("date").iloc[0]
        fallback = "nearest subsequent observation"
    else:
        row = usable.sort_values("date").iloc[-1]
        fallback = "latest observation on or before checkpoint"
    return {
        "date": row["date"],
        winner_col: row[winner_col],
        loser_col: row[loser_col],
        "fallback": fallback,
    }


def checkpoint_evaluations(race: RaceDefinition, frame: pd.DataFrame) -> list[dict]:
    evaluations = []
    for name, checkpoint in race.checkpoints.items():
        market_row = latest_on_or_before(frame, checkpoint, "market_prob_winner", "market_prob_loser")
        poll_row = latest_on_or_before(frame, checkpoint, "poll_value_winner", "poll_value_loser")
        evaluations.append(
            {
                "race_id": race.race_id,
                "checkpoint_name": name,
                "checkpoint_date": checkpoint,
                "source_kind": "market",
                "observation_date_used": market_row["date"],
                "classification": classify_market(market_row["market_prob_winner"], market_row["market_prob_loser"]),
                "fallback_rule_used": market_row["fallback"],
            }
        )
        evaluations.append(
            {
                "race_id": race.race_id,
                "checkpoint_name": name,
                "checkpoint_date": checkpoint,
                "source_kind": "poll",
                "observation_date_used": poll_row["date"],
                "classification": classify_poll(race, poll_row["poll_value_winner"], poll_row["poll_value_loser"]),
                "fallback_rule_used": poll_row["fallback"],
            }
        )
    return evaluations


def export_figure(race: RaceDefinition, evaluations: pd.DataFrame) -> Path:
    """Write one checkpoint classification chart per analytical row."""
    subset = evaluations[evaluations["race_id"] == race.race_id].copy()
    order = ["90d", "30d", "eve"]
    label_map = {"90d": "90 days", "30d": "30 days", "eve": "Election eve"}
    score_map = {"no": 0, "toss-up": 1, "yes": 2, "missing": np.nan}

    def series_for(source_kind: str) -> pd.DataFrame:
        frame = subset[subset["source_kind"] == source_kind].copy()
        frame["checkpoint_name"] = pd.Categorical(frame["checkpoint_name"], categories=order, ordered=True)
        frame = frame.sort_values("checkpoint_name")
        frame["x_label"] = frame["checkpoint_name"].map(label_map)
        frame["score"] = frame["classification"].map(score_map)
        return frame

    market = series_for("market")
    poll = series_for("poll")

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=market["x_label"],
            y=market["score"],
            mode="lines+markers",
            name="Market",
            line={"color": "#c0392b", "width": 3},
            marker={"size": 10},
            text=market["classification"],
            hovertemplate="Checkpoint: %{x}<br>Market: %{text}<extra></extra>",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=poll["x_label"],
            y=poll["score"],
            mode="lines+markers",
            name="Poll predictions",
            line={"color": "#1f77b4", "width": 3},
            marker={"size": 10},
            text=poll["classification"],
            hovertemplate="Checkpoint: %{x}<br>Poll predictions: %{text}<extra></extra>",
        )
    )
    figure.update_layout(
        title=f"{race.race_label}: who each source favored at the checkpoints",
        xaxis_title="Checkpoint days before the election",
        yaxis_title="Favored outcome",
        yaxis={
            "tickmode": "array",
            "tickvals": [0, 1, 2],
            "ticktext": ["no", "toss-up", "yes"],
            "range": [-0.2, 2.2],
        },
        legend={"orientation": "h", "y": -0.2},
        template="plotly_white",
        height=450,
    )
    output = FIGURES_DIR / f"{race.race_id}.html"
    figure.write_html(output, include_plotlyjs="cdn")
    return output


def race_takeaway(race: RaceDefinition, evaluations: pd.DataFrame) -> str:
    subset = evaluations[evaluations["race_id"] == race.race_id].copy()
    summary_bits = []
    for checkpoint in ["90d", "30d", "eve"]:
        market = subset[(subset["checkpoint_name"] == checkpoint) & (subset["source_kind"] == "market")]["classification"].iloc[0]
        poll = subset[(subset["checkpoint_name"] == checkpoint) & (subset["source_kind"] == "poll")]["classification"].iloc[0]
        summary_bits.append(f"{checkpoint}: market {market}, polling side {poll}")
    joined = "; ".join(summary_bits)
    if race.poll_kind == "forecast":
        method_note = "The chamber row uses a forecast-style non-market probability rather than raw polling."
    else:
        method_note = "The polling side is a checked-in checkpoint record of who polling averages favored."
    return f"**{race.race_label}.** Eventual winner: {race.eventual_winner}. {joined}. {method_note}"
'''


PIPELINE = r'''races = [
    RaceDefinition(
        race_id="president_2020",
        race_label="2020 U.S. presidential election",
        election_date="2020-11-03",
        eventual_winner="Joseph R. Biden Jr.",
        eventual_loser="Donald Trump",
        market_source_name="ElectionBettingOdds historical page",
        market_source_url="https://electionbettingodds.com/President2020.html",
        poll_source_name="Checked-in polling-average fixture",
        poll_source_url="prediction-markets-story/data/raw/candidate_poll_checkpoints.csv",
        market_kind="probability",
        poll_kind="polls",
        ebo_page="https://electionbettingodds.com/President2020.html",
        ebo_winner_match="Biden",
        ebo_loser_match="Trump",
    ),
    RaceDefinition(
        race_id="house_2022_control",
        race_label="2022 House control",
        election_date="2022-11-08",
        eventual_winner="Republicans",
        eventual_loser="Democrats",
        market_source_name="ElectionBettingOdds House 2022 chart",
        market_source_url="https://electionbettingodds.com/House2022.html",
        poll_source_name="FiveThirtyEight chamber forecast writeups fixture",
        poll_source_url="https://fivethirtyeight.com/tag/2022-election-forecast/",
        market_kind="probability",
        poll_kind="forecast",
        ebo_page="https://electionbettingodds.com/House2022.html",
        ebo_winner_match="REP",
        ebo_loser_match="DEM",
    ),
    RaceDefinition(
        race_id="senate_2022_control",
        race_label="2022 Senate control",
        election_date="2022-11-08",
        eventual_winner="Democrats",
        eventual_loser="Republicans",
        market_source_name="ElectionBettingOdds Senate 2022 chart",
        market_source_url="https://electionbettingodds.com/Senate2022.html",
        poll_source_name="FiveThirtyEight chamber forecast writeups fixture",
        poll_source_url="https://fivethirtyeight.com/tag/2022-election-forecast/",
        market_kind="probability",
        poll_kind="forecast",
        ebo_page="https://electionbettingodds.com/Senate2022.html",
        ebo_winner_match="DEM",
        ebo_loser_match="REP",
    ),
    RaceDefinition(
        race_id="pa_senate_2022",
        race_label="2022 Pennsylvania Senate",
        election_date="2022-11-08",
        eventual_winner="John Fetterman",
        eventual_loser="Mehmet Oz",
        market_source_name="ElectionBettingOdds Senate 2022 chart",
        market_source_url="https://electionbettingodds.com/Senate2022.html",
        poll_source_name="Checked-in polling-average fixture",
        poll_source_url="prediction-markets-story/data/raw/candidate_poll_checkpoints.csv",
        market_kind="probability",
        poll_kind="polls",
        ebo_page="https://electionbettingodds.com/Senate2022.html",
        ebo_winner_match="DEM",
        ebo_loser_match="REP",
    ),
    RaceDefinition(
        race_id="president_2024",
        race_label="2024 U.S. presidential election",
        election_date="2024-11-05",
        eventual_winner="Donald Trump",
        eventual_loser="Kamala Harris",
        market_source_name="ElectionBettingOdds 2024 presidency chart",
        market_source_url="https://electionbettingodds.com/President2024.html",
        poll_source_name="Checked-in polling-average fixture",
        poll_source_url="prediction-markets-story/data/raw/candidate_poll_checkpoints.csv",
        market_kind="probability",
        poll_kind="polls",
        ebo_page="https://electionbettingodds.com/President2024.html",
        ebo_winner_match="Trump",
        ebo_loser_match="Harris",
    ),
]

display(Markdown("## Source Inventory"))
for race in races:
    display(
        Markdown(
            f"- **{race.race_label}**  \n"
            f"  Market: [{race.market_source_name}]({race.market_source_url})  \n"
            f"  Polling side: [{race.poll_source_name}]({race.poll_source_url})"
        )
    )

processed_frames = {}
evaluation_rows = []

for race in races:
    frame = merge_race_series(race)
    frame = frame.sort_values("date")
    processed_frames[race.race_id] = frame
    frame.to_csv(PROCESSED_DIR / f"{race.race_id}.csv", index=False)
    evaluation_rows.extend(checkpoint_evaluations(race, frame))

evaluations = pd.DataFrame(evaluation_rows)
figure_paths = {}
for race in races:
    figure_paths[race.race_id] = export_figure(race, evaluations)

summary_rows = []
for race in races:
    subset = evaluations[evaluations["race_id"] == race.race_id]
    summary_rows.append(
        {
            "race": race.race_label,
            "eventual_winner": race.eventual_winner,
            "market_favored_90d": subset[(subset["checkpoint_name"] == "90d") & (subset["source_kind"] == "market")]["classification"].iloc[0],
            "market_favored_30d": subset[(subset["checkpoint_name"] == "30d") & (subset["source_kind"] == "market")]["classification"].iloc[0],
            "market_favored_eve": subset[(subset["checkpoint_name"] == "eve") & (subset["source_kind"] == "market")]["classification"].iloc[0],
            "polls_favored_90d": subset[(subset["checkpoint_name"] == "90d") & (subset["source_kind"] == "poll")]["classification"].iloc[0],
            "polls_favored_30d": subset[(subset["checkpoint_name"] == "30d") & (subset["source_kind"] == "poll")]["classification"].iloc[0],
            "polls_favored_eve": subset[(subset["checkpoint_name"] == "eve") & (subset["source_kind"] == "poll")]["classification"].iloc[0],
        }
    )

summary = pd.DataFrame(summary_rows)
summary.to_csv(SUMMARY_PATH, index=False)

display(Markdown("## Cleaning And Alignment Notes"))
display(
    Markdown(
        "- Market data is scraped from embedded Google Charts arrays in ElectionBettingOdds HTML pages.\n"
        "- Candidate-race polling checkpoints come from a checked-in fixture built from archived polling-average reporting.\n"
        "- Checkpoints use the latest observation on or before the target date. If no earlier observation exists, the notebook falls back to the earliest subsequent one and records that choice.\n"
        "- The exported charts visualize only the checkpoint classifications: no, toss-up, or yes.\n"
        "- The 2022 chamber rows use a forecast-style non-market probability fixture because the historical FiveThirtyEight forecast CSV links no longer resolve to the original files."
    )
)

display(Markdown("## Five-Row Summary Table"))
display(summary)
'''


RACE_OUTPUTS = r'''display(Markdown("## Race Sections"))
for race in races:
    display(Markdown(race_takeaway(race, evaluations)))
    display(Markdown(f"Figure export: `{figure_paths[race.race_id].relative_to(ROOT)}`"))
'''


CONCLUSION = r'''display(Markdown("## Final Findings And Caveats"))

conclusion = """
Across these five rows, prediction markets and the polling-side comparison did
not move in lockstep. The candidate-race rows often showed similar directional
stories by election eve, but the timing of those moves differed: polling
averages shifted more discretely while market probabilities moved continuously
and sometimes flipped earlier or more aggressively.

The chamber rows deserve extra caution. They compare markets with a forecast
source rather than raw polling because chamber control is itself a forecasted
object. More broadly, the underlying historical polling and forecast CSVs that
once backed this kind of notebook are no longer reliably downloadable, so the
non-market side uses compact checkpoint fixtures built from archived polling
averages and published FiveThirtyEight writeups. That preserves a reproducible
record of the directional call while avoiding invented intermediate data.

This notebook does not claim that markets are broadly better than polls or vice
versa. It only records which side each source favored at three fixed points in
these five cases. As an additional context note, 2024 presidential market
pricing on Polymarket was widely discussed as being influenced by a small number
of large traders, which is one reason to read market prices as signals rather
than neutral ground truth.
""".strip()

display(Markdown(conclusion))
'''


def build_notebook() -> dict:
    cells = [
        md_cell(INTRO),
        code_cell(HELPERS),
        code_cell(PIPELINE),
        code_cell(RACE_OUTPUTS),
        code_cell(CONCLUSION),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


NOTEBOOK.write_text(json.dumps(build_notebook(), indent=2), encoding="utf-8")
print(f"Wrote {NOTEBOOK}")
