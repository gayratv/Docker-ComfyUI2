'''


cd /mnt/f/_prg/python/Docker-ComfyUI/py-prg/rename-files
FOLDER="/mnt/d/4/Тотальный курс по картинкам в нейросетях 2.0 [Дмитрий Зверев]/13. Нейрофото"
D:\4\Нейрограф 2005 июль
FOLDER="/mnt/d/4/Нейрограф 2005 июль"
python3 ren-subdir.py "$FOLDER" --prefix "Нейрограф 2025-07"

FOLDER="/mnt/d/4/1/ОРИГИНАЛ"
python3 ren-subdir.py "$FOLDER" --prefix "Cursor"

'''

import os
import argparse

def rename_nested_files(parent_folder, prefix="13"):
    for subdir in os.listdir(parent_folder):
        subdir_path = os.path.join(parent_folder, subdir)
        if os.path.isdir(subdir_path):
            for filename in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, filename)

                if os.path.isfile(file_path):
                    # Формируем новое имя файла
                    new_name = f"{prefix}. {subdir}. {filename}"
                    new_path = os.path.join(subdir_path, new_name)

                    try:
                        os.rename(file_path, new_path)
                        print(f"✅ {filename} -> {new_name}")
                    except Exception as e:
                        print(f"❌ Ошибка при переименовании {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Переименование файлов в поддиректориях с произвольным префиксом.")
    parser.add_argument("parent_folder", help="Путь к папке, содержащей поддиректории.")
    parser.add_argument("--prefix", default="13", help="Строка-префикс (например, 'нейрофото').")

    args = parser.parse_args()

    if not os.path.isdir(args.parent_folder):
        print(f"❌ Папка не найдена: {args.parent_folder}")
    else:
        rename_nested_files(args.parent_folder, args.prefix)
