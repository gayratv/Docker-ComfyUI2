#!/bin/bash

source /mnt/f/_prg/python/Docker-ComfyUI/.venv/bin/activate
cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2

#    --no-cache \
#    --no-cache \
DOCKER_BUILDKIT=1 docker build --progress=plain \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    --cache-from $IMAGE_NAME:$VERSION \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    --build-arg NODES="$NODES" \
    --build-arg POST_INSTALL=$POST_INSTALL \
    --build-arg WORKFLOW_TO_COPY=$WORKFLOW_TO_COPY \
    --build-arg MODELS=$MODELS \
    --build-arg DOWNLOAD_MODELS="$DOWNLOAD_MODELS" \
    --build-arg ARIA2_MODEL_DIRS="$ARIA2_MODEL_DIRS" \
    --build-arg COMFYUI_VERSION=$COMFYUI_VERSION \
    --build-arg PYTORCH_WHEEL=$PYTORCH_WHEEL \
    --build-arg REQ_MODIFY=$REQ_MODIFY \
    --output ./assets-docker/apex_wheel \
    -f /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/Dockerfile_apex_build \
    -t apex_wheel:V1 \
    /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2

echo -e "\nсобран образ apex_wheel:V1"
