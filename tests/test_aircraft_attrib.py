import pytest

from src.aircraft_attrib import Airplane


def test_for_plane(good_plane):
    assert good_plane.icao24 == "ab12"
    assert good_plane.callsign == "FLIGHT-A"
    assert good_plane.country == "USA"
    assert good_plane.velocity == 500
    assert good_plane.geo_altitude == 10000


def test_for_none_value(airplane_none_values):
    assert airplane_none_values.icao24 == "ab12"
    assert airplane_none_values.callsign == "FLIGHT-A"
    assert airplane_none_values.country == "USA"
    assert airplane_none_values.velocity == 0.0
    assert airplane_none_values.geo_altitude == 0.0


def test_for_negative_velocity():
    with pytest.raises(ValueError) as e:
        Airplane(icao24="ab12", callsign="FLIGHT-A", country="USA", velocity=-100, geo_altitude=200)
        assert "Скорость не может быть отрицательной" in e.value


def test_for_negative_geo_altitude():
    with pytest.raises(ValueError) as e:
        Airplane(icao24="ab12", callsign="FLIGHT-A", country="USA", velocity=100, geo_altitude=-200)
        assert "Высота не может быть отрицательной" in e.value


def test_from_api_row_too_short():
    row = [1, 2, 3]  # всего 3 элемента
    plane = Airplane.from_api_row(row)
    assert plane is None


def test_from_api_row_success():
    # Имитация строки от OpenSky: минимум 14 элементов
    row = [None] * 14
    row[0] = "  zz77  "  # icao24
    row[1] = "FLIGHT"  # callsign
    row[2] = "DE "  # country
    row[9] = 600  # velocity
    row[13] = 12000  # geo_altitude
    plane = Airplane.from_api_row(row)
    assert plane is not None
    assert plane.icao24 == "zz77"
    assert plane.velocity == 600.0
    assert plane.geo_altitude == 12000.0


def test_comparison_operators():
    p1 = Airplane("a", "F1", "RU", 500, 1000)
    p2 = Airplane("b", "F2", "US", 600, 2000)

    assert p1 < p2  # 500 < 600
    assert p2 > p1  # 600 > 500
    assert p1 <= p2  # 500 <= 600
    assert p2 >= p1  # 600 >= 500


def test_to_dict():
    plane = Airplane("zz1", "TEST", "RU", 800, 9000)
    d = plane.to_dict()
    assert d["icao24"] == "zz1"
    assert d["velocity"] == 800.0
    assert d["geo_altitude"] == 9000.0


def test_is_higher_than():
    low = Airplane("l", "L", "RU", 500, 5000)  # 5 км
    high = Airplane("h", "H", "US", 500, 10000)  # 10 км

    assert high.is_higher_than(low)  # высота 10 > 5 → True
    assert not low.is_higher_than(high)  # высота 5 > 10 → False
