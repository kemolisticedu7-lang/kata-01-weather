def classify_delay_risk(score: float) -> str:
    """Classify a delay risk score into a category."""
    thresholds = {
        "low": 0.3,
        "high": 0.7
    }

    if score < thresholds["low"]:
        return "low"
    if score < thresholds["high"]:
        return "medium"
    return "high"