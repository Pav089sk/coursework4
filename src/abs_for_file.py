from abc import ABC, abstractmethod
import json
import os

from airсraft_attrib import Airplane


class AddFile(ABC):
    """Абстрактный класс для записи данных в файл"""

    @abstractmethod
    def add_info(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_info(self, *args, **kwargs):
        pass

    @abstractmethod
    def deleter_info(self, *args, **kwargs):
        pass

class JSONSaver(AddFile):
    """Класс для записи данных в JSON файл"""

    def __init__(self, filename = "airplanes.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def add_info(self, plane: Airplane):
        """Добавление самолета в файл JSON"""
        plane_dict = {"icao24": plane.icao24,
                      "callsign": plane.callsign,
                      "country": plane.country,
                      "velocity": plane.velocity,
                      "geo_altitude": plane.geo_altitude
                      }
        data = self._read_file()
        data.append(plane_dict)
        self._write_file(data)

    def get_info(self, criteria: dict):
        data = self._read_file()
        result = []
        for item in data:
            if all(item.get(k) == criteria[k] for k in criteria):
                result.append(item)
        return result


    def deleter_info(self, criteria: dict):
        data = self._read_file()
        result = []
        for item in data:
            if not all(item.get(k) == criteria[k] for k in criteria):
                result.append(item)
        self._write_file(result)

    def _read_file(self):
        with open(self.filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
        return data

    def _write_file(self, data):
        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

