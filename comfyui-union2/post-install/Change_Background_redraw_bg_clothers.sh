#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

#cd /workspace/ComfyUI/custom_nodes/rgthree-comfy
#git checkout -b old-branch aa6c75a
rm -rf /workspace/ComfyUI/custom_nodes/BizyAir
rm -rf /root/.cache/pip

