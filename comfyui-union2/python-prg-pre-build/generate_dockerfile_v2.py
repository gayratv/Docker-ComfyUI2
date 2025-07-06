import os
import sys
import argparse

# Глобальная константа для базового пути
BASE_DOCKERFILE_PATH = '/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2'


def create_new_dockerfile(start_file, nodes_file, end_file, output_file):
    """
    Собирает новый Dockerfile из трех частей:
    1. Начальная часть из start_file.
    2. Сгенерированная часть на основе nodes_file.
    3. Конечная часть из end_file.

    Args:
        start_file (str): Путь к файлу с началом Dockerfile.
        nodes_file (str): Путь к файлу со списком git-репозиториев.
        end_file (str): Путь к файлу с концом Dockerfile.
        output_file (str): Путь для записи итогового Dockerfile.
    """
    dockerfile_content = []

    # 1. Чтение начального файла
    try:
        with open(start_file, 'r', encoding='utf-8') as f:
            dockerfile_content.append(f.read())
    except FileNotFoundError:
        print(f"Ошибка: Не удалось найти начальный файл '{start_file}'", file=sys.stderr)
        sys.exit(1)

    # 2. Генерация средней части на основе списка репозиториев
    try:
        with open(nodes_file, 'r', encoding='utf-8') as f:
            # Читаем строки, убираем пробелы, отфильтровываем пустые и закомментированные
            repositories = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    except FileNotFoundError:
        print(f"Ошибка: Не удалось найти файл с узлами '{nodes_file}'", file=sys.stderr)
        sys.exit(1)

    generated_part = []
    for repo in repositories:
        # Формируем команду RUN для каждого репозитория
        # Использование f-string и многострочного формата делает команду читаемой
        run_command = (
            "RUN --mount=type=cache,target=/root/repo-cache \\\n"
            "    --mount=type=cache,target=/root/pip-cache \\\n"
            "    PIP_CACHE_DIR=/root/pip-cache \\\n"
            f"    process_one_repo_install_req_hash.sh \"{repo}\" true \\\n"
            "    && rm -rf /root/.cache/pip"
        )
        generated_part.append(run_command)

    # Добавляем сгенерированную часть в общий контент
    dockerfile_content.append('\n\n'.join(generated_part))

    # 3. Чтение конечного файла
    try:
        with open(end_file, 'r', encoding='utf-8') as f:
            dockerfile_content.append(f.read())
    except FileNotFoundError:
        print(f"Ошибка: Не удалось найти конечный файл '{end_file}'", file=sys.stderr)
        sys.exit(1)

    # 4. Запись итогового файла
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # Соединяем все три части (начало, середина, конец) двойным переносом строки
            f.write('\n\n'.join(dockerfile_content))
        print(f"Успешно сгенерирован файл: '{output_file}'")
    except IOError as e:
        print(f"Ошибка при записи в файл '{output_file}': {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Главная функция для парсинга аргументов командной строки и запуска генератора.
    """
    parser = argparse.ArgumentParser(
        description=f"Генератор Dockerfile из частей. Базовый каталог: {BASE_DOCKERFILE_PATH}",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '--start',
        default='Dockerfile_start',
        help='Имя файла с начальной частью Dockerfile.\n(default: %(default)s)'
    )
    parser.add_argument(
        '--nodes',
        default='nodes1.txt',
        help='Имя файла со списком git-репозиториев.\n(default: %(default)s)'
    )
    parser.add_argument(
        '--end',
        default='Dockerfile_end',
        help='Имя файла с конечной частью Dockerfile.\n(default: %(default)s)'
    )
    parser.add_argument(
        '--output',
        default='Dockerfile.generated',
        help='Имя итогового сгенерированного файла.\n(default: %(default)s)'
    )

    args = parser.parse_args()

    # Формируем полные пути, добавляя базовый путь к каждому аргументу.
    # os.path.join корректно обработает, если в аргументе будет передан абсолютный путь.
    start_file_path = os.path.join(BASE_DOCKERFILE_PATH, args.start)
    nodes_file_path = os.path.join(BASE_DOCKERFILE_PATH, 'custom-nodes', args.nodes)
    end_file_path = os.path.join(BASE_DOCKERFILE_PATH, args.end)
    output_file_path = os.path.join(BASE_DOCKERFILE_PATH, args.output)

    create_new_dockerfile(start_file_path, nodes_file_path, end_file_path, output_file_path)


if __name__ == '__main__':
    main()
