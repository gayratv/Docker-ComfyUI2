#!/bin/bash

# Проверяем, передан ли параметр
if [ -z "$1" ]; then
  echo "Использование: $0 <MODELS>"
  exit 1
fi

MODELS="$1"

cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2 || { echo "Не удалось перейти в директорию"; exit 1; }

mkdir -p "./workflows/${MODELS}"
mkdir -p "./aria2/templates/models/${MODELS}"
mkdir -p "./workflow-descr/${MODELS}"
touch  "./custom-nodes/${MODELS}.txt"
cp ./post-install/ImageResize.sh "./post-install/${MODELS}.sh"
echo -e "\033[33mworkflow ${MODELS} подготовлено\033[0m"

# ./workflow-new-image.sh "wan-2.1"