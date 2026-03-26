"""
Scoring model for early-stage deal screening.

Each criterion returns a score from 0-10.
Final score is a weighted sum scaled to 0-100.
"""

import pandas as pd
from datetime import datetime
from config import (
    SCORING_WEIGHTS, STAGE_SCORES, MARKET_SCORES,
    REVENUE_MIDPOINTS, SCORE_BANDS
)


def score_capital_efficiency(row: pd.Series) -> tuple[float, str]:
    """
    Revenue / Total Raised. Higher ratio = leaner, more efficient business.
    Benchmarks:
      > 0.5x  -> excellent for stage
      0.2-0.5 -> good
      0.05-0.2 -> typical early
      < 0.05  -> heavy spend, low rev
    """
    revenue = REVENUE_MIDPOINTS.get(row["Revenue Range"], 0)
    raised = row["Total Raised ($M)"]

    if raised == 0 or revenue == 0:
        return 3.0, "Insufficient revenue data"

    ratio = revenue / raised

    if ratio >= 0.5:
        score, note = 10.0, f"{ratio:.2f}x rev/raised -- exceptional efficiency"
    elif ratio >= 0.2:
        score, note = 7.5, f"{ratio:.2f}x rev/raised -- solid efficiency"
    elif ratio >= 0.05:
        score, note = 5.0, f"{ratio:.2f}x rev/raised -- typical for stage"
    else:
        score, note = 2.5, f"{ratio:.2f}x rev/raised -- high burn relative to revenue"

    return score, note


def score_stage_alignment(row: pd.Series) -> tuple[float, str]:
    """Score based on preferred funding stage (Seed and Series A are target zone)."""
    stage = row["Last Funding Type"]
    score = STAGE_SCORES.get(stage, STAGE_SCORES["Unknown"])
    note = f"{stage} -- {'in target zone' if score >= 8 else 'outside target zone'}"
    return float(score), note


def score_market_category(row: pd.Series) -> tuple[float, str]:
    """Score based on industry category alignment with fund thesis."""
    industry = row["Primary Industry"]
    score = MARKET_SCORES.get(industry, MARKET_SCORES["Default"])
    note = f"{industry}"
    return float(score), note


def score_growth_momentum(row: pd.Series) -> tuple[float, str]:
    """
    Combines recency of last funding and round progression.
    Recent raise in a later round = strong momentum signal.
    """
    last_date = row["Last Funding Date"]
    num_rounds = row["Number of Rounds"]

    if pd.isna(last_date):
        return 3.0, "No funding date available"

    months_since = (datetime.now() - last_date).days / 30

    # Recency score (0-5): fresher = better
    if months_since <= 3:
        recency = 5.0
    elif months_since <= 9:
        recency = 4.0
    elif months_since <= 18:
        recency = 3.0
    elif months_since <= 30:
        recency = 2.0
    else:
        recency = 1.0

    # Progression score (0-5): more rounds = more validated
    progression = min(num_rounds * 1.5, 5.0)

    score = recency + progression
    note = (
        f"Last raised {months_since:.0f} months ago · "
        f"{int(num_rounds)} round{'s' if num_rounds != 1 else ''}"
    )
    return score, note


def score_team_strength(row: pd.Series) -> tuple[float, str]:
    """
    Proxy for team quality using founder count, prior exits, and employee
    count relative to capital raised.
    """
    founders = row["Number of Founders"]
    exits = row["Prior Exits"]
    employees = row["Employee Count"]
    raised = row["Total Raised ($M)"]

    # Prior exits are a strong signal
    exit_score = min(exits * 3.5, 7.0)

    # Founder count: 2-3 is sweet spot
    if founders == 2 or founders == 3:
        founder_score = 2.0
    elif founders == 1:
        founder_score = 1.0
    else:
        founder_score = 1.5

    # Team size efficiency: employees per $1M raised
    if raised > 0:
        ratio = employees / raised
        if 3 <= ratio <= 8:
            size_score = 1.0   # healthy lean team
        elif ratio > 8:
            size_score = 0.5   # potentially over-hired
        else:
            size_score = 0.5   # very small team relative to capital
    else:
        size_score = 0.5

    score = exit_score + founder_score + size_score
    score = min(score, 10.0)

    note = (
        f"{int(founders)} founder{'s' if founders != 1 else ''} · "
        f"{int(exits)} prior exit{'s' if exits != 1 else ''} · "
        f"{int(employees)} employees"
    )
    return score, note


def score_company(row: pd.Series) -> dict:
    """Run all scoring criteria and return a full scorecard."""
    scores = {}
    notes = {}

    scores["capital_efficiency"], notes["capital_efficiency"] = score_capital_efficiency(row)
    scores["stage_alignment"],    notes["stage_alignment"]    = score_stage_alignment(row)
    scores["market_category"],    notes["market_category"]    = score_market_category(row)
    scores["growth_momentum"],    notes["growth_momentum"]    = score_growth_momentum(row)
    scores["team_strength"],      notes["team_strength"]      = score_team_strength(row)

    # Weighted total (each criterion is 0-10; final score is 0-100)
    total = sum(
        scores[k] * SCORING_WEIGHTS[k] * 10
        for k in scores
    )

    # Determine recommendation band
    recommendation = "Pass"
    for threshold, label in SCORE_BANDS:
        if total >= threshold:
            recommendation = label
            break

    return {
        "total": round(total, 1),
        "recommendation": recommendation,
        "scores": {k: round(v, 1) for k, v in scores.items()},
        "notes": notes,
        "weights": SCORING_WEIGHTS,
    }
