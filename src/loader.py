import pandas as pd
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "pitchbook_export.csv"


def load_pipeline(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load and clean the Pitchbook export CSV."""
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    # Parse dates
    df["Last Funding Date"] = pd.to_datetime(df["Last Funding Date"], errors="coerce")

    # Numeric coercion
    for col in ["Total Raised ($M)", "Last Funding Amount ($M)", "Number of Rounds",
                "Employee Count", "Number of Founders", "Founded Year", "Prior Exits"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Normalize company name for lookup
    df["_name_lower"] = df["Company Name"].str.lower().str.strip()

    return df


def find_company(df: pd.DataFrame, name: str) -> pd.Series:
    """Return a single company row by name (case-insensitive partial match)."""
    name_lower = name.lower().strip()
    matches = df[df["_name_lower"].str.contains(name_lower, na=False)]

    if matches.empty:
        raise ValueError(
            f"No company found matching '{name}'.\n"
            f"Available companies:\n  " +
            "\n  ".join(df["Company Name"].tolist())
        )
    if len(matches) > 1:
        names = matches["Company Name"].tolist()
        raise ValueError(
            f"Multiple matches for '{name}': {names}. Be more specific."
        )
    return matches.iloc[0]
