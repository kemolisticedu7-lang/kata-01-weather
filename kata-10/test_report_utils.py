from report_utils import classify_delay_risk


def test_classify_low_risk():
    assert classify_delay_risk(0.2) == "low"


def test_classify_medium_risk():
    assert classify_delay_risk(0.5) == "medium"