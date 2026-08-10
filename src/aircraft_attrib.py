class Airplane:
    """Класс для работы с информацией о самолёте"""

    __slots__ = ("icao24", "callsign", "country", "velocity", "geo_altitude")

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
    def cast_to_object_list(cls, airplanes: dict) -> list:
        states = airplanes.get("states", [])
        planes = []
        for row in states:
            plane = cls.from_api_row(row)
            if plane:
                planes.append(plane)
        return planes

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
        if len(row) < 14:
            return None
        icao24 = str(row[0]).strip() if row[0] else None
        callsign = str(row[1]).strip() if row[1] else None
        country = str(row[2]).strip() if row[2] else None
        try:
            velocity = float(row[9]) if row[9] is not None else 0.0
            geo_altitude = float(row[13]) if row[13] is not None else 0.0
        except (ValueError, TypeError):
            return None

        if velocity < 0 or geo_altitude < 0:
            return None

        return cls(icao24=icao24, callsign=callsign, country=country, velocity=velocity, geo_altitude=geo_altitude)

    def to_dict(self):
        """Вспомогательный метод для сериализации (нужен для JSON)"""
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "country": self.country,
            "velocity": self.velocity,
            "geo_altitude": self.geo_altitude,
        }
