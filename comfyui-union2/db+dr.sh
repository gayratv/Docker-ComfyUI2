#!/bin/bash

#    --no-cache \
#    --cache-from $IMAGE_NAME:$VERSION \
#    --no-cache \
docker build --progress=plain \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    --build-arg NODES="$NODES" \
    --build-arg POST_INSTALL=$POST_INSTALL \
    --build-arg WORKFLOW_TO_COPY=$WORKFLOW_TO_COPY \
    --build-arg MODELS=$MODELS \
    --build-arg COMFYUI_VERSION=$COMFYUI_VERSION \
    --build-arg PYTORCH_WHEEL=$PYTORCH_WHEEL \
    --build-arg REQ_MODIFY=$REQ_MODIFY \
    -f /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/Dockerfile \
    -t $IMAGE_NAME:$VERSION \
    /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"

source dr.sh

#echo "run --name $IMAGE_NAME $IMAGE_NAME:$VERSION"
#docker rm -f "$IMAGE_NAME"
#docker run -it --privileged --gpus all -p 8188:8188 -p 1188:1188 \
#    --env-file .env \
#    -v /mnt/h/ComfyUI-data/models:/workspace/ComfyUI/models \
#    --name "$IMAGE_NAME" "$IMAGE_NAME:$VERSION" \
#    tmux-s-bash.sh