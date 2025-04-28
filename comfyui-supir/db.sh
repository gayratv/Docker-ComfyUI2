#!/bin/bash

#    --no-cache \
docker build --progress=plain \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    --build-arg NODES="$NODES" \
    --build-arg ACE_PLUS_NODE_INSTALL=$ACE_PLUS_NODE_INSTALL \
    --build-arg POST_INSTALL=$POST_INSTALL \
    -f /mnt/f/_prg/python/Docker-ComfyUI/comfyui-supir/Dockerfile \
    -t $IMAGE_NAME:$VERSION \
    /mnt/f/_prg/python/Docker-ComfyUI/comfyui-supir

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"

