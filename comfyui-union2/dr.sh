#!/bin/bash
# file dr.sh

# Загружаем переменные из .env файла
export $(grep -v '^#' .env | xargs)
#echo $GOOGLE_API

echo "run --name $IMAGE_NAME $IMAGE_NAME:$VERSION"
docker rm -f "$IMAGE_NAME"
docker run -it --privileged --gpus all -p 8188:8188 -p 1188:1188 \
    -e "GOOGLE_API=$GOOGLE_API" \
    -e "google_api_key=$GOOGLE_API" \
    -v /mnt/h/ComfyUI-data/models:/workspace/ComfyUI/models \
    --name "$IMAGE_NAME" "$IMAGE_NAME:$VERSION" \
    tmux-s-bash.sh