#!/bin/bash

# Установка базовой директории
BASE_INSTALL_DIR="/workspace/ComfyUI/custom_nodes/"
#BASE_INSTALL_DIR="/mnt/d/test-pip/ComfyUI/custom_nodes/"


# Получение файла со списком репозиториев из аргумента или установка значения по умолчанию
NODES_FILE="${1:-nodes.txt}"

#echo "DEBUG: Checking for file at path: $NODES_FILE"
#ls -l "$NODES_FILE"
# echo -e "\n\033[34mDEBUG\033[0m: =======NODES_FILE = $NODES_FILE\n"

# Проверка наличия файла nodes.txt
if [ ! -f "$NODES_FILE" ]; then
    echo "ERROR: $NODES_FILE not found. Create the file and add repository URLs."
    exit 1
fi

# Чтение списка репозиториев из файла
#NODES_FILE="nodes-nunchaku.txt"
mapfile -t INSTALL_DATA < <(
    sed '
        s/^[[:space:]]*//;      # удалить начальные пробелы
        s/[[:space:]]*$//;      # удалить концевые пробелы
        /^$/d;                  # удалить пустые строки
        /^#/d                   # удалить комментарии
    ' "$NODES_FILE"
)



echo "DEBUG: Processing the following repositories from $NODES_FILE:"
for GIT_REPO in "${INSTALL_DATA[@]}"; do
    echo "DEBUG: $GIT_REPO"

    # Определение директории установки
    INSTALL_DIR="$BASE_INSTALL_DIR"

    echo "DEBUG: Using INSTALL_DIR: $INSTALL_DIR"
    echo -e "\e[1;31mDEBUG: Extracted GIT_REPO: $GIT_REPO\e[0m"

    # Проверка, что GIT_REPO не пустой
    if [ -z "$GIT_REPO" ]; then
        echo "ERROR: Invalid repository URL: $GIT_REPO"
        exit 1
    fi

    # Создание директории, если она не существует
    mkdir -p "$INSTALL_DIR"

    # Переход в директорию установки
    cd "$INSTALL_DIR" || { echo "ERROR: Failed to change directory to $INSTALL_DIR"; exit 1; }

    # Клонирование репозитория
    echo "DEBUG: Cloning repository $GIT_REPO into $INSTALL_DIR..."

    REPO_NAME=$(basename "$GIT_REPO" .git | sed 's/\r$//')
    echo -e "\e[1;31mDEBUG: repo name: $REPO_NAME\e[0m"

    # Проверяем, есть ли уже склонированный репозиторий в кэше
    if [ -d "/root/repo-cache/$REPO_NAME" ]; then
        echo -e "\e[1;34mINFO: copy from cache\e[0m"
        mkdir -p "/root/repo-cache/$REPO_NAME"
        cp -r "/root/repo-cache/$REPO_NAME" "./$REPO_NAME"
    else
        git clone --recurse-submodules "$GIT_REPO"
        echo "DEBUG: Checking if /root/repo-cache exists..."
        ls -la /root/repo-cache
        echo -e "\e[1;31mDEBUG: Caching repository to /root/repo-cache/$REPO_NAME...\e[0m"
        cp -r "./$REPO_NAME" "/root/repo-cache/$REPO_NAME"
        echo "DEBUG: Copied $REPO_NAME to /root/repo-cache"
        ls -la /root/repo-cache
    fi

    # Переход во вновь созданную директорию
    # Извлекаем имя директории из URL репозитория
    REPO_DIR=$(basename "$GIT_REPO" .git | sed 's/\r$//')
    echo "DEBUG: Cloned repository directory: $REPO_DIR"

    cd "$REPO_DIR" || { echo "ERROR: Failed to change directory to $REPO_DIR"; exit 1; }

    # Проверка наличия файла requirements.txt
    if [ -f "requirements.txt" ]; then
        echo "Installing Python dependencies from requirements.txt (excluding torch)..."

        # Создаем временный файл
        TMP_REQ=$(mktemp)
        grep -v '^torch' requirements.txt | grep -v '^#' | grep . > "$TMP_REQ"

        # Устанавливаем зависимости из временного файла
        pip install --cache-dir "${PIP_CACHE_DIR:-/root/pip-cache}" -r "$TMP_REQ" 2> pip_error.log || {
            echo "ERROR: Failed to install dependencies. Check pip_error.log for details."
            rm "$TMP_REQ"
            exit 1
        }

#        pip install --cache-dir "${PIP_CACHE_DIR:-/root/pip-cache}" -r requirements.txt 2> pip_error.log || {
        pip install --cache-dir "${PIP_CACHE_DIR:-/root/pip-cache}" -r "$TMP_REQ" 2> pip_error.log || {
            echo "ERROR: Failed to install dependencies. Check pip_error.log for details."
            rm "$TMP_REQ"
            exit 1
        }

        # Удаляем временный файл
        rm "$TMP_REQ"
    else
        echo "No requirements.txt found in $REPO_DIR."
    fi

done
