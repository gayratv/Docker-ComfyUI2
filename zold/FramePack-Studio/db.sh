#!/bin/bash

#    --no-cache \
#    --cache-from $IMAGE_NAME:$VERSION \
#    --no-cache \
docker build --progress=plain \
    --build-arg PYTORCH_WHEEL=$PYTORCH_WHEEL \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    -f /mnt/f/_prg/python/Docker-ComfyUI/FramePack-Studio/Dockerfile \
    -t $IMAGE_NAME:$VERSION \
    /mnt/f/_prg/python/Docker-ComfyUI/FramePack-Studio

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"

# docker builder prune --all