#!/bin/bash

#source ../load-env.sh

if [ -z "$HF_TOKEN" ]; then
  echo "Ошибка: Переменная окружения HF_TOKEN не установлена!" >&2
  echo  "запусти source ./load-env.sh"
  exit 1
fi


# Проверяем, передан ли файл в качестве аргумента
if [ -z "$1" ]; then
  echo "Ошибка: не указан файл с токеном!"
  echo "Использование: $0 <путь к файлу с токеном>"
  exit 1
fi

# Путь к файлу
MODEL_FILE="$1"

aria2c --input-file="$MODEL_FILE" \
    --allow-overwrite=false --auto-file-renaming=false --continue=true \
    --max-connection-per-server=5 --conditional-get=true \
    ${HF_TOKEN:+--header="Authorization: Bearer ${HF_TOKEN}"}