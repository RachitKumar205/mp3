"""Shared paths, issue names and table helpers for the MP3 pipeline."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_XLSX = ROOT / "data" / "raw" / "ICTIndiv.xlsx"
CLEAN_CSV = ROOT / "data" / "processed" / "ict_clean.csv"
FIG_DIR = ROOT / "output" / "figures"
TAB_DIR = ROOT / "output" / "tables"
VALUES_JSON = ROOT / "output" / "values.json"

# The nine issues, in the order of the IMF field description.
ISSUES = ["FC", "JI", "SE", "WS", "WO", "WH", "WE", "TI", "TA"]
NAMES = {
    "FC": "Friendship circles", "JI": "Job insecurity", "SE": "Self-efficacy",
    "WS": "Work satisfaction", "WO": "Work overload", "WH": "Work-home conflict",
    "WE": "Work exhaustion", "TI": "Turnover intention", "TA": "Turnaway intention",
}
# Column names in the cleaned data: factor scores as given, sum scores standardised.
FS = [f"{i}_FS" for i in ISSUES]
S = [f"{i}_S" for i in ISSUES]
SCORES = {"FS": FS, "S": S}

SEED = 2026
K_RANGE = range(2, 11)


def save_values(new: dict) -> None:
    """Merge key numbers into values.json."""
    VALUES_JSON.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(VALUES_JSON.read_text()) if VALUES_JSON.exists() else {}
    data.update(new)
    VALUES_JSON.write_text(json.dumps(data, indent=2, sort_keys=True))


def write_table(name: str, df, floatfmt=".3f", index=False, numparse=True) -> None:
    """Write a table as Markdown and CSV. numparse=False keeps pre-formatted strings."""
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    md = df.to_markdown(index=index, floatfmt=floatfmt, disable_numparse=not numparse)
    (TAB_DIR / f"{name}.md").write_text(md + "\n")
    df.to_csv(TAB_DIR / f"{name}.csv", index=index)
