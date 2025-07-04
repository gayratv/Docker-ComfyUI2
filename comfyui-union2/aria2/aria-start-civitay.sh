#!/bin/bash

# Проверяем, передан ли файл в качестве аргумента
if [ -z "$1" ]; then
  echo "Ошибка: не указан файл с токеном!"
  echo "Использование: $0 <путь к файлу с токеном>"
  exit 1
fi

# Путь к файлу
MODEL_FILE="$1"

MODEL_FILE_TOKEN=$(echo "$MODEL_FILE" | sed 's/\(.*\)\..*/\1-token.txt/')
echo -e "MODEL_FILE_TOKEN = $MODEL_FILE_TOKEN \n"

# Префикс (второй параметр)
PREFIX="$2"
echo "PREFIX: $PREFIX"
# Если префикс передан, применяем sed и создаем новый файл
if [ -n "$PREFIX" ]; then

  NEW_MODEL_FILE="${MODEL_FILE_TOKEN}.modified"
  sed "s|^[[:space:]]*dir=|    dir=${PREFIX}/|" "$MODEL_FILE_TOKEN" > "$NEW_MODEL_FILE"
fi

aria2c --input-file="$NEW_MODEL_FILE" \
    --allow-overwrite=false \
    --auto-file-renaming=false \
    --continue=true \
    --max-connection-per-server=4 \
    --conditional-get=true
#    \
#    2>&1 | grep --color=always -v "Redirecting to"
