#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

#python3 -m pip install --cache-dir=/root/pip-cache pruna

# NUNCHAKU
#python3 -m pip install --cache-dir=/root/pip-cache \
#  https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.1%2Btorch2.7-cp311-cp311-linux_x86_64.whl

#dzNodes: LayerStyle ->
#Please REINSTALL package 'opencv-contrib-python'.

python3 -m pip uninstall -y opencv_python opencv_contrib_python_headless opencv_contrib_python opencv_python_headless
python3 -m pip install --cache-dir=/root/pip-cache opencv_python opencv_contrib_python_headless opencv_contrib_python opencv_python_headless

python3 -m pip install --cache-dir=/root/pip-cache /workspace/wheels/sageattention_wheel/3090/Cuda12_6/sageattention-*.whl

# Проверка наличия директории перед выполнением действий
if [ -d /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ ]; then
  mkdir -p /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
  mkdir -p /workspace/ComfyUI/models/depth-anything

  ln -s /workspace/ComfyUI/models/depth-anything \
   /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
fi

rm -rf /root/.cache/pip

