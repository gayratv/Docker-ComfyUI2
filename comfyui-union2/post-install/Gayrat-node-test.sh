#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

cd /workspace/ComfyUI/custom_nodes/rgthree-comfy
git checkout -b old-branch aa6c75a

pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python-headless opencv-contrib-python
pip uninstall -y mediapipe

# для https://github.com/chflame163/ComfyUI_LayerStyle_Advance
pip install --cache-dir=/root/pip-cache docopt hydra-core
#pip install --cache-dir=/root/pip-cache docopt==0.6.2 hydra-core==1.3.2

pip install --cache-dir=/root/pip-cache addict yapf pymatting
pip install --cache-dir=/root/pip-cache mediapipe
pip install --cache-dir=/root/pip-cache google-generativeai

pip install --cache-dir=/root/pip-cache scikit-image blend_modes scikit-learn
pip install --cache-dir=/root/pip-cache openai
pip install --cache-dir=/root/pip-cache segment_anything
pip install --cache-dir=/root/pip-cache timm wget matplotlib colour-science

pip install --cache-dir=/root/pip-cache opencv-python opencv-python-headless opencv-contrib-python-headless


#mkdir -p /workspace/ComfyUI/custom_nodes/comfy-mtb/extern
#mkdir -p /workspace/ComfyUI/custom_nodes/comfy_mtb/extern
#cd /workspace/ComfyUI/custom_nodes/comfy_mtb

#python3 scripts/download_models.py

rm -rf /root/.cache/pip

