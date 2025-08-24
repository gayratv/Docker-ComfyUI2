'''
 /mnt/d/4/Cursor AI [Udemy] [Грегори Джон]

cd /mnt/f/_prg/python/Docker-ComfyUI/py-prg/rename-files
python remove-skladchik.py "/mnt/d/4/Cursor AI [Udemy] [Грегори Джон]"
'''

import os
import argparse


def rename_files_in_directory(directory_path):
    """
    Рекурсивно сканирует директории и поддиректории, удаляет '[skladchik.org]'
    из имен файлов и переименовывает их.

    Args:
        directory_path (str): Путь к директории для сканирования.
    """
    # Проверяем, существует ли указанный путь
    if not os.path.exists(directory_path):
        print(f"Ошибка: Директория '{directory_path}' не найдена.")
        return

    print(f"Начинаем сканирование и переименование в '{directory_path}'...")

    # Рекурсивный обход директорий
    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            # Проверяем, содержит ли имя файла искомую подстроку
            if '[skladchik.org]' in filename:
                old_path = os.path.join(dirpath, filename)

                # Создаем новое имя файла, удаляя подстроку
                new_filename = filename.replace('[skladchik.org]', '').strip()
                # Удаляем лишние пробелы, которые могли появиться

                # Если новое имя файла пустое, можно пропустить или придумать правило
                if not new_filename:
                    print(f"Предупреждение: Имя файла '{filename}' станет пустым после удаления подстроки. Пропускаем.")
                    continue

                new_path = os.path.join(dirpath, new_filename)

                try:
                    # Переименовываем файл
                    os.rename(old_path, new_path)
                    print(f'Переименовано: {old_path} -> {new_path}')
                except OSError as e:
                    print(f'Ошибка при переименовании {old_path}: {e}')


if __name__ == '__main__':
    # Настройка парсера аргументов
    parser = argparse.ArgumentParser(
        description="Скрипт для удаления '[skladchik.org]' из имен файлов в указанной директории и ее поддиректориях.")
    parser.add_argument('directory', type=str, help="Путь к директории для сканирования.")

    # Парсинг аргументов
    args = parser.parse_args()

    # Вызов основной функции с аргументом из командной строки
    rename_files_in_directory(args.directory)
