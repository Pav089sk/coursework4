from src.abs_api import SearchAreaData
from src.utils import filter_airplanes, get_aeroplanes_by_altitude, sort_airplanes, get_top_aeroplanes, print_aeroplanes
from src.aircraft_attrib import Airplane
from src.abs_for_file import JSONSaver


def user_interaction():
    country = input("Введите название страны (на английском, например Canada): ").strip()
    if not country:
        print("Страна не может быть пустой.")
        return

    while True:
        try:
            top_n = int(input("Введите количество самолётов для вывода в топ: "))
            if top_n <= 0:
                print("Число должно быть положительным. Попробуйте ещё раз.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое положительное число.")

    filter_countries = input(
        "Страны для дополнительной фильтрации (через пробел, Enter чтобы пропустить): ").strip().split()
    altitude_range = input("Диапазон высот (MIN-MAX, например 1000-5000, Enter чтобы пропустить): ").strip()
    search = SearchAreaData()
    raw_data = search.get_data(country)

    if raw_data is None:
        print("Нет данных о самолётах для этой страны (возможно, страна не найдена или в зоне нет рейсов).")
        return
    planes = Airplane.cast_to_object_list(raw_data)
    if not planes:
        print(
            "Не удалось преобразовать данные в объекты самолётов. Проверьте индексы в cast_to_object_list (высота должна быть row[13]).")
        return
    planes = filter_airplanes(planes, filter_countries)

    if altitude_range:
        planes = get_aeroplanes_by_altitude(planes, altitude_range)

    if not planes:
        print(
            "После всех фильтров самолёты не найдены. Проверьте названия стран (полное название, например 'Canada') и диапазон высот.")
        return

    planes = sort_airplanes(planes)
    top_planes = get_top_aeroplanes(planes, top_n)
    print_aeroplanes(top_planes)
    saver = JSONSaver("airplanes.json")
    for plane in planes:
        saver.add_info(plane)
    print(f"Сохранено {len(planes)} самолётов в airplanes.json")


if __name__ == "__main__":
    user_interaction()
