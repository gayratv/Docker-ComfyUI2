#!/bin/bash

DOCKER_BASE_DIR=/mnt/f/_prg/python/Docker-ComfyUI/docker-base/docker-cuda-test
cd ${DOCKER_BASE_DIR}

docker build --progress=plain \
    --cache-from $IMAGE_NAME:$VERSION \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    --build-arg INSTALL_tensorrt="$INSTALL_tensorrt" \
    -f ${DOCKER_BASE_DIR}/Dockerfile \
    -t $IMAGE_NAME:$VERSION \
    ${DOCKER_BASE_DIR}

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"
