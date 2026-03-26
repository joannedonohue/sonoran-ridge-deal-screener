#!/usr/bin/env python3
"""
Sonoran Ridge Capital — Deal Screener
======================================
Takes a company name from the Pitchbook export, scores it against
the fund's investment criteria, and prints a one-page brief.

Usage:
    python screener.py "Luminary Health"
    python screener.py "luminary"             # partial match works
    python screener.py --list                 # show all companies
    python screener.py "Luminary" --save      # also saves brief to file
    python screener.py --batch                # score all companies, ranked
"""

import sys
import argparse
from pathlib import Path

# Add project root to path so src/ imports work
sys.path.insert(0, str(Path(__file__).parent))

from src.loader import load_pipeline, find_company
from src.scorer import score_company
from src.brief  import generate_brief, print_brief, save_brief


def run_single(name: str, save: bool = False) -> None:
    df  = load_pipeline()
    row = find_company(df, name)
    scorecard = score_company(row)
    brief = generate_brief(row, scorecard)
    print_brief(brief)
    if save:
        path = save_brief(brief, row["Company Name"])
        print(f"  Brief saved to: {path}\n")


def run_batch() -> None:
    """Score all companies and print a ranked summary table."""
    df = load_pipeline()
    results = []
    for _, row in df.iterrows():
        sc = score_company(row)
        results.append({
            "Company":        row["Company Name"],
            "Industry":       row["Primary Industry"],
            "Stage":          row["Last Funding Type"],
            "Score":          sc["total"],
            "Recommendation": sc["recommendation"],
        })

    results.sort(key=lambda x: x["Score"], reverse=True)

    print("\n" + "═" * 90)
    print("  SONORAN RIDGE CAPITAL  |  BATCH SCREEN RESULTS")
    print("═" * 90)
    print(f"  {'Company':<30} {'Industry':<25} {'Stage':<12} {'Score':>6}  Recommendation")
    print("─" * 90)
    for r in results:
        print(
            f"  {r['Company']:<30} {r['Industry']:<25} {r['Stage']:<12} "
            f"{r['Score']:>5.1f}  {r['Recommendation']}"
        )
    print("═" * 90)
    print(f"  {len(results)} companies screened\n")


def list_companies() -> None:
    df = load_pipeline()
    print("\nCompanies in pipeline:\n")
    for name in df["Company Name"].tolist():
        print(f"  • {name}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Sonoran Ridge Capital deal screener"
    )
    parser.add_argument(
        "company", nargs="?",
        help="Company name to screen (partial match OK)"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all companies in the pipeline"
    )
    parser.add_argument(
        "--batch", action="store_true",
        help="Score all companies and print ranked results"
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Save the brief to sample_output/"
    )
    args = parser.parse_args()

    if args.list:
        list_companies()
    elif args.batch:
        run_batch()
    elif args.company:
        run_single(args.company, save=args.save)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
