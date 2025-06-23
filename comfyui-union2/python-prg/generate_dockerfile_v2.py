import os

def create_new_dockerfile(
    start_file='Dockerfile_start',
    nodes_file='nodes1.txt',
    end_file='Dockerfile_end',
    output_file='Dockerfile.generated'
):
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
        with open(start_file, 'r') as f:
            dockerfile_content.append(f.read())
    except FileNotFoundError:
        print(f"Ошибка: файл '{start_file}' не найден.")
        return

    # 2. Генерация средней части
    try:
        with open(nodes_file, 'r') as f:
            repositories = [line for line in f.read().strip().split('\n') if line]
    except FileNotFoundError:
        print(f"Ошибка: файл '{nodes_file}' не найден.")
        return

    generated_part = []
    for repo in repositories:
        run_command = (
            "RUN --mount=type=cache,target=/root/repo-cache \\\n"
            "    --mount=type=cache,target=/root/pip-cache \\\n"
            "    PIP_CACHE_DIR=/root/pip-cache \\\n"
            f"    process_repos-install-req-hash.sh \"{repo}\" true \\\n"
            "    && rm -rf /root/.cache/pip"
        )
        generated_part.append(run_command)

    dockerfile_content.append('\n\n'.join(generated_part))

    # 3. Чтение конечного файла
    try:
        with open(end_file, 'r') as f:
            dockerfile_content.append(f.read())
    except FileNotFoundError:
        print(f"Ошибка: файл '{end_file}' не найден.")
        return

    # Запись итогового файла
    with open(output_file, 'w') as f:
        f.write('\n\n'.join(dockerfile_content))
    print(f"Успешно сгенерирован '{output_file}'")


if __name__ == '__main__':
    # --- Демонстрация ---
    # Для примера, создадим все необходимые файлы.
    # В реальном сценарии вы создадите эти файлы самостоятельно.

    print("Создание демонстрационных файлов: Dockerfile_start, nodes1.txt, Dockerfile_end")

    # Содержимое Dockerfile_start
    dockerfile_start_content = """FROM 127.0.0.1:5000/comfyui:latest

# setup comfyui
COPY --chown=1000:1000 comfyui-union2/ /tmp/comfyui-union2/
RUN --mount=type=cache,target=/root/.cache/pip \\
    pip install -r /tmp/comfyui-union2/requirements.txt \\
    && rm -rf /root/.cache/pip

# copy scripts and make them executable
COPY --chown=1000:1000 comfyui-union2/process_repos-install-req-hash.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/process_repos-install-req-hash.sh

# copy custom nodes list
COPY --chown=1000:1000 comfyui-union2/nodes1.txt /tmp/nodes1.txt

WORKDIR /opt/ComfyUI"""
    with open('Dockerfile_start', 'w') as f:
        f.write(dockerfile_start_content)

    # Содержимое nodes1.txt
    nodes_content = """https://github.com/ltdrdata/ComfyUI-Manager
https://github.com/AlekPet/ComfyUI_Custom_Nodes_AlekPet
https://github.com/BlenderNeko/ComfyUI_Noise
https://github.com/LEv145/images-grid-comfy-plugin"""
    with open('nodes1.txt', 'w') as f:
        f.write(nodes_content)

    # Содержимое Dockerfile_end
    dockerfile_end_content = """# Final setup
RUN rm -f /tmp/nodes1.txt"""
    with open('Dockerfile_end', 'w') as f:
        f.write(dockerfile_end_content)

    print("\\nЗапуск скрипта генерации...")
    create_new_dockerfile()

    # Вывод результата
    print(f"\\n--- Содержимое итогового файла 'Dockerfile.generated': ---")
    with open('Dockerfile.generated', 'r') as f:
        print(f.read())