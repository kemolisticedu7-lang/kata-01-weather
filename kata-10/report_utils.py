def classify_delay_risk(score: float) -> str:
    """Classify a delay risk score into a category."""
    if score < 0.3:
        return "low"
    return "medium"