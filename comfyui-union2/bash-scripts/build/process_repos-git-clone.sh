#!/bin/bash

# Получение файла со списком репозиториев из первого аргумента или значение по умолчанию
NODES_FILE="${1:-nodes.txt}"

# Получение BASE_INSTALL_DIR из второго аргумента или значение по умолчанию
BASE_INSTALL_DIR="${2:-/workspace/ComfyUI/custom_nodes/}"


# Проверка наличия файла nodes.txt
if [ ! -f "$NODES_FILE" ]; then
    echo "ERROR: $NODES_FILE not found. Create the file and add repository URLs."
    exit 1
fi

# Чтение списка репозиториев из файла
mapfile -t INSTALL_DATA < "$NODES_FILE"

echo "DEBUG: Using BASE_INSTALL_DIR: $BASE_INSTALL_DIR"
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
done