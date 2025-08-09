#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

#python3 -m pip install --cache-dir=/root/pip-cache pruna
#git clone https://github.com/PrunaAI/pruna.git

# NUNCHAKU
#python3 -m pip install --cache-dir=/root/pip-cache \
#  https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.1%2Btorch2.7-cp311-cp311-linux_x86_64.whl

# Проверка наличия директории перед выполнением действий
if [ -d /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ ]; then
  mkdir -p /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
  mkdir -p /workspace/ComfyUI/models/depth-anything

  ln -s /workspace/ComfyUI/models/depth-anything \
   /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
fi

# Блок коректировки пакетов для CUDA 12.8

python3 -m pip install --upgrade --cache-dir=/root/pip-cache torch==2.8.0 torchaudio==2.8.0 torchsde==0.2.6 torchvision==0.23.0

rm -rf /root/.cache/pip

