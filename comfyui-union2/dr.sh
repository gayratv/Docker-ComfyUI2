#!/bin/bash

echo "run --name $IMAGE_NAME $IMAGE_NAME:$VERSION"
docker rm -f "$IMAGE_NAME"
docker run -it --privileged --gpus all -p 8188:8188 -p 1188:1188 \
    -v /mnt/h/ComfyUI-data/models:/workspace/ComfyUI/models \
    --name "$IMAGE_NAME" "$IMAGE_NAME:$VERSION" \
    tmux-s-bash.sh