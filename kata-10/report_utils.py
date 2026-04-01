def classify_delay_risk(score: float) -> str:
    """Classify a delay risk score into a category."""
    low_threshold = 0.3

    if score < low_threshold:
        return "low"
    return "medium"