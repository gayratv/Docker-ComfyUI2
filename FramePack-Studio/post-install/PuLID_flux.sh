#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

# Для Deepl транслятор

# Для переводчика удалить инициализацию DeepLXTranslateNode
sed -i '/# DeepLXTranslateNode/,/# GoogleTranslateNode/{/# GoogleTranslateNode/!d;}' /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/__init__.py


#pip install --cache-dir=/root/pip-cache -r /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/DeepTranslatorNode/requirements.txt
pip install --cache-dir=/root/pip-cache -r /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/GoogleTranslateNode/requirements.txt
pip install --cache-dir=/root/pip-cache -r /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/ArgosTranslateNode/requirements.txt



pip uninstall -y opencv-contrib-python numpy opencv-python

pip install --cache-dir=/root/pip-cache numpy simpleeval opencv-python opencv-python-headless
pip install --cache-dir=/root/pip-cache timm gguf ftfy
pip install --cache-dir=/root/pip-cache insightface
pip install --cache-dir=/root/pip-cache facexlib

# pip show opencv-python

rm -rf /root/.cache/pip

