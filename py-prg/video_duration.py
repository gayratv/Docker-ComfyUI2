import os
import argparse
from moviepy.video.io.VideoFileClip import VideoFileClip

'''
cd /mnt/f/_prg/python/Docker-ComfyUI/py-prg

python video_duration.py "/mnt/d/4/ИИ-Разраб 2025 [ПродСовет]/2. Промтинг GPT"

python video_duration.py "/mnt/d/4/ИИ-Разраб 2025 [ПродСовет]/2. Промтинг GPT/1"
python video_duration.py "/mnt/d/4/ИИ-Разраб 2025 [ПродСовет]/2. Промтинг GPT/2"

cd "/mnt/d/4/ИИ-Разраб 2025 [ПродСовет]/2. Промтинг GPT/1"
ffmpeg -f concat -safe 0 -i ffmpeg_list.txt -c copy "2. Промтинг GPT-part1.mp4"

cd "/mnt/d/4/ИИ-Разраб 2025 [ПродСовет]/2. Промтинг GPT/2"
ffmpeg -f concat -safe 0 -i ffmpeg_list.txt -c copy "2. Промтинг GPT-part2.mp4"

---
cd /mnt/f/_prg/python/Docker-ComfyUI/py-prg
python video_duration.py "/mnt/d/4/ИИ-Разраб 2025 [ПродСовет]/3. Курс по нейросетям для создания графики"

cd "/mnt/d/4/ИИ-Разраб 2025 [ПродСовет]/3. Курс по нейросетям для создания графики"
ffmpeg -f concat -safe 0 -i ffmpeg_list.txt -c copy "3. Курс по нейросетям для создания графики.mp4"

---
export DIR_NAME="4. МСР автоматизации"
cd /mnt/f/_prg/python/Docker-ComfyUI/py-prg
python video_duration.py "/mnt/d/4/ИИ-Разраб 2025 [ПродСовет]/$DIR_NAME"

cd "/mnt/d/4/ИИ-Разраб 2025 [ПродСовет]/$DIR_NAME"
ffmpeg -f concat -safe 0 -i ffmpeg_list.txt -c copy "$DIR_NAME.mp4"


Этот скрипт рассчитывает общую длительность всех видеофайлов в указанной папке
и создает текстовый файл со списком видео и их продолжительностью.

Как пользоваться:
1. Установите библиотеку moviepy: 

python3 -m pip install moviepy

/mnt/f/_prg/python/Docker-ComfyUI/.venv/bin/pip install --no-cache-dir --force-reinstall moviepy

'''



def format_duration(seconds):
    """
    Преобразует длительность в секундах в формат "чч:мм:сс".
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_total_duration_and_create_logs(folder_path):
    """
    Рассчитывает общую длительность и создает лог-файлы для общего отчета, YouTube и FFmpeg.
    """
    total_duration_seconds = 0
    supported_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.wmv')

    log_file_path = os.path.join(folder_path, 'video_durations.txt')
    youtube_log_path = os.path.join(folder_path, 'youtube_timestamps.txt')
    ffmpeg_list_path = os.path.join(folder_path, 'ffmpeg_list.txt')

    with open(log_file_path, 'w', encoding='utf-8') as log_file, \
            open(youtube_log_path, 'w', encoding='utf-8') as youtube_file, \
            open(ffmpeg_list_path, 'w', encoding='utf-8') as ffmpeg_file:
        log_file.write("Список видео и их длительность:\n\n")
        youtube_file.write("Таймкоды для YouTube-описания:\n\n")
        ffmpeg_file.write("# Список файлов для FFmpeg\n")

    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_extensions)]
    video_files.sort()

    for filename in video_files:
        file_path = os.path.join(folder_path, filename)
        try:
            clip = VideoFileClip(file_path)

            # Запись в файл для YouTube (накопительный итог)
            formatted_youtube_time = format_duration(total_duration_seconds)
            with open(youtube_log_path, 'a', encoding='utf-8') as youtube_file:
                youtube_file.write(f"{formatted_youtube_time} {filename}\n")

            # Запись в основной лог-файл (длительность каждого видео)
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"{format_duration(clip.duration)} | {filename}\n")

            # Запись в файл для FFmpeg (формат: file 'имя_файла.mp4')
            with open(ffmpeg_list_path, 'a', encoding='utf-8') as ffmpeg_file:
                # Относительный путь, чтобы не зависеть от папки
                relative_path = os.path.basename(file_path)
                ffmpeg_file.write(f"file '{relative_path}'\n")

            total_duration_seconds += clip.duration

            clip.close()
        except Exception as e:
            print(f"Не удалось обработать файл {filename}: {e}")

    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n--- Общая длительность: {format_duration(total_duration_seconds)} ---")

    return total_duration_seconds


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Рассчитывает общую длительность видео в папке и создает лог.")
    parser.add_argument("folder_path", help="Путь к папке с видео")

    args = parser.parse_args()

    if not os.path.isdir(args.folder_path):
        print(f"Ошибка: Папка не найдена по пути '{args.folder_path}'")
    else:
        print("Обработка видеофайлов...")
        total_seconds = get_total_duration_and_create_logs(args.folder_path)
        print(f"Общая длительность всех видео: {format_duration(total_seconds)}")
        print(
            f"Подробные отчеты созданы в файлах 'video_durations.txt', 'youtube_timestamps.txt' и 'ffmpeg_list.txt' в папке: {args.folder_path}")