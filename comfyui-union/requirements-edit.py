import argparse
from get_pyth_pckg_last_ver import get_latest_version

def process_files(frontend_ver, additional_packages):
    file_path = "requirements.txt"

    # Создаем регулярное выражение для точного совпадения с началом строки

    with open(file_path, "r") as file:
        lines = file.readlines()

    if additional_packages :
        with open(additional_packages, "r") as file:
            lines_add = file.readlines()

    lines.append("\n")
    lines.extend(lines_add)

    with open(file_path, "w") as file:
        for line in lines:
            stripped_line = line.strip()

            # Если строка содержит 'comfyui-frontend-package==', заменяем её
            if stripped_line.startswith("comfyui-frontend-package"):
                file.write(f"comfyui-frontend-package=={frontend_ver}\n")
                continue

            # Иначе записываем строку как есть
            file.write(line)


if __name__ == "__main__":
    # Настройка парсера аргументов командной строки
    parser = argparse.ArgumentParser(description="Объединяет содержимое requirements.txt и дополнительного файла.")

    # Добавляем аргумент --add_package
    parser.add_argument(
        "--add_package",
        # default="python-packages-to-add.txt",
        help="Путь к дополнительному файлу с пакетами. По умолчанию: python-packages-to-add.txt."
    )

    parser.add_argument(
        "--frontend_ver",
        help="Путь к дополнительному файлу с пакетами. По умолчанию: python-packages-to-add.txt."
    )

    # Парсим аргументы командной строки
    args = parser.parse_args()

    print(f"------- args.frontend_ver |{args.frontend_ver}|")

    if args.frontend_ver and args.frontend_ver !='""' :
        frontend_ver = args.frontend_ver
    else:
        frontend_ver = get_latest_version("comfyui-frontend-package")

    print("frontend_ver:", frontend_ver)

    # Вызываем функцию для обработки файлов
    process_files(frontend_ver,args.add_package)

