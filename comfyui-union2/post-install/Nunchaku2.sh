#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

python3 -m pip install --cache-dir=/root/pip-cache \
  https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.1%2Btorch2.7-cp311-cp311-linux_x86_64.whl

# Для
# https://github.com/Fannovel16/comfyui_controlnet_aux
# создать символическую ссылку

mkdir -p /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
mkdir -p /workspace/ComfyUI/models/depth-anything

ln -s /workspace/ComfyUI/models/depth-anything \
 /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts

#cd /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
#rm -rf /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts/depth-anything

rm -rf /root/.cache/pip

