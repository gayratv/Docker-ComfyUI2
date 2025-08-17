#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

python3 -m pip uninstall -y opencv_python opencv_contrib_python_headless opencv_contrib_python opencv_python_headless
python3 -m pip install --cache-dir=/root/pip-cache opencv_python opencv_contrib_python_headless opencv_contrib_python opencv_python_headless
python3 -m pip install --cache-dir=/root/pip-cache opencv_python onnx onnxruntime


python3 -m pip install --cache-dir=/root/pip-cache /workspace/wheels/sageattention_wheel/3090/Cuda12_6/sageattention-*.whl

# Проверка наличия директории перед выполнением действий
if [ -d /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ ]; then
  mkdir -p /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
  mkdir -p /workspace/ComfyUI/models/depth-anything

  ln -s /workspace/ComfyUI/models/depth-anything \
   /workspace/ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts
fi

rm -rf /root/.cache/pip
