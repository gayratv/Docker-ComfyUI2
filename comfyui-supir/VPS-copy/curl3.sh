#!/bin/bash

#set -x

# Получаем директорию, где находится текущий скрипт
SCRIPT_DIR=$(dirname "$(realpath "$BASH_SOURCE")")

# Загружаем переменные из .env, если файл существует в той же директории
if [ -f "$SCRIPT_DIR/.env" ]; then
    source "$SCRIPT_DIR/.env"
else
    echo "Файл .env не найден! Создайте его и укажите токены."
    exit 1
fi

download_file_curl() {
    local directory="$1"
    local url="$2"

    echo "Директория: $directory"
    echo "URL: $url"

    # Определяем заголовок авторизации
    local auth_header=""
    if [[ "$url" == *"huggingface.co"* ]]; then
        auth_header="-H \"Authorization: Bearer $HF_TOKEN\""
    elif [[ "$url" == *"civitai.com"* ]]; then
        auth_header="-H \"Authorization: Bearer $CIVITAI_TOKEN\""
    fi


    mkdir -p "$directory"

#    eval curl -L -J --progress-bar $auth_header --output-dir "$directory" -O "$url"
    eval curl -L -J -s $auth_header --output-dir "$directory" -O "$url" &

    echo "Загрузка запущена."

}

# если вызывается как функция то закомментировать
# download_file_curl "$1" "$2"

# Пример вызова функции
# civitai
# ./curl3.sh "/mnt/f/_prg/python/Docker-test/download-test/download-test" "https://civitai.com/api/download/models/355900?type=Model&format=SafeTensor&size=full&fp=fp16"
# huggingface
# ./curl3.sh "/mnt/f/_prg/python/Docker-test/download-test/download-test" "https://huggingface.co/black-forest-labs/FLUX.1-Depth-dev/resolve/main/flux1-depth-dev.safetensors"



