from unittest.mock import Mock, patch

from src.abs_api import SearchAreaData


@patch("src.abs_api.requests.get")
def test_connector_returns_ok(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"test": "data"}
    mock_get.return_value = mock_response
    search = SearchAreaData()
    response = search.connector("test.url")
    assert response.status_code == 200
    assert response.json() == {"test": "data"}


@patch("src.abs_api.requests.get")
def test_get_data_success(mock_get):
    mock_nominatim = Mock()
    mock_nominatim.status_code = 200
    mock_nominatim.json.return_value = [
        {"boundingbox": ["45.0", "50.0", "-120.0", "-110.0"], "display_name": "Test Country"}
    ]
    mock_opensky = Mock()
    mock_opensky.status_code = 200
    mock_opensky.json.return_value = {
        "states": [["a1", "FLIGHT1", "USA", None, None, None, None, None, None, 500.0, None, None, None, 10000.0]],
        "time": 1234567890,
    }
    mock_get.side_effect = [mock_nominatim, mock_opensky]
    search = SearchAreaData()
    result = search.get_data("Test Country")
    assert result is not None
    assert "states" in result
    assert len(result["states"]) == 1
    assert search.airplanes is result
