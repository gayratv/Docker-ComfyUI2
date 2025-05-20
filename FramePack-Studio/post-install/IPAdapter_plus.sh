#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

pip install --cache-dir=/root/pip-cache insightface


#ubuntu bash
#в файле
#/workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/cnr_utils.py
#есть фрагмент кода
#            if page % 5 == 0:
#                print(f"FETCH ComfyRegistry Data: {page}/{sub_json_obj['totalPages']}")
#надо найти и удалить его

sed -i '/if page % 5 == 0:/,+1d' /workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/cnr_utils.py

#/workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/manager_server.py
#logging.info(f"[ComfyUI-Manager] default cache updated: {uri}")

#sed -i '/^[[:space:]]*logging.info(f"[ComfyUI-Manager] default cache updated: {uri}")/d' \
#    /workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/manager_server.py

#/workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/manager_util.py
#            if not silent:
#                logging.info(f"[ComfyUI-Manager] default cache updated: {uri}")

#sed -i '/^[[:space:]]*if not silent:/ {
#N
#/^[[:space:]]*logging.info(f"$$ComfyUI-Manager$$ default cache updated: {uri}")/d
#}' /workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/manager_util.py

# grep -r 'default cache updated' /workspace/ComfyUI/custom_nodes/ComfyUI-Manager/
# grep -r 'default cache updated' /mnt/d/1/ComfyUI-Manager/glob


#python3 /workspace/ComfyUI/gayrat_py/remove_lines.py

rm -rf /root/.cache/pip