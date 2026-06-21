from src.utils import filter_airplanes, get_aeroplanes_by_altitude, sort_airplanes, print_aeroplanes

def test_filter_airplanes(sample_planes):
    assert len(filter_airplanes(sample_planes, ['USA', 'RU'])) == 3
    assert len(filter_airplanes(sample_planes, ['RU'])) == 1

def test_get_aero(edge_case_planes):
    assert len(get_aeroplanes_by_altitude(edge_case_planes, "2500-5500")) == 1
    assert len(get_aeroplanes_by_altitude(edge_case_planes, "2500-25500")) == 2

def test_sort_airplanes(planes):
    sorted_planes = sort_airplanes(planes)
    expected_icao = ["ab04", "ab02", "ab01", "ab03", "ab05"]
    actual_icao = [p.icao24 for p in sorted_planes]
    assert actual_icao == expected_icao


def test_print_aeroplanes_output(planes, capsys):
    print_aeroplanes(planes)
    captured = capsys.readouterr()
    out = captured.out
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    assert len(lines) == 5
    assert lines[
               0] == "1.Идентификатор: ab01 | Позывной: FLT-A | Страна регистрации: USA | Горизонтальная скорость (м/с)500.0 | Высота: 10000.0"
    assert lines[
               -1] == "5.Идентификатор: ab05 | Позывной: FLT-E | Страна регистрации: FR | Горизонтальная скорость (м/с)450.0 | Высота: 0.0"


def test_print_aeroplanes_empty(empty_planes, capsys):
    print_aeroplanes(empty_planes)
    captured = capsys.readouterr()

    assert captured.out.strip() == "Самолеты не найдены"