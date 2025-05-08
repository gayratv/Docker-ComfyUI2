#!/bin/bash

# Получаем директорию, где находится текущий скрипт
SCRIPT_DIR=$(dirname "$(realpath "$BASH_SOURCE")")

source "$SCRIPT_DIR/curl3.sh"

base_dir=/workspace/ComfyUI/models/
directory1="${base_dir%/}/stablesr"
# https://huggingface.co/Iceclear/StableSR
# Put the StableSR webui_786v_139.ckpt model into Comyfui/models/stablesr/
url1="https://huggingface.co/Iceclear/StableSR/resolve/main/webui_768v_139.ckpt"
download_file_curl "$directory1" "$url1"

# Put the StableSR stablesr_768v_000139.ckpt model into Comyfui/models/checkpoints/
directory1="${base_dir%/}/checkpoints/stablesr"
url1="https://huggingface.co/Iceclear/StableSR/resolve/main/stablesr_768v_000139.ckpt"
download_file_curl "$directory1" "$url1"

# KamCastle/jugg juggernaut_reborn.safetensors
directory1="${base_dir%/}/checkpoints/SD1.5"
url1="https://huggingface.co/KamCastle/jugg/resolve/main/juggernaut_reborn.safetensors"
download_file_curl "$directory1" "$url1"

# Kijai/SUPIR_pruned
# SUPIR-v0F_fp16.safetensors
directory1="${base_dir%/}/checkpoints/SUPIR"
url1="https://huggingface.co/Kijai/SUPIR_pruned/resolve/main/SUPIR-v0F_fp16.safetensors"
download_file_curl "$directory1" "$url1"
# SUPIR-v0Q_fp16.safetensors
url1="https://huggingface.co/Kijai/SUPIR_pruned/resolve/main/SUPIR-v0Q_fp16.safetensors"
download_file_curl "$directory1" "$url1"

# RealVisXL V5.0 SDXL
directory1="${base_dir%/}/checkpoints/SDXL"
url1="https://civitai.com/api/download/models/789646?type=Model&format=SafeTensor&size=full&fp=fp16"
download_file_curl "$directory1" "$url1"


wait  # Ожидание завершения всех фоновых процессов
echo ""
echo ""
echo "=========================================="
echo "Все загрузки завершены!"