import json

# Указываем путь к вашему JSON файлу
file_path = 'vast-search.json'

# Открываем и читаем файл
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Проверяем, что в данных есть список offers
if 'offers' in data:
    # Выводим заголовок таблицы
    print(f"{'ID':<10} {'CPU RAM':<10} {'GPU Name':<15} {'Inet Down':<12} {'IDown Cost':<15} {'IDown Cost TB':<15}  {'Setup Cost':<12} {'Machine ID':<12} {'Total Hour':<12}")
    print("-" * 97)  # Разделительная линия

    for offer in data['offers']:
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
        setup_cost = inet_down_cost * 40

        # Выводим данные в формате столбцов с фиксированной шириной
        print(f"{offer_id:<10} {cpu_ram:<10} {gpu_name:<15} {inet_down:<12.1f} {inet_down_cost:<15.6f} {internet_down_cost_per_tb:<15.6f} {setup_cost:<12.6f} {machine_id:<12} {total_hour:<12.6f}")
else:
    print("В файле нет данных о предложениях.")