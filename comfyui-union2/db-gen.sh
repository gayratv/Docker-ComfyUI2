#!/bin/bash

source /mnt/f/_prg/python/Docker-ComfyUI/.venv/bin/activate

cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2
mkdir -p ./input/"${MODELS}"

python3 ./python-prg-pre-build/generate_dockerfile_v2.py --nodes "${MODELS}.txt"

# Установить PY_VER по умолчанию, если не задана
: "${PY_VER:=3.11}"
export PY_VER
: "${COMFYUI_FRONTEND_VERSION:=1.25.1}"

#    --no-cache \
#    --cache-from $IMAGE_NAME:$VERSION \
#    --no-cache \
DOCKER_BUILDKIT=1 docker build --progress=plain \
    --build-arg BUILDKIT_INLINE_CACHE=1 \
    --build-arg PY_VER="$PY_VER" \
    --build-arg COMFYUI_FRONTEND_VERSION="$COMFYUI_FRONTEND_VERSION" \
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
    -f /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/Dockerfile.generated \
    -t $IMAGE_NAME:$VERSION \
    /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"

# docker builder prune --all

# Пример запуска:
#   ARIA2_MODEL_DIRS="dir1 dir2 dir3" ./db.sh
