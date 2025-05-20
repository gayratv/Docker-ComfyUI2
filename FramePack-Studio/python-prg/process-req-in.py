import argparse
import os


def read_prefixes_from_file(prefixes_file_path):
    """
    Читает префиксы из файла для удаления строк.

    :param prefixes_file_path: Путь к файлу с префиксами
    :return: Список префиксов
    """
    try:
        with open(prefixes_file_path, 'r', encoding='utf-8') as file:
            prefixes = [line.strip() for line in file if line.strip()]
        return prefixes
    except FileNotFoundError:
        print(f"Файл {prefixes_file_path} не найден.")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении префиксов: {e}")
        return []


def read_additional_lines(additional_lines_file_path):
    """
    Читает дополнительные строки из файла для добавления.

    :param additional_lines_file_path: Путь к файлу с дополнительными строками
    :return: Список дополнительных строк
    """
    try:
        with open(additional_lines_file_path, 'r', encoding='utf-8') as file:
            additional_lines = [line.strip() for line in file if line.strip()]
        return additional_lines
    except FileNotFoundError:
        print(f"Файл {additional_lines_file_path} не найден.")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении дополнительных строк: {e}")
        return []


def remove_and_add_lines(input_file, output_file, prefixes_to_remove, additional_lines):
    """
    Удаляет строки из файла, начинающиеся с указанных префиксов,
    и добавляет новые строки в конец файла.

    :param input_file: Путь к исходному файлу requirements.in
    :param output_file: Путь к файлу для записи результата
    :param prefixes_to_remove: Список префиксов строк для удаления
    :param additional_lines: Список строк для добавления
    """

    print(f"аргументы input_file {input_file}")
    print(f"output_file {output_file}")
    print(f"prefixes_to_remove {prefixes_to_remove}")
    print(f"additional_lines {additional_lines}")


    try:
        # Читаем содержимое файла
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Фильтруем строки, исключая те, которые начинаются с указанных префиксов
        filtered_lines = [
            line for line in lines
            if not any(line.startswith(prefix) for prefix in prefixes_to_remove)
        ]

        # Добавляем новые строки в конец файла
        filtered_lines.extend([f"{line}\n" for line in additional_lines])

        # Записываем отфильтрованные строки в выходной файл
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(filtered_lines)

        print(f"Результат успешно записан в файл {output_file}.")

    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Описание аргументов командной строки
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Удаление и добавление строк в файл requirements.in.")

    # Обязательные аргументы с значениями по умолчанию
    parser.add_argument(
        "--requirements-file",
        type=str,
        default="requirements.in",
        help="Путь к файлу requirements.in (по умолчанию: requirements.in)"
    )
    parser.add_argument(
        "--prefixes-file",
        type=str,
        default="prefixes_to_remove.txt",
        help="Путь к файлу с префиксами для удаления строк (по умолчанию: prefixes_to_remove.txt)"
    )
    parser.add_argument(
        "--additional-lines-file",
        type=str,
        default="additional_lines.txt",
        help="Путь к файлу с дополнительными строками для добавления (по умолчанию: additional_lines.txt)"
    )

    # Парсинг аргументов
    args = parser.parse_args()

    # Генерация имени выходного файла
    base_name, ext = os.path.splitext(args.requirements_file)
    output_file = f"{base_name}.modify{ext}"

    # Читаем префиксы из файла
    prefixes_to_remove = read_prefixes_from_file(args.prefixes_file)

    # Читаем дополнительные строки из файла
    additional_lines = read_additional_lines(args.additional_lines_file)

    if prefixes_to_remove is not None and additional_lines is not None:
        # Вызов функции для удаления и добавления строк
        remove_and_add_lines(args.requirements_file, output_file, prefixes_to_remove, additional_lines)