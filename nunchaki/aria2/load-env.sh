#!/bin/bash

# Получаем директорию, где находится текущий скрипт
SCRIPT_DIR=$(dirname "$(realpath "$BASH_SOURCE")")

# Загружаем переменные из .env, если файл существует в той же директории
if [ -f "$SCRIPT_DIR/templates/.env" ]; then
    # Читаем и экспортируем каждую строку из .env
    while IFS='=' read -r key value; do
        # Игнорируем пустые строки и комментарии
        if [[ ! "$key" =~ ^#.*$ && -n "$key" && -n "$value" ]]; then

            value=$(echo "$value" | tr -d '"')
            export "$key=$value"
        fi
    done < "$SCRIPT_DIR/templates/.env"
else
    echo "Файл .env не найден! Создайте его и укажите токены."
#    exit 1
fi

# source ./load-env.sh
# echo $CIVITAI_TOKEN
# env | grep CIVITAI_TOKEN
# printenv | grep CIVITAI_TOKEN