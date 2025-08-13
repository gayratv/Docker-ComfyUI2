#!/bin/bash

#cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/aria2/templates
#python3 /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/python-prg/common_dl.py \
#  ./models/FluxKontext/models.txt --prefix /mnt/d/_tmp

# Проверка наличия первого аргумента
if [ -z "$1" ]; then
    echo "Использование: $0 <путь_к_models.txt> [путь_к_папке_назначения]"
    exit 1
fi

MODELS_FILE="./models/$1"
DEST_PATH="$2"
# Базовый путь к python-программам
#PY_PRG_PATH="/mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/python-prg"
PY_PRG_PATH="/workspace/ComfyUI/gayrat_py"

# Проверка, что файл существует
if [ ! -f "$MODELS_FILE" ]; then
    echo "Ошибка: файл '$MODELS_FILE' не найден."
    exit 1
fi

# Переход в рабочую директорию
# cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/aria2/templates || exit 1
cd /workspace/aria2/templates || exit 1

# Запуск Python-скрипта
if [ -z "$DEST_PATH" ]; then
    python3 "$PY_PRG_PATH/common_dl.py" \
      "$MODELS_FILE"
else
    python3 "$PY_PRG_PATH/common_dl.py" \
      "$MODELS_FILE" --prefix "$DEST_PATH"
fi
