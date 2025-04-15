#!/bin/bash

#cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-supir/aria2/templates

# Проверка наличия первого параметра
if [ -z "$1" ]; then
  echo "Ошибка: Необходимо указать первый параметр (например, supir-bodrov)."
  echo "Использование: $0 <параметр> [рабочая_директория]"
  exit 1
fi

# Присваиваем первый параметр переменной
MODEL_PARAM="$1"

# Определяем рабочую директорию (второй параметр или значение по умолчанию)
WORKSPACE_DIR="${2:-/workspace/ComfyUI/}"

# Определяем пути на основе параметров
HF_FILE="./models/$MODEL_PARAM/hf.txt"
CIVITAI_FILE="./models/$MODEL_PARAM/civitay.txt"

# Проверяем наличие файла hf.txt
if [[ -e "$HF_FILE" ]]; then
  # Запускаем скрипт для Hugging Face, если файл существует
  echo "Запуск скрипта для Hugging Face с файлом '$HF_FILE'..."
  ../aria-start-huggingface.sh "$HF_FILE" "$WORKSPACE_DIR"
else
  echo "Пропуск запуска скрипта для Hugging Face из-за отсутствия файла '$HF_FILE'."
fi

# Проверяем наличие файла civitay.txt
if [[ -e  "$CIVITAI_FILE" ]]; then
  # Запускаем скрипт для Civitai, если файл существует
  echo "Запуск скрипта для Civitai с файлом '$CIVITAI_FILE'..."
  ../process-models-civitai.sh "$CIVITAI_FILE"
  ../aria-start-civitay.sh "$CIVITAI_FILE" "$WORKSPACE_DIR"
else
  echo "Пропуск запуска скриптов для Civitai из-за отсутствия файла '$CIVITAI_FILE'."
fi