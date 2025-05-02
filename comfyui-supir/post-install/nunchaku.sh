#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

# Пути
WHEELS_CACHE_DIR="/root/pip-cache/wheels-cache"
PIP_CACHE_DIR="/root/pip-cache"
WHEEL_URL="https://github.com/mit-han-lab/nunchaku/releases/download/v0.2.0/nunchaku-0.2.0+torch2.6-cp311-cp311-linux_x86_64.whl"
WHEEL_FILE="$WHEELS_CACHE_DIR/nunchaku-0.2.0+torch2.6-cp311-cp311-linux_x86_64.whl"

# Создаем кэш-каталоги
mkdir -p "$WHEELS_CACHE_DIR" "$PIP_CACHE_DIR"

# Скачиваем .whl, если его нет
if [ ! -f "$WHEEL_FILE" ]; then
    echo "Downloading nunchaku wheel..."
    wget -O "$WHEEL_FILE" "$WHEEL_URL"
else
    echo "Using cached wheel: $WHEEL_FILE"
fi

# Устанавливаем пакет из кэшированного файла
pip install --cache-dir="$PIP_CACHE_DIR" "$WHEEL_FILE"

#pip install --cache-dir /root/pip-cache --verbose "https://github.com/mit-han-lab/nunchaku/releases/download/v0.2.0/nunchaku-0.2.0+torch2.6-cp311-cp311-linux_x86_64.whl"


# Для Deepl транслятор

pip install --cache-dir="$PIP_CACHE_DIR" -r /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/DeepTranslatorNode/requirements.txt
pip install --cache-dir="$PIP_CACHE_DIR" -r /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/GoogleTranslateNode/requirements.txt
pip install --cache-dir="$PIP_CACHE_DIR" -r /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/ArgosTranslateNode/requirements.txt

rm -rf /root/.cache/pip


# Для Deepl транслятор
#mkdir /temp
#cd /temp
#wget https://go.dev/dl/go1.24.2.linux-amd64.tar.gz
#tar -xzf go1.24.2.linux-amd64.tar.gz -C /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/DeepLXTranslateNode
#cd /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/DeepLXTranslateNode
#git clone https://github.com/OwO-Network/DeepLX

#echo 'export IP=127.0.0.1' >> /root/.bashrc
