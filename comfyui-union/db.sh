#!/bin/bash

docker build --progress=plain \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    --build-arg NODES="$NODES" \
    --build-arg COMFYUI_VERSION="$COMFYUI_VERSION" \
    --build-arg ACE_PLUS_NODE_INSTALL=$ACE_PLUS_NODE_INSTALL \
    --build-arg POST_INSTALL_SH=$POST_INSTALL_SH \
    -f /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union/Dockerfile \
    -t $IMAGE_NAME:$VERSION \
    /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union
echo -e "\nсобран образ $IMAGE_NAME:$VERSION"