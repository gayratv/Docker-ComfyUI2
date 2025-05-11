#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

cd /workspace/ComfyUI/custom_nodes/rgthree-comfy
git checkout -b old-branch aa6c75a

pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python-headless opencv-contrib-python

pip install --cache-dir=/root/pip-cache scikit-image blend_modes
pip install --cache-dir=/root/pip-cache opencv-python opencv-python-headless opencv-contrib-python-headless

rm -rf /root/.cache/pip

