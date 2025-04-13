#!/bin/bash

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

# Запускаем скрипт для Hugging Face
../aria-start-huggingface.sh "$HF_FILE" "$WORKSPACE_DIR"

# Запускаем скрипт для Civitai
../process-models-civitai.sh "$CIVITAI_FILE"
../aria-start-civitay.sh "$CIVITAI_FILE" "$WORKSPACE_DIR"