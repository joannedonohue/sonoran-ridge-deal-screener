# Scoring weights — must sum to 1.0
SCORING_WEIGHTS = {
    "capital_efficiency":  0.25,
    "stage_alignment":     0.15,
    "market_category":     0.20,
    "growth_momentum":     0.20,
    "team_strength":       0.20,
}

# Target stage preferences (higher = more preferred)
STAGE_SCORES = {
    "Pre-Seed": 4,
    "Seed":     10,
    "Series A": 9,
    "Series B": 6,
    "Series C": 3,
    "Series D+": 1,
    "Unknown":  2,
}

# Market category scores (based on current thesis interest)
MARKET_SCORES = {
    "AI/ML":                10,
    "Climate Tech":          9,
    "Health Tech":           9,
    "Fintech":               8,
    "B2B SaaS":              8,
    "Data Infrastructure":   8,
    "Commerce Infrastructure": 7,
    "Cybersecurity":         8,
    "Insurtech":             7,
    "Behavioral Health":     8,
    "Healthcare Services":   7,
    "Femtech":               7,
    "PropTech":              6,
    "Senior Care":           6,
    "Supply Chain":          6,
    "AgriTech":              5,
    "Robotics":              7,
    "Consumer Food":         5,
    "Creator Economy":       5,
    "EdTech/FoodTech":       4,
    "Default":               4,
}

# Revenue ranges mapped to estimated midpoints ($M)
REVENUE_MIDPOINTS = {
    "$0":             0,
    "<$1M":           0.5,
    "$100K-$250K":    0.175,
    "$250K-$500K":    0.375,
    "$500K-$1M":      0.75,
    "$1M-$5M":        3.0,
    "$5M-$10M":       7.5,
    "$10M-$25M":      17.5,
    "$25M-$50M":      37.5,
    "$50M+":          60.0,
    "Unknown":        0,
}

# Score band labels
SCORE_BANDS = [
    (80, "Priority — move to IC"),
    (65, "Dig Deeper — schedule founder call"),
    (45, "Monitor — revisit in 90 days"),
    (0,  "Pass"),
]
