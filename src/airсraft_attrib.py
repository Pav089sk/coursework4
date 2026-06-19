
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
        return cls(
            icao24=row[0],
            callsign=row[1],
            country=row[2],
            velocity=row[9],
            geo_altitude=row[11]
        )

