#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для запуска aria2c с поддержкой токена HuggingFace.

Логика работы:
1) Проверяет наличие переменной окружения HF_TOKEN.
2) Читает model_file и --prefix (по умолчанию /workspace/ComfyUI/).
3) В каждой строке файла, начинающейся с "dir=", добавляет prefix перед исходным путём:
   Пример:
       dir=models/insightface/models/antelopev2
       → dir=/workspace/ComfyUI/models/insightface/models/antelopev2
   prefix нормализуется так, чтобы в конце был ровно один "/".
4) Сохраняет изменённый файл под именем <model_file>.modified.
5) Запускает aria2c с этим файлом.
6) Фильтрует из вывода строки "Redirecting to".

Примеры запуска:
    python3 aria_start_hf.py models.txt
        # Использует префикс по умолчанию: /workspace/ComfyUI/

    cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/python-prg/download-models
    export HF_TOKEN=HF_TOKEN
    python3 aria_start_hf.py hf.txt --prefix /mnt/d/_tmp
        # Добавляет префикс /mnt/storage/ перед каждым путём в dir=

    HF_TOKEN=ваш_токен python3 aria_start_hf.py models.txt
        # Передача токена напрямую в окружении (если не прописан в системе)
"""

import os
import sys
import subprocess
import shutil
import argparse

def parse_args():
    p = argparse.ArgumentParser(
        description="Запуск aria2c с токеном HuggingFace и добавлением префикса в dir=..."
    )
    p.add_argument("model_file", help="Путь к файлу списка для aria2c")
    p.add_argument(
        "--prefix",
        default="/workspace/ComfyUI/",
        help="Префикс, добавляемый перед путём в dir= (по умолчанию: /workspace/ComfyUI/)"
    )
    return p.parse_args()

def main():
    args = parse_args()

    # Проверка HF_TOKEN
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("Ошибка: Переменная окружения HF_TOKEN не установлена!", file=sys.stderr)
        print("Запусти: source ./load-env.sh")
        sys.exit(1)

    # Нормализация префикса
    prefix = (args.prefix or "/workspace/ComfyUI/").rstrip("/") + "/"
    print(f"PREFIX: {prefix}")

    # Создаём изменённый файл
    new_model_file = f"{args.model_file}.modified"
    with open(args.model_file, "r", encoding="utf-8") as f_in, open(new_model_file, "w", encoding="utf-8") as f_out:
        for line in f_in:
            if line.lstrip().startswith("dir="):
                leading = line[:len(line) - len(line.lstrip())]
                original_path = line.strip().split("=", 1)[1]
                new_path = f"{prefix}{original_path.lstrip('/')}"
                f_out.write(f"{leading}dir={new_path}\n")
            else:
                f_out.write(line)

    # Проверка aria2c
    if not shutil.which("aria2c"):
        print("Ошибка: aria2c не установлен или не найден в PATH.", file=sys.stderr)
        sys.exit(1)

    # Запуск aria2c
    cmd = [
        "aria2c",
        f"--input-file={new_model_file}",
        "--allow-overwrite=false",
        "--auto-file-renaming=false",
        "--continue=true",
        "--max-connection-per-server=5",
        "--conditional-get=true",
        f"--header=Authorization: Bearer {hf_token}",
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for out in proc.stdout:
        if "Redirecting to" not in out:
            print(out, end="")
    proc.wait()
    sys.exit(proc.returncode)

if __name__ == "__main__":
    main()
