#!/bin/bash

#    --no-cache \
#    --cache-from $IMAGE_NAME:$VERSION \
#    --no-cache \
docker build --progress=plain \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    --build-arg MODELS=$MODELS \
    --build-arg PYTORCH_WHEEL=$PYTORCH_WHEEL \
    -f /mnt/f/_prg/python/Docker-ComfyUI/Fluxgym/Dockerfile \
    -t $IMAGE_NAME:$VERSION \
    /mnt/f/_prg/python/Docker-ComfyUI/Fluxgym

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"

# docker builder prune --all