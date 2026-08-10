import pytest

from src.aircraft_attrib import Airplane


@pytest.fixture
def good_plane():
    plane = Airplane(icao24="ab12", callsign="FLIGHT-A", country="USA", velocity=500, geo_altitude=10000)
    return plane


@pytest.fixture
def airplane_none_values():
    plane = Airplane(icao24="ab12", callsign="FLIGHT-A", country="USA", velocity=None, geo_altitude=None)
    return plane


@pytest.fixture
def airplane_negative_velocity():
    plane = Airplane(icao24="ab12", callsign="FLIGHT-A", country="USA", velocity=-100, geo_altitude=200)
    return plane


@pytest.fixture
def sample_planes():
    return [
        Airplane(icao24="ab01", callsign="FLT-A", country="USA", velocity=500, geo_altitude=10000),
        Airplane(icao24="ab02", callsign="FLT-B", country="RU", velocity=600, geo_altitude=11000),
        Airplane(icao24="ab03", callsign="FLT-C", country="DE", velocity=550, geo_altitude=9000),
        Airplane(icao24="ab04", callsign="FLT-D", country="USA", velocity=700, geo_altitude=12000),
        Airplane(icao24="ab05", callsign="FLT-E", country="FR", velocity=450, geo_altitude=None),
    ]


@pytest.fixture
def planes():
    return [
        Airplane(icao24="ab01", callsign="FLT-A", country="USA", velocity=500, geo_altitude=10000),
        Airplane(icao24="ab02", callsign="FLT-B", country="RU", velocity=600, geo_altitude=11000),
        Airplane(icao24="ab03", callsign="FLT-C", country="DE", velocity=550, geo_altitude=9000),
        Airplane(icao24="ab04", callsign="FLT-D", country="USA", velocity=700, geo_altitude=12000),
        Airplane(icao24="ab05", callsign="FLT-E", country="FR", velocity=450, geo_altitude=0.0),
    ]


@pytest.fixture
def edge_case_planes():
    return [
        Airplane(icao24="x1", callsign="E1", country="XX", velocity=100, geo_altitude=0),
        Airplane(icao24="x2", callsign="E2", country="XX", velocity=200, geo_altitude=5000),
        Airplane(icao24="x3", callsign="E3", country="XX", velocity=300, geo_altitude=20000),
        Airplane(icao24="x4", callsign="E4", country="XX", velocity=400, geo_altitude=None),
    ]


@pytest.fixture
def empty_planes():
    return []
