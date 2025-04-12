# script.py
import re

file_path = "requirements.txt"

# Список пакетов для удаления
packages_to_remove = {
    "torch",
    "torchvision",
    "torchaudio",
    "numpy"
}

# Создаем регулярное выражение для точного совпадения с началом строки
pattern = re.compile(r"^(?:{})(?:$|[^a-zA-Z0-9])".format("|".join(re.escape(pkg) for pkg in packages_to_remove)))

with open(file_path, "r") as file:
    lines = file.readlines()

with open(file_path, "w") as file:
    for line in lines:
        stripped_line = line.strip()

        # Пропускаем строку, если она соответствует регулярному выражению
        if pattern.match(stripped_line):
            continue

        # Если строка содержит 'comfyui-frontend-package==', заменяем её
        if stripped_line.startswith("comfyui-frontend-package"):
            file.write("comfyui-frontend-package\n")
            continue

        # Иначе записываем строку как есть
        file.write(line)