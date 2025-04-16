import json
import mysql.connector
from mysql.connector import Error

# Функция для подключения к базе данных
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=3307
        )
        print("Подключение к базе данных успешно установлено")
    except Error as e:
        print(f"Ошибка подключения: {e}")
    return connection

# Функция для выполнения SQL-запроса
def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Запрос выполнен успешно")
    except Error as e:
        print(f"Ошибка выполнения запроса: {e}")

# Основная программа
if __name__ == "__main__":
    # Параметры подключения
    host = "localhost"  # или IP-адрес сервера MySQL
    user = "root"       # имя пользователя
    password = "root"  # пароль
    database = "vast"  # название базы данных

    # Создаем подключение
    conn = create_connection(host, user, password, database)

    if conn is not None:
        # Читаем JSON из файла
        try:
            with open("../vast-search.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                print("JSON успешно загружен")
        except Exception as e:
            print(f"Ошибка чтения JSON: {e}")
            conn.close()
            exit()

            # Извлекаем список предложений из JSON
        if isinstance(data, dict) and "offers" in data:
            offers = data["offers"]
            print(f"Найдено {len(offers)} предложений")
        else:
            print("Ошибка: ключ 'offers' отсутствует или данные имеют неправильную структуру")
            conn.close()
            exit()

        # SQL-запросы для вставки или обновления данных
        insert_or_update_host_query = """
        INSERT INTO hosts (
            host_id, hosting_type, hostname, mobo_name, os_version, pci_gen, pcie_bw, public_ipaddr, static_ip,
            start_date, reliability, reliability_mult, rentable, rented, score, verification, vericode, vms_enabled,
            expected_reliability, rn
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            hosting_type = VALUES(hosting_type),
            hostname = VALUES(hostname),
            mobo_name = VALUES(mobo_name),
            os_version = VALUES(os_version),
            pci_gen = VALUES(pci_gen),
            pcie_bw = VALUES(pcie_bw),
            public_ipaddr = VALUES(public_ipaddr),
            static_ip = VALUES(static_ip),
            start_date = VALUES(start_date),
            reliability = VALUES(reliability),
            reliability_mult = VALUES(reliability_mult),
            rentable = VALUES(rentable),
            rented = VALUES(rented),
            score = VALUES(score),
            verification = VALUES(verification),
            vericode = VALUES(vericode),
            vms_enabled = VALUES(vms_enabled),
            expected_reliability = VALUES(expected_reliability),
            rn = VALUES(rn)
        """

        insert_or_update_gpu_query = """
        INSERT INTO gpus (
            host_id, gpu_name, gpu_ram, gpu_total_ram, gpu_max_power, gpu_max_temp, gpu_mem_bw, gpu_lanes, has_avx
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            gpu_name = VALUES(gpu_name),
            gpu_ram = VALUES(gpu_ram),
            gpu_total_ram = VALUES(gpu_total_ram),
            gpu_max_power = VALUES(gpu_max_power),
            gpu_max_temp = VALUES(gpu_max_temp),
            gpu_mem_bw = VALUES(gpu_mem_bw),
            gpu_lanes = VALUES(gpu_lanes),
            has_avx = VALUES(has_avx)
        """

        insert_or_update_network_query = """
        INSERT INTO network (
            host_id, inet_down, inet_down_cost, inet_up, inet_up_cost, is_bid
        ) VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            inet_down = VALUES(inet_down),
            inet_down_cost = VALUES(inet_down_cost),
            inet_up = VALUES(inet_up),
            inet_up_cost = VALUES(inet_up_cost),
            is_bid = VALUES(is_bid)
        """

        insert_or_update_storage_query = """
        INSERT INTO storage (
            host_id, storage_cost, storage_total_cost
        ) VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            storage_cost = VALUES(storage_cost),
            storage_total_cost = VALUES(storage_total_cost)
        """

        insert_or_update_costs_query = """
        INSERT INTO costs (
            host_id, dph_total_adj, vram_costperhour
        ) VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            dph_total_adj = VALUES(dph_total_adj),
            vram_costperhour = VALUES(vram_costperhour)
        """

        insert_or_update_search_query = """
        INSERT INTO search (
            host_id, gpu_cost_per_hour, disk_hour, total_hour, discount_total_hour, discounted_total_per_hour
        ) VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            gpu_cost_per_hour = VALUES(gpu_cost_per_hour),
            disk_hour = VALUES(disk_hour),
            total_hour = VALUES(total_hour),
            discount_total_hour = VALUES(discount_total_hour),
            discounted_total_per_hour = VALUES(discounted_total_per_hour)
        """

        insert_or_update_instance_query = """
        INSERT INTO instance (
            host_id, gpu_cost_per_hour, disk_hour, total_hour, discount_total_hour, discounted_total_per_hour
        ) VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            gpu_cost_per_hour = VALUES(gpu_cost_per_hour),
            disk_hour = VALUES(disk_hour),
            total_hour = VALUES(total_hour),
            discount_total_hour = VALUES(discount_total_hour),
            discounted_total_per_hour = VALUES(discounted_total_per_hour)
        """

        # Обработка данных JSON
        for item in offers:
            host_id = item.get("host_id")

            # Данные для таблицы hosts
            host_data = (
                host_id,
                item.get("hosting_type"),
                item.get("hostname"),
                item.get("mobo_name"),
                item.get("os_version"),
                item.get("pci_gen"),
                item.get("pcie_bw"),
                item.get("public_ipaddr"),
                item.get("static_ip"),
                item.get("start_date"),
                item.get("reliability"),
                item.get("reliability_mult"),
                item.get("rentable"),
                item.get("rented"),
                item.get("score"),
                item.get("verification"),
                item.get("vericode"),
                item.get("vms_enabled"),
                item.get("expected_reliability"),
                item.get("rn")
            )
            execute_query(conn, insert_or_update_host_query, host_data)

            # Данные для таблицы gpus
            gpu_data = (
                host_id,
                item.get("gpu_name"),
                item.get("gpu_ram"),
                item.get("gpu_total_ram"),
                item.get("gpu_max_power"),
                item.get("gpu_max_temp"),
                item.get("gpu_mem_bw"),
                item.get("gpu_lanes"),
                item.get("has_avx")
            )
            execute_query(conn, insert_or_update_gpu_query, gpu_data)

            # Данные для таблицы network
            network_data = (
                host_id,
                item.get("inet_down"),
                item.get("inet_down_cost"),
                item.get("inet_up"),
                item.get("inet_up_cost"),
                item.get("is_bid")
            )
            execute_query(conn, insert_or_update_network_query, network_data)

            # Данные для таблицы storage
            storage_data = (
                host_id,
                item.get("storage_cost"),
                item.get("storage_total_cost")
            )
            execute_query(conn, insert_or_update_storage_query, storage_data)

            # Данные для таблицы costs
            costs_data = (
                host_id,
                item.get("dph_total_adj"),
                item.get("vram_costperhour")
            )
            execute_query(conn, insert_or_update_costs_query, costs_data)

            # Данные для таблицы search
            search_data = (
                host_id,
                item["search"].get("gpuCostPerHour"),
                item["search"].get("diskHour"),
                item["search"].get("totalHour"),
                item["search"].get("discountTotalHour"),
                item["search"].get("discountedTotalPerHour")
            )
            execute_query(conn, insert_or_update_search_query, search_data)

            # Данные для таблицы instance
            instance_data = (
                host_id,
                item["instance"].get("gpuCostPerHour"),
                item["instance"].get("diskHour"),
                item["instance"].get("totalHour"),
                item["instance"].get("discountTotalHour"),
                item["instance"].get("discountedTotalPerHour")
            )
            execute_query(conn, insert_or_update_instance_query, instance_data)

        # Закрываем соединение
        conn.close()
        print("Соединение закрыто")