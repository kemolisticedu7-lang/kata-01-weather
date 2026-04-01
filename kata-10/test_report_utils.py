from report_utils import classify_delay_risk


def test_classify_low_risk():
    assert classify_delay_risk(0.2) == "low"