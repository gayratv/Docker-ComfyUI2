#!/bin/bash

export LOCAL_PATH=/mnt/f/_prg/python/ComfyUI_Gayrat/SaveImageAndMask/
export REMOTE_PATH=/workspace/ComfyUI/custom_nodes/ComfyUI_Gayrat/SaveImageAndMask/

docker exec comfyui-union2 rm -rf /workspace/ComfyUI/custom_nodes/ComfyUI_Gayrat/SaveImageAndMask/__pycache__

#docker cp ${LOCAL_PATH}LoadImageWithTrimOptions.py  comfyui-union2:${REMOTE_PATH}
#docker cp ${LOCAL_PATH}save_image_with_alpha.py  comfyui-union2:${REMOTE_PATH}
docker cp ${LOCAL_PATH}  comfyui-union2:${REMOTE_PATH}
