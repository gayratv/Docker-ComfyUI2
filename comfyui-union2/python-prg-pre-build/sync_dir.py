# cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/python-prg
# python3 sync_dir.py "clarity-upscale"
# python3 sync_dir.py "FluxKontext"

import os
import shutil
import argparse
from tqdm import tqdm  # Импортируем библиотеку для progress bar

# --- 1. КОНФИГУРАЦИЯ ---
# Укажите здесь пути к вашим реальным директориям.
PERMANENT_DIR = "/mnt/d/ComfyUI-data"  # Постоянная директория
TEMP_DIR = "/mnt/h/ComfyUI-data"  # Временная директория
# Основная директория, в которой лежат поддиректории с конфигурационными файлами
BASE_TEMPLATE_DIR = "/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/aria2/templates/models"


def process_model_configs(config_path, permanent_root, temp_root, display_path):
    """
    Анализирует один конфигурационный файл и копирует существующие модели
    из постоянной директории во временную.
    """
    print(f"--- Обработка файла: {display_path} ---")

    # --- ЭТАП 1: ЧТЕНИЕ И ОЧИСТКА ФАЙЛА ---
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл конфигурации не найден по пути: {config_path}")
        return

    # Используем цикл for для очистки комментариев и пустых строк
    cleaned_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith('#'):
            cleaned_lines.append(stripped_line)

    print(f"После очистки в файле осталось {len(cleaned_lines)} значащих строк.")

    # --- ЭТАП 2: ОСНОВНАЯ ОБРАБОТКА БЛОКАМИ ---
    if len(cleaned_lines) % 3 != 0:
        print("⚠️ Предупреждение: Количество значащих строк не кратно 3. Возможен неверный формат файла.")

    copied_files_count = 0
    checked_files_count = 0

    # Обрабатываем очищенные строки блоками по 3
    for i in range(0, len(cleaned_lines) // 3 * 3, 3):
        url_line = cleaned_lines[i]
        line_A = cleaned_lines[i + 1]
        line_B = cleaned_lines[i + 2]

        dir_line = None
        out_line = None

        # Определяем, какая строка 'dir', а какая 'out'
        if line_A.startswith('dir=') and line_B.startswith('out='):
            dir_line = line_A
            out_line = line_B
        elif line_A.startswith('out=') and line_B.startswith('dir='):
            out_line = line_A
            dir_line = line_B
        else:
            print(
                f"❌ Ошибка формата в блоке для URL '{url_line}'. 'dir' и 'out' не найдены или в неверном формате. Пропуск блока.")
            continue

        # Извлекаем значения
        try:
            dir_val = dir_line.split('=', 1)[1].strip()
            out_val = out_line.split('=', 1)[1].strip()
        except IndexError:
            print(f"❌ Ошибка извлечения значения в блоке для URL '{url_line}'. Пропуск блока.")
            continue

        checked_files_count += 1
        print(f"Найдена запись: dir='{dir_val}', out='{out_val}'")

        source_file_path = os.path.join(permanent_root, dir_val, out_val)

        if os.path.exists(source_file_path):
            dest_file_path = os.path.join(temp_root, dir_val, out_val)

            copy_needed = False
            source_size = os.path.getsize(source_file_path)

            if os.path.exists(dest_file_path):
                dest_size = os.path.getsize(dest_file_path)
                if source_size == dest_size:
                    print(f"  -> ⏩ Файл уже существует и размеры совпадают (пропуск).")
                else:
                    # Используем 1000**3 для GB
                    source_size_gb = source_size / (1000 ** 3)
                    dest_size_gb = dest_size / (1000 ** 3)
                    print(
                        f"  -> ⚠️  Размеры файлов не совпадают. Исходный: {source_size_gb:.2f} GB, целевой: {dest_size_gb:.2f} GB. Перезапись...")
                    copy_needed = True
            else:
                copy_needed = True

            if copy_needed:
                dest_dir = os.path.dirname(dest_file_path)

                # --- ИЗМЕНЕНИЕ ЗДЕСЬ: Создаем директории по одной для надежности ---
                path_to_create = os.path.relpath(dest_dir, temp_root)
                current_path = temp_root
                all_dirs_created = True

                for part in path_to_create.split(os.path.sep):
                    current_path = os.path.join(current_path, part)
                    if not os.path.exists(current_path):
                        try:
                            os.mkdir(current_path)
                        except Exception as e:
                            print(f"  -> ❌ КРИТИЧЕСКАЯ ОШИБКА при создании директории: {current_path}")
                            print(
                                f"  -> Проверьте, что родительская директория '{os.path.dirname(current_path)}' существует и доступна для записи.")
                            print(f"  -> Системная ошибка: {e}")
                            all_dirs_created = False
                            break  # Прекращаем попытки создать дочерние директории

                if not all_dirs_created:
                    continue  # Пропускаем текущий файл и переходим к следующему

                # Используем 1000**3 для GB
                file_size_gb = source_size / (1000 ** 3)

                print(f"  -> ✅ Файл найден: '{os.path.abspath(source_file_path)}' ({file_size_gb:.2f} GB)")
                print(f"  -> 📥 Копирование в: '{os.path.abspath(dest_file_path)}'")

                # Копирование файла с progress bar
                chunk_size = 10 * 1024 * 1024  # 10MB
                try:
                    with open(source_file_path, 'rb') as fsrc, \
                            open(dest_file_path, 'wb') as fdst, \
                            tqdm(total=source_size, unit='B', unit_scale=True,
                                 desc=os.path.basename(dest_file_path)) as pbar:
                        while True:
                            chunk = fsrc.read(chunk_size)
                            if not chunk:
                                break
                            fdst.write(chunk)
                            pbar.update(len(chunk))

                    # Копируем метаданные (права доступа, время изменения)
                    shutil.copystat(source_file_path, dest_file_path)
                    copied_files_count += 1
                except Exception as e:
                    print(f"  -> ❌ Ошибка при копировании файла: {e}")

        else:
            print(f"  -> 💨 Файл не найден (пропуск): '{os.path.abspath(source_file_path)}'")
        print("-" * 25)

    print(f"Проверено записей: {checked_files_count}, скопировано файлов: {copied_files_count}")
    print("-" * 50 + "\n")


def main():
    """
    Главная функция для запуска скрипта.
    """
    # Проверка существования базовых директорий
    if not os.path.isdir(PERMANENT_DIR):
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: Постоянная директория не найдена по пути: {PERMANENT_DIR}")
        print("Пожалуйста, проверьте путь в переменной PERMANENT_DIR в скрипте.")
        return

    if not os.path.isdir(TEMP_DIR):
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: Временная директория не найдена по пути: {TEMP_DIR}")
        print("Пожалуйста, проверьте путь в переменной TEMP_DIR или создайте эту директорию.")
        return

    parser = argparse.ArgumentParser(
        description="Синхронизирует файлы моделей на основе конфигурационных файлов hf.txt и civitay.txt в указанной поддиректории.")
    parser.add_argument("subdirectory", nargs='?', default="clarity-upscale",
                        help="Имя поддиректории в 'templates/models' для поиска конфигурационных файлов.")
    args = parser.parse_args()

    # Формируем полный путь к директории с конфигами
    target_dir = os.path.join(BASE_TEMPLATE_DIR, args.subdirectory)

    if not os.path.isdir(target_dir):
        print(f"❌ Ошибка: Директория не найдена по пути: {target_dir}")
        return

    print(f"Целевая директория: {target_dir}\n")

    # Имена файлов, которые нужно найти и обработать
    config_filenames_to_process = ["hf.txt", "civitay.txt"]

    processed_any_file = False
    for filename in config_filenames_to_process:
        config_path = os.path.join(target_dir, filename)
        if os.path.exists(config_path):
            # Формируем относительный путь для отображения
            display_path = os.path.join(args.subdirectory, filename)
            # Вызываем основную функцию для каждого найденного файла
            process_model_configs(config_path, PERMANENT_DIR, TEMP_DIR, display_path)
            processed_any_file = True

    if not processed_any_file:
        print("Не найдено ни одного конфигурационного файла (hf.txt, civitay.txt) для обработки.")


if __name__ == "__main__":
    main()
