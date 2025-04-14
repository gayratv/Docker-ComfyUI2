import requests
import json
from urllib.parse import urlencode
import argparse

# Указываем путь к JSON файлу
file_path_json = 'vast-search.json'

def fetch_vast_data(gpu_name, cpu_ram):
    # URL для запроса
    url = "https://cloud.vast.ai/api/v0/search/asks/"

    # Параметры запроса с учетом переданных аргументов
    query_data = {
        "q": json.dumps({
            "gpu_name": {"eq": gpu_name},
            "num_gpus": {"eq": 1},
            "rentable": {"eq": True},
            "cuda_max_good": {"gte": "12.4"},
            "cpu_ram": {"gte": str(cpu_ram)},
            "inet_down": {"gte": "1000.0"},
            "gpu_frac": {"gte": "0.5"},
            "disk_space": {"gte": "100.0"}
        })
    }

    # Кодирование параметров с помощью urlencode
    encoded_params = urlencode(query_data)

    # Полный URL с закодированными параметрами
    full_url = f"{url}?{encoded_params}"

    # Выполнение GET-запроса
    response = requests.get(full_url)

    # Проверка статуса ответа
    if response.status_code == 200:
        data = response.json()

        # Проверка наличия ключа 'offers' в ответе
        if "offers" in data and isinstance(data["offers"], list):
            # Подсчет количества записей в массиве offers
            offer_count = len(data["offers"])
            print(f"\nКоличество записей в массиве 'offers': {offer_count}\n")

        # Сохранение результата в файл vast-search.json
        with open(file_path_json, "w") as file:
            json.dump(data, file, indent=4)
        print("Данные успешно сохранены в файл vast-search.json\n")
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
        print(f"Ответ сервера: {response.text}")

import json

import json

import json

import json

import json

# columns = [
#         {"var_name": "id", "title": "ID", "width": 10, "order_num": 1, "decimal_places": None},
#         {"var_name": "search.totalHour", "title": "Tot $/HR", "width": 10, "order_num": 2, "decimal_places": 2},
#         {"var_name": "cpu_ram", "title": "CPU RAM", "width": 10, "order_num": 3, "decimal_places": None},
#         {"var_name": "gpu_frac", "title": "GPU Frac", "width": 10, "order_num": 4, "decimal_places": 1},
#         {"var_name": "inet_down", "title": "Inet Down", "width": 10, "order_num": 5, "decimal_places": 1},
#         {"var_name": "search.gpuCostPerHour", "title": "GPU $/HR", "width": 9, "order_num": 6, "decimal_places": 2},
#         {"var_name": "search.diskHour", "title": "Disk $/HR", "width": 10, "order_num": 7, "decimal_places": 3},
#         {"var_name": "instance.diskHour", "title": "Inst Disk $/HR", "width": 15, "order_num": 8, "decimal_places": 3},
#         {"var_name": "instance.totalHour", "title": "Inst Tot $/HR", "width": 15, "order_num": 9, "decimal_places": 4},
#         {"var_name": "internet_down_cost_per_tb", "title": "IDown Cost TB", "width": 15, "order_num": 10, "decimal_places": 2},
#         {"var_name": "storage_cost", "title": "Storage Cost", "width": 15, "order_num": 11, "decimal_places": 3},
#         {"var_name": "storage_total_cost", "title": "Storage Total Cost", "width": 15, "order_num": 12, "decimal_places": 3},
#         {"var_name": "inet_down_cost", "title": "IDown Cost", "width": 12, "order_num": 13, "decimal_places": 4},
#         {"var_name": "host_id", "title": "Host ID", "width": 10, "order_num": 14, "decimal_places": None},
#         {"var_name": "machine_id", "title": "Machine ID", "width": 12, "order_num": 15, "decimal_places": None},
#     ]


def display_offers():
    # Определяем структуру вывода
    columns = [
        {"var_name": "id", "title": "ID", "width": 10, "order_num": 1, "decimal_places": None},
        {"var_name": "search.totalHour", "title": "Tot $/HR", "width": 10, "order_num": 2, "decimal_places": 2},
        {"var_name": "internet_down_cost_per_tb", "title": "IDown Cost TB", "width": 15, "order_num": 3, "decimal_places": 2},
        {"var_name": "inet_down", "title": "Inet Down", "width": 10, "order_num": 4, "decimal_places": 1},
        {"var_name": "cpu_ram", "title": "CPU RAM", "width": 10, "order_num": 5, "decimal_places": None},
        {"var_name": "gpu_frac", "title": "GPU Frac", "width": 10, "order_num": 6, "decimal_places": 1},
        {"var_name": "search.gpuCostPerHour", "title": "GPU $/HR", "width": 9, "order_num": 7, "decimal_places": 2},
        {"var_name": "instance.totalHour", "title": "Inst Tot $/HR", "width": 15, "order_num": 8, "decimal_places": 4},
        {"var_name": "storage_cost", "title": "Storage Cost", "width": 15, "order_num": 9, "decimal_places": 3},
        {"var_name": "storage_total_cost", "title": "Storage Total Cost", "width": 15, "order_num": 10, "decimal_places": 3},
        {"var_name": "host_id", "title": "Host ID", "width": 10, "order_num": 11, "decimal_places": None},
        {"var_name": "machine_id", "title": "Machine ID", "width": 12, "order_num": 12, "decimal_places": None},
    ]

    # Открываем и читаем файл
    try:
        with open(file_path_json, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что в данных есть список offers
        if 'offers' in data:
            # Сортируем данные по значению search.totalHour
            sorted_offers = sorted(
                data['offers'],
                key=lambda offer: offer.get('search', {}).get('totalHour', float('inf'))
            )

            # Формируем заголовок таблицы
            header = ""
            separator = ""
            for col in sorted(columns, key=lambda x: x["order_num"]):
                header += f"{col['title']:<{col['width']}}"
                separator += "-" * col["width"]
            print(header)
            print(separator)

            # Выводим данные
            for offer in sorted_offers:
                row = ""
                for col in sorted(columns, key=lambda x: x["order_num"]):
                    var_name = col["var_name"]
                    width = col["width"]
                    decimal_places = col["decimal_places"]

                    # Извлекаем значение из данных
                    if '.' in var_name:
                        # Для вложенных полей (например, search.totalHour)
                        keys = var_name.split('.')
                        value = offer
                        for key in keys:
                            value = value.get(key, None)
                            if value is None:
                                break
                    else:
                        # Для простых полей
                        value = offer.get(var_name, None)

                    # Форматируем значение
                    if isinstance(value, float) and decimal_places is not None:
                        row += f"{value:<{width}.{decimal_places}f}"
                    elif isinstance(value, int):
                        row += f"{value:<{width}}"
                    else:
                        row += f"{'':<{width}}"
                print(row)
        else:
            print("В файле нет данных о предложениях.")
    except FileNotFoundError:
        print("Файл vast-search.json не найден. Сначала выполните запрос к API.")

if __name__ == "__main__":
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Поиск предложений Vast.ai с фильтрацией по GPU и CPU RAM.")
    parser.add_argument("--gpu", type=str, default="RTX 3090", help="Модель GPU (например, 'RTX 3090')")
    parser.add_argument("--ram", type=int, default=32000, help="Минимальный объем оперативной памяти в МБ (например, 32000)")

    args = parser.parse_args()

    # Выполняем запрос к API
    fetch_vast_data(args.gpu, args.ram)

    # Отображаем результаты
    display_offers()

    #  python script.py --gpu "RTX 3090" --ram 32000