#!/bin/bash

DOCKER_BASE_DIR=/mnt/f/_prg/python/Docker-ComfyUI/docker-base/docker-cuda-12-4-nvidia
cd ${DOCKER_BASE_DIR}

#    --no-cache \
#    --cache-from $IMAGE_NAME:$VERSION \
#    --no-cache \
docker build --progress=plain \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    -f ${DOCKER_BASE_DIR}/Dockerfile \
    -t $IMAGE_NAME:$VERSION \
    ${DOCKER_BASE_DIR}

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"

# docker builder prune --all
