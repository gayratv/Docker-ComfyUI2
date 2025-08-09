#!/usr/bin/env python3
"""
check_requirements_and_cleanup.py

Описание:
    Этот скрипт проверяет наличие файла requirements.txt (или другого указанного имени)
    в заданной директории. Если файл не найден, скрипт удаляет указанную директорию
    вместе со всем её содержимым (поддиректориями и файлами).

Использование:
    python3 check_requirements_and_cleanup.py /путь/к/директории [--requirements имя_файла]

Аргументы:
    1. directory (обязательный): путь к директории, которую нужно проверить.
    2. --requirements (необязательный): имя файла requirements (по умолчанию requirements.txt).

Пример:
    python3 check_requirements_and_cleanup.py /workspace/ComfyUI/custom_nodes/ComfyUI-Inspire-Pack/
    python3 check_requirements_and_cleanup.py /some/dir --requirements custom_reqs.txt
"""

import argparse
import os
import shutil
from pathlib import Path

def process_directory(directory: Path, requirements_filename: str):
    requirements_path = directory / requirements_filename

    if not directory.exists():
        print(f"Ошибка: директория {directory} не существует.")
        return

    if not requirements_path.exists():
        print(f"Файл {requirements_filename} не найден. Удаляю директорию {directory}...")
        shutil.rmtree(directory)
        print("Директория успешно удалена.")
    else:
        print(f"Файл {requirements_filename} найден. Директория сохранена.")

def main():
    parser = argparse.ArgumentParser(description="Проверка наличия файла и удаление директории при его отсутствии.")
    parser.add_argument(
        "directory",
        type=Path,
        help="Путь к директории для проверки (обязательный параметр)."
    )
    parser.add_argument(
        "--requirements",
        default="requirements.txt",
        help="Имя файла requirements (по умолчанию requirements.txt)"
    )

    args = parser.parse_args()
    process_directory(args.directory, args.requirements)

if __name__ == "__main__":
    main()
