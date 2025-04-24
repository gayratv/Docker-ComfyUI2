"""
Модуль для импорта данных из JSON-файла в базу данных MySQL.
"""

import json
import os
from typing import Optional, List, Tuple
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector import Error
from .db_connection import create_db_connection


class DisplayOffers:
    """
    Класс для импорта данных из JSON-файла в таблицу offers базы данных.
    """

    def __init__(self, batch_num_param: int):
        self.batch_num_param = batch_num_param
        self.conn: Optional[MySQLConnection] = None
        self.cursor: Optional[MySQLCursor] = None

    def connect_to_db(self) -> None:
        """
        Подключение к базе данных.
        """
        if not self.conn or not self.conn.is_connected():
            self.conn = create_db_connection()
            if not self.conn:
                raise ConnectionError("Не удалось подключиться к базе данных.")
            self.cursor = self.conn.cursor()

    def disconnect_from_db(self) -> None:
        """
        Отключение от базы данных.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
        self.conn = None
        self.cursor = None

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> Optional[List[Tuple]]:
        """
        Выполняет SQL-запрос и возвращает результаты.

        :param query: SQL-запрос для выполнения.
        :param params: Параметры для подстановки в запрос (если есть).
        :return: Список кортежей с результатами для SELECT-запросов или None для других типов запросов.
        """
        try:
            # Убедимся, что соединение установлено
            self.connect_to_db()

            # Выполняем запрос с параметрами (если они есть)
            self.cursor.execute(query, params)

            # Если это SELECT-запрос, извлекаем результаты
            if query.strip().upper().startswith("SELECT"):
                result = self.cursor.fetchall()
                return result
            else:
                # Для INSERT, UPDATE, DELETE фиксируем изменения
                self.conn.commit()
                return None

        except Error as e:
            # Обрабатываем ошибки базы данных
            print(f"Ошибка при выполнении запроса: {e}")
            if self.conn and self.conn.is_connected():
                self.conn.rollback()  # Откатываем изменения в случае ошибки
            return None

    def display_results(self) -> None:
        """
        Отображает результаты запроса к таблице offers.
        """
        query = """
                SELECT id, \
                       search_totalHour          AS "$/HR", \
                       internet_down_cost_per_tb AS "idown$/TB", \
                       inet_down, \
                       geolocation, \
                       gpu_name, \
                       host_id
                FROM offers
                WHERE batch_number = %s
                ORDER BY search_totalHour \
                """

        params = (self.batch_num_param,)
        result = self.execute_query(query, params)
        if result:
            for row in result:
                print(row)
        else:
            print("Запрос не вернул результатов или произошла ошибка.")

    def __enter__(self):
        """
        Метод для использования класса в контекстном менеджере.
        """
        self.connect_to_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Метод для закрытия соединения при выходе из контекстного менеджера.
        """
        self.disconnect_from_db()


# Пример использования
if __name__ == "__main__":
    with DisplayOffers(59) as display:
        display.display_results()