from abc import ABC, abstractmethod
import json
import os
from pathlib import Path

from aircraft_attrib import Airplane


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
        base_dir = Path("data")
        base_dir.mkdir(parents=True, exist_ok=True)
        self.filename = str(base_dir / filename)
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

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
        with open(self.filename, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data

    def _write_file(self, data):
        with open(self.filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

# if __name__ == '__main__':
#     filename = "data/test_airplanes.json"
#     if os.path.exists(filename):
#         os.remove(filename)  # удаляем старый файл, чтобы начать с чистого листа
#
#     saver = JSONSaver("test_airplanes.json")
#
#     # Создаём пару самолётов
#     p1 = Airplane('39de53', 'TVF10HW', 'France', 126.42, 1242.06)
#     p2 = Airplane('4bc8a7', 'TCREG', 'Turkey', 214.3, 13655.04)
#
#     # Добавляем
#     saver.add_info(p1)
#     saver.add_info(p2)
#
#     # Получаем по критерию
#     france_planes = saver.get_info({"country": "France"})
#     print(france_planes)  # [{'icao24': '39de53', ...}]
#
#     # Удаляем по критерию (например, все из Турции)
#     saver.deleter_info({"country": "Turkey"})
#
#     # Проверяем, что осталось
#     all_planes = saver.get_info({})
#     print(all_planes)  # должен остаться только p1