"""
Модуль для импорта данных из JSON-файла в базу данных MySQL.
"""

from typing import Optional, List, Tuple
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from mysql.connector import Error
from .db_connection import create_db_connection

class DisplayOffers:
    """
    Класс для импорта данных из JSON-файла в таблицу offers базы данных.
    """

    def __init__(self,  batch_num_param:int):
        self.batch_num_param = batch_num_param
        self.conn: Optional[MySQLConnection] = None
        self.cursor: Optional[MySQLCursor] = None

    def connect_to_db(self) -> None:
        """
        Подключение к базе данных.
        """
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
        if self.conn:
            self.conn.close()


    def execute_query(query: str, params: Optional[Tuple] = None) -> Optional[List[Tuple]]:
        """
        Выполняет SQL-запрос и возвращает результаты.

        :param query: SQL-запрос для выполнения.
        :param params: Параметры для подстановки в запрос (если есть).
        :return: Список кортежей с результатами для SELECT-запросов или None для других типов запросов.
        """
        connection: Optional[MySQLConnection] = None
        cursor: Optional[MySQLCursor] = None
        try:
            # Создаем подключение к базе данных
            connection = create_db_connection()
            if connection is None:
                raise Exception("Не удалось установить соединение с базой данных.")

            # Создаем курсор для выполнения запроса
            cursor = connection.cursor()

            # Выполняем запрос с параметрами (если они есть)
            cursor.execute(query, params)

            # Если это SELECT-запрос, извлекаем результаты
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                return result
            else:
                # Для INSERT, UPDATE, DELETE фиксируем изменения
                connection.commit()
                return None

        except Error as e:
            # Обрабатываем ошибки базы данных
            print(f"Ошибка при выполнении запроса: {e}")
            if connection and connection.is_connected():
                connection.rollback()  # Откатываем изменения в случае ошибки
            return None

        finally:
            # Закрываем курсор и соединение
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()


    def display_results(self) -> None:
        query = "SELECT * FROM offers WHERE batch_number = %s"
        params = (self.batch_num_param,)
        result=self.execute_query(query, params)
        if result:
            for row in result:
                print(row)
        else:
            print("Запрос не вернул результатов или произошла ошибка.")

# Пример использования
if __name__ == "__main__":
    display = DisplayOffers(59)
    display.display_results()