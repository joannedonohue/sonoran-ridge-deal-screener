# Private Fund — Deal Screener

> **Disclaimer:** This is an anonymized sample project. The fund name, scoring weights, thesis parameters, and company data are illustrative only and do not represent a real investment model or fund.

A Python-based investment research tool that takes a company name from a Pitchbook export, scores it against the fund's thesis criteria, and generates a one-page deal brief in seconds.

Built to replace manual first-pass screening — what used to take a few hours of pulling founder backgrounds, funding history, and market comps across multiple tabs now runs in under 10 seconds per company.

---

## What it does

1. Loads a Pitchbook export CSV (company profile, funding history, team, revenue range)
2. Runs each company through a five-criterion weighted scoring model
3. Outputs a formatted one-page brief with a recommendation band

---

## Scoring model

| Criterion | Weight | What it measures |
|---|---|---|
| Capital Efficiency | 25% | Revenue / total raised — how lean is the business? |
| Market Category | 20% | Sector alignment with fund thesis |
| Growth Momentum | 20% | Recency and progression of funding rounds |
| Team Strength | 20% | Prior exits, founder count, headcount relative to capital |
| Stage Alignment | 15% | Preferred stage (Seed / Series A target zone) |

Score bands:
- **80–100** → Priority — move to IC
- **65–79** → Dig Deeper — schedule founder call
- **45–64** → Monitor — revisit in 90 days
- **0–44** → Pass

Weights and scoring parameters are fully configurable in `config.py`.

---

## Usage

```bash
# Screen a single company
python screener.py "Luminary Health"

# Partial name match works
python screener.py "luminary"

# Save brief to sample_output/
python screener.py "Luminary Health" --save

# Score all companies and print ranked results
python screener.py --batch

# List all companies in the pipeline
python screener.py --list
```

---

## Example output

```
══════════════════════════════════════════════════════════════
  PRIVATE FUND  |  DEAL BRIEF
  Generated: Mar 25, 2026
══════════════════════════════════════════════════════════════

  LUMINARY HEALTH
  luminaryhealth.com

  AI-powered benefits navigation platform that helps employees
  find and use mental health coverage

  COMPANY SNAPSHOT
  ──────────────────────────────────────────────────────────
  Industry           Health Tech
  HQ                 Austin, TX
  Founded            2021
  Employees          48
  Revenue Range      $1M-$5M
  Total Raised       $12.4M across 2 round(s)
  Last Round         Series A — $10.0M (Mar 2024)
  Lead Investors     Andreessen Horowitz, Founders Fund
  Founders           Sarah Chen, Marcus Webb
  Prior Exits        1

  SCORECARD
  ──────────────────────────────────────────────────────────
  Capital Efficiency     [███████████████░░░░░]   7.5/10
  Stage Alignment        [██████████████████░░]   9.0/10
  Market Category        [██████████████████░░]   9.0/10
  Growth Momentum        [██████████░░░░░░░░░░]   5.0/10
  Team Strength          [█████████████░░░░░░░]   6.5/10

  OVERALL SCORE:  73.2/100
  RECOMMENDATION: Dig Deeper — schedule founder call
══════════════════════════════════════════════════════════════
```

---

## Setup

```bash
pip install -r requirements.txt
python screener.py --batch
```

No API keys required. Designed to run against any Pitchbook CSV export — swap in your own data file at `data/pitchbook_export.csv`.

---

## Project structure

```
sonoran-ridge-deal-screener/
├── screener.py                  # CLI entry point
├── config.py                    # Scoring weights and parameters
├── requirements.txt
├── data/
│   └── pitchbook_export.csv     # Sample Pitchbook export (25 companies)
├── src/
│   ├── loader.py                # Data loading and company lookup
│   ├── scorer.py                # Five-criterion scoring model
│   └── brief.py                 # Brief formatting and file export
└── sample_output/
    └── brief_luminary_health.txt
```

---

## Extending this

The scoring model is intentionally simple and transparent. To adapt it:

- **Change thesis weights** — edit `SCORING_WEIGHTS` in `config.py`
- **Add sectors** — extend `MARKET_SCORES` with your own category preferences
- **Plug in real data** — replace the CSV with a live Pitchbook API integration or a Crunchbase export
- **Add LLM narrative** — pipe the company description through an OpenAI call to generate a thesis-fit summary in the brief

---

## Data note

The CSV in `data/` uses synthetic company data modeled after real Pitchbook export formats. Fields, funding structures, and investor names are illustrative and not representative of actual companies.


