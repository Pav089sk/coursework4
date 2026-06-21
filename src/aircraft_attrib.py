
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

    def __repr__(self):
        return f"{self.icao24} {self.callsign} ({self.country}) {self.velocity} {self.geo_altitude}"

    @classmethod
    def cast_to_object_list(cls, airplanes):
        airplanes_list = []
        data = airplanes.get('states', [])
        for airplane in data:
            if not isinstance(airplane, list) or len(airplane) < 8:
                continue
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
        return cls(
            icao24=row[0],
            callsign=row[1],
            country=row[2],
            velocity=row[9],
            geo_altitude=row[13]
        )

    def to_dict(self):
        """Вспомогательный метод для сериализации (нужен для JSON)"""
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "country": self.country,
            "velocity": self.velocity,
            "geo_altitude": self.geo_altitude
        }



if __name__ == '__main__':
    a = Airplane
    print(a.cast_to_object_list({'time': 1782035010, 'states': [['39de53', 'TVF10HW ', 'France', 1782035007, 1782035007, 28.2754, 36.3539, 1158.24, False, 126.42, 70.75, -2.93, None, 1242.06, '5547', False, 0], ['4bc8a7', 'TCREG   ', 'Turkey', 1782035009, 1782035009, 21.6585, 41.2055, 13106.4, False, 214.3, 300.75, 0.33, None, 13655.04, '5304', False, 0], ['4bc8cd', 'PGT387U ', 'Turkey', 1782034992, 1782034992, 29.2084, 40.85, 495.3, False, 79.61, 63.93, -3.58, None, 647.7, None, False, 0]]}))
    plane = Airplane('39de53', 'TVF10HW', 'France', 126.42, 1242.06)
    print(plane.to_dict())