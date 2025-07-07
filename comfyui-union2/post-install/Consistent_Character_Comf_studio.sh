#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

#pip install --cache-dir=/root/pip-cache segment_anything

process_one_repo_install_req_hash.sh https://github.com/Limitex/ComfyUI-Diffusers false

export REQ_MODIFY=Consistent_Character_Comf_studio
export REQ_MODIFY_PATH=/workspace/requirements-modify/Consistent_Character_Comf_studio/

python3 /workspace/ComfyUI/gayrat_py/process-req-in.py \
            --requirements-file "/workspace/ComfyUI/custom_nodes/ComfyUI-Diffusers/requirements.txt" \
            --prefixes-file "$REQ_MODIFY_PATH/remove-lines.txt" \
            --additional-lines-file "$REQ_MODIFY_PATH/add-lines.txt"

cd /workspace/ComfyUI/custom_nodes/ComfyUI-Diffusers/
python3 -m pip install --cache-dir=/root/pip-cache -r requirements.modify.txt

#streamdiffusion[tensorrt] @ git+https://github.com/cumulo-autumn/StreamDiffusion.git@main
#git+https://github.com/cumulo-autumn/StreamDiffusion.git@main#egg=streamdiffusion[tensorrt]

#63 39.26 ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
#63 39.26 mediapipe 0.10.14 requires protobuf<5,>=4.25.3, but you have protobuf 3.20.2 which is incompatible.
#63 39.26 Successfully installed colored-2.3.0 cuda-bindings-12.9.0 cuda-python-12.9.0 diffusers-0.24.0 fire-0.7.0 lightning-utilities-0.14.3 onnx-1.15.0 onnxruntime-1.16.3 protobuf-3.20.2 pytorch_lightning-2.5.2 streamdiffusion-0.1.1 torchmetrics-1.7.4 xformers-0.0.31
#63 39.26 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.

rm -rf /root/.cache/pip

