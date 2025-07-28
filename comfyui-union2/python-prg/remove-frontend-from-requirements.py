#!/usr/bin/env python3
"""
Скрипт перемещает (переименовывает) файл requirements.txt → requirements.in
и формирует новый requirements.txt, исключив строки, чьи префиксы указаны
в списке `BAD_PREFIXES`.
"""

import os
from pathlib import Path
import sys

# ──────────────────────────────────────────────
# Настройки (можно править под себя)
BAD_PREFIXES = ['comfyui-frontend-package']      # строки, начинающиеся с этих префиксов, удаляем
SRC_NAME     = 'requirements.txt'  # исходный файл
DST_NAME_IN  = 'requirements.in'   # куда переименовываем исходник
NEW_NAME_TXT = 'requirements.txt'  # новый выходной файл
# ──────────────────────────────────────────────


def main(directory: Path) -> None:
    """Основная логика скрипта."""
    src_path = directory / SRC_NAME
    in_path  = directory / DST_NAME_IN
    out_path = directory / NEW_NAME_TXT

    # 1. Проверяем, что исходный файл существует
    if not src_path.exists():
        sys.exit(f'Файл {src_path} не найден.')

    # 2. Переименовываем (moves) requirements.txt → requirements.in
    src_path.rename(in_path)

    # 3. Фильтруем строки и пишем новый requirements.txt
    with in_path.open('r', encoding='utf-8') as fin, \
         out_path.open('w', encoding='utf-8') as fout:

        for raw_line in fin:
            line = raw_line.lstrip()          # игнорируем ведущие пробелы при проверке
            if any(line.startswith(p) for p in BAD_PREFIXES):
                continue                      # пропускаем «запрещённую» строку
            fout.write(raw_line)              # сохраняем в выходной файл

    print(f'Готово! Создан {out_path.name}, исходник перемещён в {in_path.name}.')


if __name__ == '__main__':
    # Скрипт запускается из той же директории, где лежит requirements.txt
    # либо передайте путь к папке в качестве аргумента.
    workdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    main(workdir)
