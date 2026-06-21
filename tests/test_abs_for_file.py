import pytest
import json
from pathlib import Path
from src.aircraft_attrib import Airplane
from src.abs_for_file import JSONSaver


@pytest.fixture
def json_saver_local():
    test_dir = Path(__file__).parent
    tmp_file = test_dir / "test_airplanes.json"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    saver = JSONSaver(filename=str(tmp_file))
    yield saver

def test_add_one_plane(json_saver_local):
    plane = Airplane(
        icao24="ab12",
        callsign="FLIGHT-A",
        country="USA",
        velocity=500,
        geo_altitude=10000
    )
    json_saver_local.add_info(plane)
    all_data = json_saver_local.get_info({})
    assert len(all_data) == 1
    assert all_data[0]["icao24"] == "ab12"
    assert all_data[0]["velocity"] == 500.0
    assert all_data[0]["country"] == "USA"


def test_get_info_by_country(json_saver_local):
    p1 = Airplane("x1", "F1", "USA", 500, 10000)
    p2 = Airplane("x2", "F2", "RU", 600, 11000)
    json_saver_local.add_info(p1)
    json_saver_local.add_info(p2)
    only_ru = json_saver_local.get_info({"country": "RU"})
    assert len(only_ru) == 1
    assert only_ru[0]["callsign"] == "F2"


def test_deleter_info_removes_matching(json_saver_local):
    p1 = Airplane("x1", "F1", "USA", 500, 10000)
    p2 = Airplane("x2", "F2", "RU", 600, 11000)
    json_saver_local.add_info(p1)
    json_saver_local.add_info(p2)
    json_saver_local.deleter_info({"country": "USA"})
    remaining = json_saver_local.get_info({})
    assert len(remaining) == 1
    assert remaining[0]["callsign"] == "F2"