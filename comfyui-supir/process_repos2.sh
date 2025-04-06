#!/bin/bash

# Установка базовой директории
BASE_INSTALL_DIR="/workspace/ComfyUI/custom_nodes/"
#BASE_INSTALL_DIR="/mnt/d/test-pip/ComfyUI/custom_nodes/"


# Получение файла со списком репозиториев из аргумента или установка значения по умолчанию
NODES_FILE="${1:-nodes.txt}"

#echo "DEBUG: Checking for file at path: $NODES_FILE"
#ls -l "$NODES_FILE"

# Проверка наличия файла nodes.txt
if [ ! -f "$NODES_FILE" ]; then
    echo "ERROR: $NODES_FILE not found. Create the file and add repository URLs."
    exit 1
fi

# Чтение списка репозиториев из файла
mapfile -t INSTALL_DATA < "$NODES_FILE"

#cd "$BASE_INSTALL_DIR"

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
    git clone --recurse-submodules "$GIT_REPO"
#    git clone "$GIT_REPO"


    # Переход во вновь созданную директорию
    # Извлекаем имя директории из URL репозитория
    REPO_DIR=$(basename "$GIT_REPO" .git | sed 's/\r$//')
    echo "DEBUG: Cloned repository directory: $REPO_DIR"

#    cd "$REPO_DIR" || { echo "ERROR: Failed to change directory to $REPO_DIR"; exit 1; }

    # Проверка наличия файла requirements.txt
#    if [ -f "requirements.txt" ]; then
#        echo "Installing Python dependencies from requirements.txt..."
#        pip3 install -r requirements.txt
#    else
#        echo "No requirements.txt found in $REPO_DIR."
#    fi

done
