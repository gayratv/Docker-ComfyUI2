import argparse

def process_files( additional_packages="python-packages-to-add.txt"):
    file_path = "requirements.txt"

    # Создаем регулярное выражение для точного совпадения с началом строки

    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(additional_packages, "r") as file:
        lines_add = file.readlines()

    lines.append("\n")
    lines.extend(lines_add)

    with open(file_path, "w") as file:
        for line in lines:
            stripped_line = line.strip()

            # Если строка содержит 'comfyui-frontend-package==', заменяем её
            if stripped_line.startswith("comfyui-frontend-package"):
                file.write("comfyui-frontend-package\n")
                continue

            # Иначе записываем строку как есть
            file.write(line)


if __name__ == "__main__":
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description="Объединяет содержимое requirements.txt и дополнительного файла.")

    # Добавляем аргумент --add_package
    parser.add_argument(
        "--add_package",
        default="python-packages-to-add.txt",
        help="Путь к дополнительному файлу с пакетами. По умолчанию: python-packages-to-add.txt."
    )

    # Парсим аргументы командной строки
    args = parser.parse_args()

    # Вызываем функцию для обработки файлов
    result = process_files(args.add_package)

