#!/bin/bash

DOCKER_BASE_DIR=/mnt/f/_prg/python/Docker-ComfyUI/docker-base/wheel-complie
cd ${DOCKER_BASE_DIR}
IMAGE_NAME=wheel
VERSION=triton

#    --no-cache \

#    --no-cache \
docker build --progress=plain \
    --cache-from $IMAGE_NAME:$VERSION \
    -f ${DOCKER_BASE_DIR}/Dockerfile \
    --output type=local,dest=./prebuilt_wheels \
    ${DOCKER_BASE_DIR}

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"

# docker builder prune --all
