

def filter_airplanes(planes: list, countries: list):
    """Фильтрация по странам"""
    if not countries:
        return planes
    target_countries = [c.strip().lower() for c in countries if c.strip()]
    return [p for p in planes if p.country.lower() in target_countries]


def get_aeroplanes_by_altitude(planes: list, altitude: str):
    """Функция выборки самолетов по диапазону высот"""
    try:
        alt = altitude.split("-")
        alt_min = float(alt[0].strip())
        alt_max = float(alt[1].strip())
        return [i for i in planes if i.geo_altitude is not None and alt_min <= i.geo_altitude <= alt_max]
    except (ValueError, IndexError):
        print("Введено некорректное значение высоты")
        return []


def sort_airplanes(planes: list):
    """Сортировка по высоте"""
    return sorted(planes, key=lambda i: i.geo_altitude if i.geo_altitude is not None else 0, reverse=True)


def get_top_aeroplanes(planes: list, top_n: int):
    """Возврат первые n самолетов"""
    return planes[:top_n]


def print_aeroplanes(planes: list):
    """Вывод списка самолетов"""
    if not planes:
        print("Самолеты не найдены")
        return
    for i, a in enumerate(planes, 1):
        print(
            f"{i}.Идентификатор: {a.icao24} | Позывной: {a.callsign} | Страна регистрации: {a.country} | Горизонтальная скорость (м/с){a.velocity} | Высота: {a.geo_altitude}"
        )
