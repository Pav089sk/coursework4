import requests
from requests import get
from abc import ABC, abstractmethod


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
        self.__url_coord = 'https://nominatim.openstreetmap.org/search'
        self.__url_airplanes = 'https://opensky-network.org/api/states/all'
        self.airplanes = None

    def connector(self, url: str, headers=None, params=None):
        """Метод подключения к API"""
        return requests.get(url, headers=headers, params=params)

    def get_data(self, country: str):
        """Метод получения данных о самолётах по координатам"""
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }
        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }
        response = self.connector(
            self.__url_coord,
            headers=headers_nominatim,  # явно указываем имя аргумента
            params=params_nominatim  # явно указываем имя аргумента
        )
        if response.status_code == 200:
            data = response.json()
            if not data:
                print('Страна не найдена')
                return

            geo_coordinates = data[0].get('boundingbox')
            if geo_coordinates is None:
                print("Нет boundingbox")
                return
            # Параметры для фильтрации самолетов по их географическим координатам.
            params = {'lamin': float(geo_coordinates[0]),
                      'lamax': float(geo_coordinates[1]),
                      'lomin': float(geo_coordinates[2]),
                      'lomax': float(geo_coordinates[3]), }
            response = get(url=self.__url_airplanes, params=params)
            self.airplanes = response.json()
            print(self.airplanes)
        else:
            print(f'код ошибки {response.status_code}')
            print(f'Сервис {self.__url_coord} недоступен')


if __name__ == '__main__':
    api = SearchAreaData()
    api.get_data('Italy')
