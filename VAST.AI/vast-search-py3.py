import requests
import json
from urllib.parse import urlencode
import argparse
from PY_mysql.vast_offers_to_sql import OfferImporter

# Указываем путь к JSON файлу
file_path_json = 'vast-search.json'

def fetch_vast_data(gpu_name1, cpu_ram):
    # URL для запроса
    url = "https://cloud.vast.ai/api/v0/search/asks/"

    gpu_name_filter =  {"eq": gpu_name1}

    query_data = {
        "q": json.dumps({
            "gpu_name": gpu_name_filter,
            "num_gpus": {"eq": 1},
            "rentable": {"eq": True},
            "cpu_ram": {"gte": str(cpu_ram)},
            "inet_down": {"gte": "800.0"},
            "disk_space": {"gte": "100.0"},
            "cuda_max_good": {"gte": "12.4"},
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


if __name__ == "__main__":
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Поиск предложений Vast.ai с фильтрацией по GPU и CPU RAM.")
    parser.add_argument("--gpu1", type=str, default="RTX 3090", help="Модель GPU (например, 'RTX 3090')")
    parser.add_argument("--gpu2", type=str)
    parser.add_argument("--ram", type=int, default=32000, help="Минимальный объем оперативной памяти в МБ (например, 32000)")

    args = parser.parse_args()

    # Выполняем запрос к API
    fetch_vast_data(args.gpu1, args.ram)

    importer = OfferImporter(json_file="vast-search.json")
    inserted1, batch_number1 = importer.insert_offers()

    if args.gpu2:
        print(f"===== args.gpu2: {args.gpu2}")
        fetch_vast_data(args.gpu2, args.ram)
        inserted2, batch_number2 = importer.insert_offers(batch_number1)
    else:
        inserted2=0

    print(f"inserted1: {inserted1}, inserted2: {inserted2}")


    #  python script.py --gpu "RTX 3090" --ram 32000