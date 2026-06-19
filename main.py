from src.abs_api import SearchAreaData
from src.utils import filter_airplanes, get_aeroplanes_by_altitude, sort_airplanes, get_top_aeroplanes, print_aeroplanes
from src.airсraft_attrib import Airplane
from src.abs_for_file import JSONSaver

def user_interaction():
    # 1. Ввод данных
    country = input("Введите название страны (на английском): ").strip()

    while True:
        try:
            top_n = int(input("Введите количество самолётов для вывода в топ N: "))
            if top_n <= 0:
                print("Число должно быть положительным. Попробуйте ещё раз.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое положительное число.")

    filter_countries = input \
        ("Страны для дополнительной фильтрации (через пробел, Enter чтобы пропустить): ").strip().split()
    altitude_range = input("Диапазон высот (MIN-MAX, например 1000-5000, Enter чтобы пропустить): ").strip()

    # 2. Загрузка сырых данных
    search = SearchAreaData()
    search.get_data(country)

    # Если страна не найдена или нет boundingbox, search.airplanes останется None
    if search.airplanes is None:
        print("Не удалось получить данные о самолётах. Завершаем работу.")
        return

    raw_data = search.airplanes

    # 3. Преобразование в объекты
    planes = Airplane.cast_to_object_list(raw_data)

    # 4. Цепочка обработки
    planes = filter_airplanes(planes, filter_countries)

    if altitude_range:  # если пользователь что-то ввёл
        planes = get_aeroplanes_by_altitude(planes, altitude_range)

    planes = sort_airplanes(planes)
    top_planes = get_top_aeroplanes(planes, top_n)

    # 5. Вывод результата
    print_aeroplanes(top_planes)

    saver = JSONSaver()
    for plane in top_planes:
        saver.add_info(plane)
    print("Топ самолётов сохранён в airplanes.json")

if __name__ == "__main__":
    user_interaction()