#!/bin/bash

# Получаем директорию, где находится текущий скрипт
SCRIPT_DIR=$(dirname "$(realpath "$BASH_SOURCE")")

source "$SCRIPT_DIR/curl3.sh"

base_dir=/workspace/ComfyUI/models/
#base_dir=/mnt/D/ComfyUI-data/models/


directory1="${base_dir%/}/diffusion_models"
# Flux-Main/flux1-dev-fp8-e4m3fn.safetensors
url1="https://huggingface.co/OreX/Models/resolve/main/Flux-Main/flux1-dev-fp8-e4m3fn.safetensors"
download_file_curl "$directory1" "$url1"

directory1="${base_dir%/}/clip"
# t5-v1_1-xxl-encoder-Q5_K_M.gguf
url1="https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/resolve/main/t5-v1_1-xxl-encoder-Q5_K_M.gguf"
download_file_curl "$directory1" "$url1"

# Flux-Main/t5xxl_fp8_e4m3fn.safetensors
url1="https://huggingface.co/OreX/Models/resolve/main/Flux-Main/t5xxl_fp8_e4m3fn.safetensors"
download_file_curl "$directory1" "$url1"

# Flux-Main/clip_l.safetensors
url1="https://huggingface.co/OreX/Models/resolve/main/Flux-Main/clip_l.safetensors"
download_file_curl "$directory1" "$url1"

directory1="${base_dir%/}/upscale_models"
# UltraSharp upscale
url1="https://huggingface.co/Gayrat1968/UltraSharp-upscaler/resolve/main/4x-UltraSharp.pth"
download_file_curl "$directory1" "$url1"


wait  # Ожидание завершения всех фоновых процессов
echo ""
echo ""
echo "=========================================="
echo "Все загрузки завершены!"