import os
import argparse


def find_requirements_files(directory):
    """
    Рекурсивно ищет все файлы requirements.txt в указанной директории и её поддиректориях.
    Возвращает список путей к найденным файлам.
    """
    requirements_files = []
    for root, _, files in os.walk(directory):
        if 'requirements.txt' in files:
            requirements_files.append(os.path.join(root, 'requirements.txt'))
    return requirements_files


def read_unique_lines(file_path):
    """
    Читает строки из файла, удаляет дубликаты и возвращает их как множество.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Удаляем лишние пробелы и переводы строк
    return set(line.strip() for line in lines if line.strip())


def merge_requirements(output_file, input_files):
    """
    Объединяет все строки из входных файлов, удаляет дубликаты,
    сортирует их и записывает в выходной файл.
    """
    all_lines = set()
    for file_path in input_files:
        all_lines.update(read_unique_lines(file_path))

    # Сортируем строки
    sorted_lines = sorted(all_lines)

    # Записываем отсортированные строки в выходной файл
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(sorted_lines) + '\n')


def main():
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description="Объединение всех requirements.txt в один файл.")
    parser.add_argument(
        "directory",
        nargs="?",  # Делает аргумент необязательным
        default=os.getcwd(),  # Если аргумент не указан, используется текущая директория
        help="Директория, с которой начать поиск файлов requirements.txt"
    )
    args = parser.parse_args()

    # Начальная директория
    start_directory = args.directory

    # Проверяем, существует ли указанная директория
    if not os.path.isdir(start_directory):
        print(f"Ошибка: Директория '{start_directory}' не существует.")
        return

    # Находим все файлы requirements.txt
    requirements_files = find_requirements_files(start_directory)

    if not requirements_files:
        print("Файлы requirements.txt не найдены.")
        return

    # Путь к объединенному файлу
    output_file = os.path.join(start_directory, 'requirements-common.txt')

    # Объединяем файлы
    merge_requirements(output_file, requirements_files)

    print(f"Объединенный файл создан: {output_file}")


if __name__ == "__main__":
    main()