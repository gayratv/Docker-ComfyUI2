#!/bin/bash

#    --no-cache \
#    --cache-from $IMAGE_NAME:$VERSION \
#    --no-cache \
BASE_DOCKER_DIR="/mnt/f/_prg/python/Docker-ComfyUI/OneTrainer"

docker build --progress=plain \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    --build-arg PYTORCH_WHEEL=$PYTORCH_WHEEL \
    -f ${BASE_DOCKER_DIR}/Dockerfile \
    -t ${IMAGE_NAME}:${VERSION} \
    ${BASE_DOCKER_DIR}

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"

# docker builder prune --all