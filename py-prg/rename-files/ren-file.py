'''


cd /mnt/f/_prg/python/Docker-ComfyUI/py-prg/rename-files
FOLDER="/mnt/d/4/Тотальный курс по картинкам в нейросетях 2.0 [Дмитрий Зверев]/3. Создание картинок в нейросети Midjourney - часть 2"
FOLDER="/mnt/d/4/Тотальный курс по картинкам в нейросетях 2.0 [Дмитрий Зверев]/2. Создание картинок в нейросети Midjourney - часть 1"
FOLDER="/mnt/d/4/Тотальный курс по картинкам в нейросетях 2.0 [Дмитрий Зверев]/7. Генерация картинок через ChatGPT и Sora"
FOLDER="/mnt/d/4/Тотальный курс по картинкам в нейросетях 2.0 [Дмитрий Зверев]/10. Playground и Lexica"
python3 ren-file.py "$FOLDER" --prefix 10

'''
import os
import re
import argparse

def rename_files(folder_path, new_prefix="2"):
    files = os.listdir(folder_path)

    for file in files:
        match = re.match(r"^(\d+)\.(.*)", file)
        if match:
            old_number = match.group(1)
            rest_of_name = match.group(2)
            new_name = f"{new_prefix}.{old_number}.{rest_of_name}"
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, new_name)

            try:
                os.rename(old_path, new_path)
                print(f"✅ Переименован: {file} -> {new_name}")
            except Exception as e:
                print(f"❌ Ошибка при переименовании {file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Переименование файлов с добавлением нового префикса.")
    parser.add_argument("folder_path", help="Путь к папке с файлами.")
    parser.add_argument("--prefix", default="2", help="Новый префикс (по умолчанию: 2).")

    args = parser.parse_args()

    if not os.path.isdir(args.folder_path):
        print(f"❌ Папка не найдена: {args.folder_path}")
    else:
        rename_files(args.folder_path, args.prefix)
