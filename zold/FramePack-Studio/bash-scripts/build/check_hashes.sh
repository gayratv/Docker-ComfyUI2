#!/bin/bash

# Очищаем файл вывода (если он уже существует)
echo -e "\n RUN check_hashes ===="
> last_hashes.txt

# Перебираем все директории первого уровня в /root/repo-cache/
for dir in /root/repo-cache/*/; do
  if [ -f "${dir}.last_hash" ]; then
    echo "Директория: ${dir}" >> last_hashes.txt
    cat "${dir}.last_hash" >> last_hashes.txt
    echo "----------------------------------" >> last_hashes.txt
  else
    echo "Директория без .last_hash: ${dir}" >> last_hashes.txt
  fi
done

# Выводим результат для проверки
cat last_hashes.txt