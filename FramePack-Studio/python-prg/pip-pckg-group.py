import re


# Чтение списка пакетов из файла requirements.txt
def read_packages(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # Убираем комментарии и пустые строки
    packages = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return packages


# Группировка пакетов
def group_packages(packages):
    groups = {
        "nvidia": [],
        "torch": [],
        "xformers": [],
        "other": []
    }

    for package in packages:
        # Извлекаем название пакета и версию
        # match = re.match(r'^([\w-]+)==([\d\.]+)', package)
        match = re.match(r'^([^=]+)==(.+)$', package)
        if not match:
            continue  # Пропускаем некорректные строки
        name, version = match.groups()

        # Группируем по названию
        if name.startswith("nvidia"):
            groups["nvidia"].append(f"{name}=={version}")
        elif name.startswith("torch"):
            groups["torch"].append(f"{name}=={version}")
        elif name.startswith("xformers"):
            groups["xformers"].append(f"{name}=={version}")
        else:
            groups["other"].append(f"{name}=={version}")

    return groups


# Запись групп в файлы
def write_groups(groups, output_dir):
    for group_name, packages in groups.items():
        file_path = f"{output_dir}/{group_name}_requirements.txt"
        with open(file_path, 'w') as f:
            f.write("\n".join(packages))
        print(f"Group {group_name} saved to {file_path}")


# Основная функция
def main():
    input_file = "requirements.out"  # Файл с полным списком пакетов
    output_dir = ".."  # Директория для сохранения групп

    # Шаги
    packages = read_packages(input_file)
    grouped_packages = group_packages(packages)
    write_groups(grouped_packages, output_dir)


if __name__ == "__main__":
    main()