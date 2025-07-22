#!/bin/bash


cd /workspace/Docker-ComfyUI2/comfyui-union2
mkdir -p ./input/"${MODELS}"
# chmod +x db-gen.sh

python3 ./python-prg-pre-build/generate_dockerfile_v2.py --nodes "${MODELS}.txt"

export BASE_DIR_BUILDX=/workspace/Docker-ComfyUI2/comfyui-union2

#    --no-cache \
#    --cache-from $IMAGE_NAME:$VERSION \
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
    -f "$BASE_DIR_BUILDX/Dockerfile.generated" \
    -t $IMAGE_NAME:$VERSION \
    "$BASE_DIR_BUILDX"

echo -e "\nсобран образ $IMAGE_NAME:$VERSION"

# docker builder prune --all

# Пример запуска:
#   ARIA2_MODEL_DIRS="dir1 dir2 dir3" ./db.sh
