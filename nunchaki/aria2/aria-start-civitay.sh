#!/bin/bash

# Проверяем, передан ли файл в качестве аргумента
if [ -z "$1" ]; then
  echo "Ошибка: не указан файл с токеном!"
  echo "Использование: $0 <путь к файлу с токеном>"
  exit 1
fi

# Путь к файлу
MODEL_FILE="$1"

aria2c --input-file="$MODEL_FILE" \
    --allow-overwrite=false \
    --auto-file-renaming=false \
    --continue=true \
    --max-connection-per-server=4 \
    --conditional-get=true
