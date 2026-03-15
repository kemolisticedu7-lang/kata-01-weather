import sys
from pathlib import Path
from unittest.mock import Mock, patch
import requests

sys.path.append(str(Path("kata-03").resolve()))

from api_client import request_with_retry, fetch_all_observations


@patch("api_client.requests.get")
def test_request_with_retry_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"observations": [{"value": "1.2"}]}'
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"observations": [{"value": "1.2"}]}
    mock_get.return_value = mock_response

    result = request_with_retry({"series_id": "TEST"})
    assert "observations" in result

@patch("api_client.requests.get")
def test_request_with_retry_http_error(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 error")
    mock_get.return_value = mock_response

    result = request_with_retry({"series_id": "TEST"})
    assert result is None

@patch("api_client.time.sleep", return_value=None)
@patch("api_client.requests.get")
def test_request_with_retry_timeout(mock_get, mock_sleep):
    mock_get.side_effect = requests.Timeout("timeout")

    result = request_with_retry({"series_id": "TEST"}, retries=1, timeout=1)

    assert result is None
    assert mock_get.call_count == 1
    
@patch("api_client.time.sleep", return_value=None)
@patch("api_client.requests.get")
def test_request_with_retry_retry_then_success(mock_get, mock_sleep):
    timeout_error = requests.Timeout("timeout")

    success_response = Mock()
    success_response.status_code = 200
    success_response.text = '{"observations": [{"value": "2.5"}]}'
    success_response.raise_for_status.return_value = None
    success_response.json.return_value = {"observations": [{"value": "2.5"}]}

    mock_get.side_effect = [timeout_error, timeout_error, success_response]

    result = request_with_retry({"series_id": "TEST"}, retries=3, timeout=1)
    assert result == {"observations": [{"value": "2.5"}]}
    assert mock_get.call_count == 3


@patch("api_client.request_with_retry")
def test_fetch_all_observations_uses_mock(mock_retry):
    mock_retry.side_effect = [
        {
            "observations": [
                {"date": "2024-01-01", "value": "1.0"},
                {"date": "2024-01-02", "value": "2.0"},
            ]
        },
        {
            "observations": []
        },
    ]

    result = fetch_all_observations("TEST_SERIES", "FAKE_API_KEY", limit=2)

    assert len(result) == 2
    assert result[0]["value"] == "1.0"
    assert mock_retry.call_count == 2