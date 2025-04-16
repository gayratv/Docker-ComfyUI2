# process_contracts.py

import os
import json
from typing import Optional, Tuple
from db_connection import create_db_connection
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor


def process_contract(id: int) -> None:
    """
    Читает файл vast-create-instance.txt, извлекает данные о контракте,
    получает последнюю запись из таблицы vast.batches и записывает данные в таблицу contracts.

    Args:
        id (int): Входной параметр id для записи в таблицу contracts.
    """
    # Определяем путь к файлу
    file_path = os.path.join(os.path.dirname(__file__), '..', 'vast-create-instance.txt')

    # Проверяем существование файла
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return

    # Читаем содержимое файла
    with open(file_path, 'r') as file:
        content = file.read().strip()

    # Парсим JSON-часть из строки
    try:
        # Извлекаем JSON-строку после "Started."
        json_part = content.split("Started.")[1].strip()
        data = json.loads(json_part)

        # Извлекаем new_contract из данных
        new_contract = data.get('new_contract')
        if new_contract is None:
            print("Ошибка: Поле 'new_contract' отсутствует в данных.")
            return

    except (IndexError, json.JSONDecodeError) as e:
        print(f"Ошибка при парсинге файла: {e}")
        return

    # Подключаемся к базе данных
    conn: Optional[MySQLConnection] = create_db_connection()

    if conn is None:
        print("Не удалось подключиться к базе данных.")
        return

    cursor: MySQLCursor = conn.cursor()

    try:
        # Получаем последнюю запись из таблицы batches
        cursor.execute("SELECT batch_number FROM vast.batches ORDER BY batch_number DESC LIMIT 1")
        result = cursor.fetchone()

        if result is None:
            print("Таблица vast.batches пуста. Нет записей для обработки.")
            return

        batch_number = result[0]

        # Записываем данные в таблицу contracts
        insert_query = """
        INSERT INTO vast.contracts (id, batch_number, contract)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (id, batch_number, new_contract))

        # Фиксируем изменения
        conn.commit()
        print(f"Данные успешно записаны: id={id}, batch_number={batch_number}, contract={new_contract}")

    except Exception as e:
        print(f"Ошибка при выполнении запросов: {e}")
        conn.rollback()

    finally:
        # Закрываем соединение
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Пример вызова функции с параметром id
    process_contract(id=123)