# script.py
import re

file_path = "requirements.txt"

# Создаем регулярное выражение для точного совпадения с началом строки

with open(file_path, "r") as file:
    lines = file.readlines()

with open(file_path, "w") as file:
    for line in lines:
        stripped_line = line.strip()

        # Если строка содержит 'comfyui-frontend-package==', заменяем её
        if stripped_line.startswith("comfyui-frontend-package"):
            file.write("comfyui-frontend-package\n")
            continue

        # Иначе записываем строку как есть
        file.write(line)