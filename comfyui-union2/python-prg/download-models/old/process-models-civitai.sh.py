#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для постобработки списка ссылок на модели Civitai.

Как работает:
1. Принимает путь к входному текстовому файлу как аргумент командной строки.
2. Если указан параметр -o/--output, результат сохраняется в этот файл.
   Иначе имя формируется автоматически: к имени входного файла (без расширения)
   добавляется суффикс "-token.txt".
3. Читает файл построчно:
   - Если строка начинается с http:// или https:// — удаляет завершающий \r (если есть)
     и добавляет в конец ссылки параметр &token=<CIVITAI_TOKEN>, где CIVITAI_TOKEN —
     переменная окружения.
   - Если строка не является ссылкой, записывает её без изменений.
4. Записывает результат в новый файл, перезаписывая его, если он существует.

Пример:
$ export CIVITAI_TOKEN=abcdef12345
$ python3 process_models.py models.txt
→ создаст models-token.txt с добавленными токенами в ссылки.
"""

import argparse
import os
import re
import sys
from pathlib import Path

def abort(message: str) -> None:
    """Выводит сообщение об ошибке и завершает работу с кодом 1."""
    print(f"Ошибка: {message}", file=sys.stderr)
    sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Добавляет &token=$CIVITAI_TOKEN к ссылкам в файле."
    )
    parser.add_argument("input_file", help="Путь к входному файлу")
    parser.add_argument(
        "-o", "--output",
        help="Путь к выходному файлу (по умолчанию: <input>-token.txt)"
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        abort("Входной файл не найден.")

    if not input_path.is_file():
        abort("Указанный путь не является файлом.")

    # Формируем имя выходного файла: <имя_без_расширения>-token.txt
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_name(f"{input_path.stem}-token.txt")

    civitai_token = os.environ.get("CIVITAI_TOKEN")
    if not civitai_token:
        abort("Переменная окружения CIVITAI_TOKEN не установлена.")

    url_re = re.compile(r"^https?://", re.IGNORECASE)

    try:
        with input_path.open("r", encoding="utf-8", errors="replace") as fin, \
             output_path.open("w", encoding="utf-8") as fout:

            for raw in fin:
                # strip() удаляет:
                #     пробелы
                #     табуляции(\t)
                #     переводы строк(\n, \r, \r\n)
                #     другие невидимые символы пробельного типа
                line = raw.strip()  # убираем только \n
                if url_re.match(line):
                    line = line.rstrip("\r")  # удаляем \r, если есть
                    fout.write(f"{line}&token={civitai_token}\n")
                else:
                    fout.write(f"{line}\n")
    except OSError as e:
        abort(f"Ошибка при работе с файлами: {e}")

    print(f"Результат записан в файл: {output_path}")

if __name__ == "__main__":
    main()
