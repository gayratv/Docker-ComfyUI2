import os
import argparse
import subprocess
import shutil  # Добавлен импорт shutil
from moviepy.video.io.VideoFileClip import VideoFileClip


def format_duration(seconds):
    """
    Преобразует длительность в секундах в формат "чч:мм:сс".
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def get_max_resolution(folder_path, video_files):
    """
    Определяет максимальное разрешение среди всех видеофайлов.
    """
    max_width, max_height = 0, 0
    for filename in video_files:
        file_path = os.path.join(folder_path, filename)
        try:
            clip = VideoFileClip(file_path)
            if clip.size[0] > max_width:
                max_width = clip.size[0]
            if clip.size[1] > max_height:
                max_height = clip.size[1]
            clip.close()
        except Exception as e:
            print(f"Не удалось определить разрешение для {filename}: {e}")
    return max_width, max_height


def process_videos(folder_path):
    """
    Основная функция для обработки видео.
    """
    supported_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.wmv')

    log_file_path = os.path.join(folder_path, 'video_durations.txt')
    youtube_log_path = os.path.join(folder_path, 'youtube_timestamps.txt')

    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_extensions)]
    video_files.sort()

    if not video_files:
        print("В папке не найдено ни одного видеофайла. Процесс остановлен.")
        return

    max_width, max_height = get_max_resolution(folder_path, video_files)
    print(f"\nОбнаружено максимальное разрешение: {max_width}x{max_height}")

    transcoded_dir = os.path.join(folder_path, "_transcoded_videos")
    list_file_name = "ffmpeg_list.txt"
    output_file_name = f"{os.path.basename(os.path.normpath(folder_path))}.mp4"

    if os.path.exists(transcoded_dir):
        print("Удаление старой временной папки...")
        shutil.rmtree(transcoded_dir)
    os.makedirs(transcoded_dir)
    print(f"Создана временная папка: {transcoded_dir}\n")

    transcoded_files_list = []
    total_duration_seconds = 0.0

    with open(log_file_path, 'w', encoding='utf-8') as log_file, \
            open(youtube_log_path, 'w', encoding='utf-8') as youtube_file:
        log_file.write("Список видео и их длительность:\n\n")
        youtube_file.write("Таймкоды для YouTube-описания:\n\n")

    for i, filename in enumerate(video_files):
        print(f"  \033[1;34mОбработка файла {i + 1}/{len(video_files)}:\033[0m {filename}")

        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(transcoded_dir, filename)

        command = [
            "ffmpeg",
            "-i", input_path,
            "-vf",
            f"scale={max_width}:{max_height}:force_original_aspect_ratio=decrease,pad={max_width}:{max_height}:(ow-iw)/2:(oh-ih)/2,setsar=1:1,format=yuv420p",
            "-c:v", "h264_nvenc",
            "-r", "30",  # <--- NEW: Установлена постоянная частота кадров 30 FPS
            "-c:a", "aac",
            "-b:a", "192k",
            "-vsync", "2",
            "-preset", "fast",
            "-crf", "23",
            "-stats",
            "-y", output_path
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

            clip = VideoFileClip(input_path)
            formatted_youtube_time = format_duration(total_duration_seconds)
            with open(youtube_log_path, 'a', encoding='utf-8') as f:
                f.write(f"{formatted_youtube_time} {filename}\n")
            with open(log_file_path, 'a', encoding='utf-8') as f:
                f.write(f"{format_duration(clip.duration)} | {filename}\n")
            total_duration_seconds += clip.duration
            clip.close()

            transcoded_files_list.append(output_path)

        except subprocess.CalledProcessError as e:
            print(f"  \033[1;31mОшибка транскодирования файла {filename}:\033[0m")
            print(e.output.decode())
            return

    print("\nСоздание списка для объединения...")
    with open(os.path.join(folder_path, list_file_name), 'w', encoding='utf-8') as f:
        for file_path in transcoded_files_list:
            f.write(f"file '{file_path}'\n")

    print("\033[1;34mОбъединение видео...\033[0m")
    concat_command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", os.path.join(folder_path, list_file_name),
        "-c", "copy",
        "-vsync", "2",
        "-stats",
        "-y", os.path.join(folder_path, output_file_name)
    ]

    try:
        subprocess.run(concat_command, check=True)
    except subprocess.CalledProcessError as e:
        print("\033[1;31mОшибка объединения файлов:\033[0m")
        print(e.output.decode())
        return

    print(f"\n\033[1;32mГотово! Объединенный файл '{output_file_name}' создан.\033[0m")

    # === ИЗМЕНЕНИЕ ===
    # Команды удаления временной папки и файла-списка удалены.
    # Добавлено информационное сообщение.
    print(f"\nВременная папка '{transcoded_dir}' и файл-список '{list_file_name}' сохранены.")
    print("Вы можете удалить их вручную, когда они больше не понадобятся.")

    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(f"\n--- Общая длительность: {format_duration(total_duration_seconds)} ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Рассчитывает общую длительность видео в папке и создает лог.")
    parser.add_argument("folder_path", help="Путь к папке с видео")

    args = parser.parse_args()

    if not os.path.isdir(args.folder_path):
        print(f"Ошибка: Папка не найдена по пути '{args.folder_path}'")
    else:
        print("\033[1;34mНачинаю работу. Пожалуйста, подождите...\033[0m")
        process_videos(args.folder_path)
