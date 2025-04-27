import argparse

def process_files(additional_packages):
    file_path = "requirements.txt"

    # Создаем регулярное выражение для точного совпадения с началом строки

    with open(file_path, "r") as file:
        lines = file.readlines()

    if additional_packages:
        try:
            with open(additional_packages, "r") as file:
                lines_add = file.readlines()
            lines.append("\n")
            lines.extend(lines_add)
        except FileNotFoundError:
            print(f"Файл {additional_packages} не найден. Пропускаем добавление пакетов.")

    with open(file_path, "w") as file:
        for line in lines:
            stripped_line = line.strip()

            # Иначе записываем строку как есть
            file.write(line)


if __name__ == "__main__":
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description="Объединяет содержимое requirements.txt и дополнительного файла.")

    # Добавляем аргумент --add_package
    parser.add_argument(
        "--add_package",
        # default="python-packages-to-add.txt",
        default=None,
        help="Путь к дополнительному файлу с пакетами. По умолчанию: python-packages-to-add.txt."
    )

    args = parser.parse_args()

    process_files(args.add_package)

