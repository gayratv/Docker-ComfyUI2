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
from tabulate import tabulate


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
                SELECT o.id as id, \
                       search_totalHour          AS "$/HR", \
                       internet_down_cost_per_tb AS "idown$/TB", \
                       inet_down, \
                       geolocation, \
                       gpu_name, \
                       host_id, \
                       vericode, \
                       cuda_max_good 
                FROM offers o
                    left join  
                     vast.bad_machines bm 
                        on o.machine_id = bm.machine_id
                WHERE batch_number = %s and vericode < 2 and bm.id is null and o.internet_down_cost_per_tb < 6
                ORDER BY search_totalHour \
                """


        params = (self.batch_num_param,)
        result = self.execute_query(query, params)

        # Определяем заголовки для таблицы
        headers = ["ID", "$/HR", "idown$/TB", "inet_down", "geolocation", "gpu_name", "host_id", "vericode","cuda_max_good"]

        if result:
            formatted_result = [
                (
                    row[0],  # ID
                    round(row[1], 2),  # $/HR
                    round(row[2], 2),  # idown$/TB
                    row[3],  # inet_down
                    row[4],  # geolocation
                    row[5],  # gpu_name
                    row[6],
                    row[7],
                    row[8]
                )
                for row in result
            ]

            # # Форматируем заголовки с разделителями
            # header_row = " | ".join(f"{header:^10}" for header in headers)
            # print(header_row)
            # print("-" * len(header_row))  # Разделитель под заголовками
            #
            # # Форматируем строки данных с разделителями
            # for row in formatted_result:
            #     data_row = " | ".join(f"{str(value):^10}" for value in row)
            #     print(data_row)

            # table = tabulate(formatted_result, headers=headers, tablefmt="grid")
            table = tabulate(formatted_result, headers=headers, tablefmt="simple")
            print(table)

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