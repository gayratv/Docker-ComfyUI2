#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

python3 -m pip install --cache-dir=/root/pip-cache \
  https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.1%2Btorch2.7-cp311-cp311-linux_x86_64.whl


# python3 -m pip install --cache-dir=/root/pip-cache triton
# python3 -m pip uninstall -y triton

# Для
# https://github.com/Fannovel16/comfyui_controlnet_aux
# создать символическую ссылку

mkdir -p /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
mkdir -p /workspace/ComfyUI/models/depth-anything

ln -s /workspace/ComfyUI/models/depth-anything \
 /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts

#cd /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
#rm -rf /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts/depth-anything

# nunchaku просит установить apex
python3 -m pip install --cache-dir=/root/pip-cache /workspace/wheels/apex_wheel/apex-*.whl

rm -rf /root/.cache/pip

