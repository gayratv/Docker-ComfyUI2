#!/bin/bash
# file dr.sh

# Загружаем переменные из .env файла
export $(grep -v '^#' .env | xargs)
#echo $GOOGLE_API

echo "run --name $IMAGE_NAME $IMAGE_NAME:$VERSION"
docker rm -f "$IMAGE_NAME"
docker run -it --privileged --gpus all -p 7860:7860  \
    -v /mnt/h/ComfyUI-data/models:/workspace/ComfyUI/models \
    --name "$IMAGE_NAME" "$IMAGE_NAME:$VERSION" \
    bash
#    tmux-s.sh
#    tmux-s-bash.sh