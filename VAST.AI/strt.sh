#!/bin/bash

# Проверка наличия аргумента для IMAGE_NAME
if [ -z "$1" ]; then
    echo "Ошибка: Необходимо указать имя образа Docker в качестве первого аргумента."
    echo "Пример использования: $0 gayrat/comfy-union:SUPIR-v2-MaskTile"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Ошибка: Необходимо указать версию CUDA"
    echo "Пример использования: $0 gayrat/comfy-union:SUPIR-v2-MaskTile"
    exit 1
fi

# Установка рабочей директории
cd /mnt/f/_prg/python/Docker-ComfyUI/

cd /mnt/f/_prg/python/Docker-ComfyUI/VAST.AI
source /mnt/f/_prg/python/Docker-ComfyUI/.venv-wsl/bin/activate
export IMAGE_NAME="$1"
python3 vast-search-py3.py --ram 32000 --gpu1 "RTX 4090" --gpu2 "RTX 3090" --cuda_max_good "$2"