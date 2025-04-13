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

def display_offers():
    # Открываем и читаем файл
    try:
        with open(file_path_json, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что в данных есть список offers
        if 'offers' in data:
            # Сортируем данные по значению total_hour
            sorted_offers = sorted(
                data['offers'],
                key=lambda offer: offer.get('search', {}).get('totalHour', float('inf'))
            )

            # Выводим заголовок таблицы
            print(f"{'ID':<10} {'CPU RAM':<10} {'GPU Name':<15} {'Inet Down':<12} {'IDown Cost':<15} {'IDown Cost TB':<15}  {'Setup Cost':<12} {'Machine ID':<12} {'$/HR':<12}")
            print("-" * 97)  # Разделительная линия

            for offer in sorted_offers:
                # Извлекаем необходимые данные
                offer_id = offer.get('id')
                cpu_ram = offer.get('cpu_ram')
                gpu_name = offer.get('gpu_name')
                inet_down = offer.get('inet_down')
                inet_down_cost = offer.get('inet_down_cost')
                internet_down_cost_per_tb = offer.get('internet_down_cost_per_tb')
                machine_id = offer.get('machine_id')
                total_hour = offer.get('search', {}).get('totalHour')

                # Вычисляем Setup cost
                setup_cost = inet_down_cost * 40 if inet_down_cost is not None else 0

                # Выводим данные в формате столбцов с фиксированной шириной
                print(f"{offer_id:<10} {cpu_ram:<10} {gpu_name:<15} {inet_down:<12.1f} {inet_down_cost:<15.6f} {internet_down_cost_per_tb:<15.6f} {setup_cost:<12.6f} {machine_id:<12} {total_hour:<12.6f}")
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