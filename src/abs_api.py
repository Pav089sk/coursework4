from abc import ABC, abstractmethod

import requests


class WorkWithApi(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def connector(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass


class SearchAreaData(WorkWithApi):
    """Класс получения координат страны и данных о самолетах"""

    def __init__(self):
        self.__url_coord = "https://nominatim.openstreetmap.org/search"
        self.__url_airplanes = "https://opensky-network.org/api/states/all"
        self.airplanes = None

    def connector(self, url: str, headers=None, params=None):
        """Метод подключения к API"""
        return requests.get(url, headers=headers, params=params)

    def get_data(self, country: str):
        """Метод получения данных о самолётах по координатам"""
        headers_nominatim = {
            "User-Agent": "test-app/1.0",
        }
        params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }
        response = self.connector(self.__url_coord, headers=headers_nominatim, params=params_nominatim)
        if response.status_code == 200:
            data = response.json()
            if not data:
                return

            geo_coordinates = data[0].get("boundingbox")
            if geo_coordinates is None:
                return
            # Параметры для фильтрации самолетов по их географическим координатам.
            params = {
                "lamin": float(geo_coordinates[0]),
                "lamax": float(geo_coordinates[1]),
                "lomin": float(geo_coordinates[2]),
                "lomax": float(geo_coordinates[3]),
            }
            response = self.connector(self.__url_airplanes, params=params)
            self.airplanes = response.json()
            return self.airplanes
        else:
            return
