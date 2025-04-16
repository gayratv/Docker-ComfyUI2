# db_connection.py

import mysql.connector
from mysql.connector import Error

def create_db_connection():
    """
    Создает и возвращает соединение с базой данных MySQL.
    В случае ошибки выводит сообщение об ошибке и возвращает None.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='vast',
            port=3307
        )
        if connection.is_connected():
            print("Успешное подключение к базе данных")
        return connection
    except Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None


    #  from db_connection import create_db_connection
    #  from src.db_connection import create_db_connection