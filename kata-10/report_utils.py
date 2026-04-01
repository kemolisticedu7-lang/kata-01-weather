def classify_delay_risk(score: float) -> str:
    """Classify a delay risk score into a category."""
    low_threshold = 0.3
    high_threshold = 0.7

    if score < low_threshold:
        return "low"
    elif score < high_threshold:
        return "medium"
    return "high"