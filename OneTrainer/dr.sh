#!/bin/bash
# file dr.sh

echo "run --name $IMAGE_NAME $IMAGE_NAME:$VERSION"
docker rm -f "$IMAGE_NAME"

#docker run -it --privileged --gpus all -p 7860:7860  \
#    -v /mnt/h/ComfyUI-data/models:/workspace/ComfyUI/models \
#    --name "$IMAGE_NAME" "$IMAGE_NAME:$VERSION" \
#    bash
#  -e DISPLAY=$DISPLAY \

docker run \
  -e DISPLAY=172.21.176.1:0 \
  -it --gpus all \
  -v /mnt/h/ComfyUI-data/models:/workspace/ComfyUI/models \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --name "$IMAGE_NAME" "$IMAGE_NAME:$VERSION" \
  bash

#  tmux-s-bash.sh