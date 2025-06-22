#!/bin/bash
# file dr.sh

# Загружаем переменные из .env файла
#export $(grep -v '^#' .env | xargs)
#echo $GOOGLE_API

#export MODELS="SDXL_Consistent_Character"

echo "run --name $IMAGE_NAME $IMAGE_NAME:$VERSION"
docker rm -f "$IMAGE_NAME"
docker run -it --privileged --gpus all -p 8188:8188 -p 1188:1188 \
    --env-file .env \
    -v /mnt/h/ComfyUI-data/models:/workspace/ComfyUI/models \
    -v /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/_temp_save/output:/workspace/ComfyUI/output \
    -v /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/workflows/${MODELS}:/workspace/ComfyUI/user/default/workflows/${MODELS} \
    -v /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/input/${MODELS}:/workspace/ComfyUI/input/ \
    --name "$IMAGE_NAME" "$IMAGE_NAME:$VERSION" \
    tmux-s-bash.sh
#    bash
#    tmux-s.sh
