#!/usr/bin/env python3
"""
Скрипт для удаления поддиректорий в /workspace/aria2/templates/models,
кроме указанных в параметрах командной строки.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path


def cleanup_directories(base_path, keep_dirs):
    """
    Удаляет все поддиректории в base_path, кроме указанных в keep_dirs.

    Args:
        base_path (str): Путь к базовой директории
        keep_dirs (list): Список названий директорий, которые нужно оставить
    """
    base_path = Path(base_path)

    # Проверяем существование базовой директории
    if not base_path.exists():
        print(f"Ошибка: директория {base_path} не существует")
        return False

    if not base_path.is_dir():
        print(f"Ошибка: {base_path} не является директорией")
        return False

    # Получаем все поддиректории
    subdirs = [d for d in base_path.iterdir() if d.is_dir()]

    # Счетчики для статистики
    deleted_count = 0
    kept_count = 0

    print(f"Найдено {len(subdirs)} поддиректорий в {base_path}")
    print(f"Будут сохранены: {', '.join(keep_dirs) if keep_dirs else 'нет'}")
    print("-" * 50)

    # Обрабатываем каждую поддиректорию
    for subdir in subdirs:
        dir_name = subdir.name

        if dir_name in keep_dirs:
            print(f"✓ Сохранено: {dir_name}")
            kept_count += 1
        else:
            try:
                shutil.rmtree(subdir)
                print(f"✗ Удалено: {dir_name}")
                deleted_count += 1
            except Exception as e:
                print(f"⚠ Ошибка при удалении {dir_name}: {e}")

    print("-" * 50)
    print(f"Итого: удалено {deleted_count}, сохранено {kept_count}")

    return True


def main():
    """Главная функция программы."""
    parser = argparse.ArgumentParser(
        description="Удаляет все поддиректории в указанной директории, кроме перечисленных"
    )

    parser.add_argument(
        "keep_dirs",
        nargs="*",
        help="Названия директорий, которые нужно сохранить"
    )

    parser.add_argument(
        "--path",
        default="/workspace/aria2/templates/models",
        help="Путь к директории (по умолчанию: /workspace/aria2/templates/models)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Показать, что будет удалено, без фактического удаления"
    )

    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Запросить подтверждение перед удалением"
    )

    args = parser.parse_args()

    # Если указан режим dry-run
    if args.dry_run:
        print("=== РЕЖИМ ПРОВЕРКИ (без удаления) ===")
        base_path = Path(args.path)
        if base_path.exists() and base_path.is_dir():
            subdirs = [d.name for d in base_path.iterdir() if d.is_dir()]
            print(f"\nВсе поддиректории в {args.path}:")
            for d in sorted(subdirs):
                status = "✓ будет сохранена" if d in args.keep_dirs else "✗ будет удалена"
                print(f"  {d} - {status}")
        else:
            print(f"Директория {args.path} не найдена")
        return

    # Запрос подтверждения, если указан флаг
    if args.confirm:
        response = input(f"\nВы уверены, что хотите удалить поддиректории в {args.path}? (y/N): ")
        if response.lower() != 'y':
            print("Операция отменена")
            return

    # Выполняем очистку
    success = cleanup_directories(args.path, args.keep_dirs)

    # Возвращаем код выхода
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()