#!/bin/bash
# file dr.sh

# Загружаем переменные из .env файла
#export $(grep -v '^#' .env | xargs)
#echo $GOOGLE_API

#export MODELS="SDXL_Consistent_Character"

echo "run --name $IMAGE_NAME $IMAGE_NAME:$VERSION"
docker rm -f "$IMAGE_NAME"

#    -e WAS_CONFIG_DIR=/workspace/WAS_node \
docker run -it --privileged --gpus all \
    -e MODELS=$MODELS \
     --name "$IMAGE_NAME" "$IMAGE_NAME:$VERSION" \
    bash

