#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

cd /workspace/ComfyUI/custom_nodes/rgthree-comfy
git checkout -b old-branch aa6c75a

#pip uninstall -y mediapipe

pip install --cache-dir=/root/pip-cache gguf simpleeval


## Для Deepl транслятор
## Для переводчика удалить инициализацию DeepLXTranslateNode
#sed -i '/# DeepLXTranslateNode/,/# GoogleTranslateNode/{/# GoogleTranslateNode/!d;}' /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/__init__.py
#
##pip install --cache-dir=/root/pip-cache -r /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/DeepTranslatorNode/requirements.txt
#pip install --cache-dir=/root/pip-cache -r /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/GoogleTranslateNode/requirements.txt
#pip install --cache-dir=/root/pip-cache -r /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/ArgosTranslateNode/requirements.txt


rm -rf /root/.cache/pip

