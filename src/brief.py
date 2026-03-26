"""
Generates a formatted one-page deal brief for terminal output and text file export.
"""

from datetime import datetime
import pandas as pd


CRITERION_LABELS = {
    "capital_efficiency": "Capital Efficiency",
    "stage_alignment":    "Stage Alignment",
    "market_category":    "Market Category",
    "growth_momentum":    "Growth Momentum",
    "team_strength":      "Team Strength",
}

BAR_WIDTH = 20


def _bar(score: float, max_score: float = 10.0) -> str:
    """Render a simple ASCII progress bar."""
    filled = int((score / max_score) * BAR_WIDTH)
    return "[" + "█" * filled + "░" * (BAR_WIDTH - filled) + "]"


def _divider(char: str = "-", width: int = 62) -> str:
    return char * width


def generate_brief(row: pd.Series, scorecard: dict) -> str:
    """Return a formatted one-page brief as a string."""
    scores  = scorecard["scores"]
    notes   = scorecard["notes"]
    weights = scorecard["weights"]
    total   = scorecard["total"]
    rec     = scorecard["recommendation"]

    last_date = row["Last Funding Date"]
    date_str  = last_date.strftime("%b %Y") if pd.notna(last_date) else "Unknown"

    lines = []
    lines.append(_divider("="))
    lines.append(f"  SONORAN RIDGE CAPITAL  |  DEAL BRIEF")
    lines.append(f"  Generated: {datetime.now().strftime('%b %d, %Y')}")
    lines.append(_divider("="))

    lines.append(f"\n  {row['Company Name'].upper()}")
    lines.append(f"  {row['Website']}")
    lines.append(f"\n  {row['Description']}")

    lines.append(f"\n{_divider()}")
    lines.append("  COMPANY SNAPSHOT")
    lines.append(_divider())

    snapshot = [
        ("Industry",        row["Primary Industry"]),
        ("HQ",              f"{row['HQ City']}, {row['HQ State']}"),
        ("Founded",         int(row["Founded Year"])),
        ("Employees",       int(row["Employee Count"])),
        ("Revenue Range",   row["Revenue Range"]),
        ("Total Raised",    f"${row['Total Raised ($M)']}M across {int(row['Number of Rounds'])} round(s)"),
        ("Last Round",      f"{row['Last Funding Type']} -- ${row['Last Funding Amount ($M)']}M ({date_str})"),
        ("Lead Investors",  row["Lead Investors"]),
        ("Founders",        row["Founder Names"]),
        ("Prior Exits",     int(row["Prior Exits"])),
    ]
    for label, value in snapshot:
        lines.append(f"  {label:<18} {value}")

    lines.append(f"\n{_divider()}")
    lines.append("  SCORECARD")
    lines.append(_divider())

    for key, label in CRITERION_LABELS.items():
        s   = scores[key]
        w   = int(weights[key] * 100)
        bar = _bar(s)
        note = notes[key]
        lines.append(f"  {label:<22} {bar}  {s:>4}/10  (weight: {w}%)")
        lines.append(f"  {'':22}   {note}")
        lines.append("")

    lines.append(_divider())
    lines.append(f"  OVERALL SCORE:  {total}/100")
    lines.append(f"  RECOMMENDATION: {rec}")
    lines.append(_divider("="))
    lines.append("")

    return "\n".join(lines)


def print_brief(brief_text: str) -> None:
    print(brief_text)


def save_brief(brief_text: str, company_name: str, output_dir: str = "sample_output") -> str:
    """Save brief to a text file. Returns the file path."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    safe_name = company_name.lower().replace(" ", "_")
    path = os.path.join(output_dir, f"brief_{safe_name}.txt")
    with open(path, "w") as f:
        f.write(brief_text)
    return path
