#!/bin/bash

## Получаем директорию, где находится текущий скрипт
#SCRIPT_DIR=$(dirname "$(realpath "$BASH_SOURCE")")
#
## Загружаем переменные из .env, если файл существует в той же директории
#if [ -f "$SCRIPT_DIR/.env" ]; then
#    source "$SCRIPT_DIR/.env"
#else
#    echo "Файл .env не найден! Создайте его и укажите токены."
#    exit 1
#fi

# Проверяем, что передан входной файл
if [ -z "$1" ]; then
  echo "Пожалуйста, укажите имя входного файла."
  exit 1
fi

# Указываем входной файл
input_file="$1"
# Формируем имя выходного файла, добавляя "-token" перед расширением
output_file="${input_file%.txt}-token.txt"

# Очищаем выходной файл перед записью (перезаписываем)
> "$output_file"

# Открываем файл для записи и читаем его построчно
while IFS= read -r line; do
  # Если строка содержит ссылку (начинается с http)
  if [[ "$line" =~ ^https?:// ]]; then
    line=$(echo -n "$line" | sed 's/\r$//')
    # Добавляем &token=$TOKEN в конец строки
    echo "$line&token=$CIVITAI_TOKEN" >> "$output_file"
  else
    # Если это не ссылка, выводим строку без изменений
    echo "$line" >> "$output_file"
  fi
done < "$input_file"

echo "Результат записан в файл: $output_file"
