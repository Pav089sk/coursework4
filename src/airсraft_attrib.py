
class Airplane:
    """Класс для работы с информацией о самолёте"""
    __slots__ = ('icao24', 'callsign', 'country', 'velocity','geo_altitude')

    def __init__(self, icao24, callsign, country, velocity, geo_altitude):
        self.icao24 = str(icao24).strip()
        self.callsign = str(callsign).strip()
        self.country = str(country).strip()
        # Валидация скорости
        if velocity is None:
            self.velocity = 0.0
        else:
            v = float(velocity)
            if v < 0:
                raise ValueError("Скорость не может быть отрицательной")
            self.velocity = v

        # Валидация высоты
        if geo_altitude is None:
            self.geo_altitude = 0.0
        else:
            altitude = float(geo_altitude)
            if altitude < 0:
                raise ValueError("Высота не может быть отрицательной")
            self.geo_altitude = altitude

    @classmethod
    def cast_to_object_list(cls, airplanes):
        airplanes_list =[]
        for airplane in airplanes:
            airplanes_list.append(Airplane.from_api_row(airplane))
        return airplanes_list


    def __le__(self, other):
        return self.velocity <= other.velocity
    def __ge__(self, other):
        return self.velocity >= other.velocity
    def __lt__(self, other):
        return self.velocity < other.velocity
    def __gt__(self, other):
        return self.velocity > other.velocity
    def is_higher_than(self, other):
        return self.geo_altitude > other.geo_altitude

    @classmethod
    def from_api_row(cls, row):
        def safe_get(idx):
            return row[idx] if len(row) > idx else None

        return cls(
            icao24=safe_get(0),
            callsign=safe_get(1),
            country=safe_get(2),
            velocity=safe_get(9),
            geo_altitude=safe_get(11)
        )

