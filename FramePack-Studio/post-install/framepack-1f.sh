#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

pip uninstall -y opencv-contrib-python numpy

pip install --cache-dir=/root/pip-cache opencv-contrib-python accelerate numpy diffusers imageio-ffmpeg


#ubuntu bash
#в файле
#/workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/cnr_utils.py
#есть фрагмент кода
#            if page % 5 == 0:
#                print(f"FETCH ComfyRegistry Data: {page}/{sub_json_obj['totalPages']}")
#надо найти и удалить его

# sed -i '/if page % 5 == 0:/,+1d' /workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/cnr_utils.py


rm -rf /root/.cache/pip
