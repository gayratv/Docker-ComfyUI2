#!/bin/bash

echo "run --name $IMAGE_NAME $IMAGE_NAME:$VERSION"
docker rm -f "$IMAGE_NAME"

# --runtime=nvidia
#--gpus all \

docker run \
  -it \
  --runtime=nvidia \
  --name "$IMAGE_NAME" "$IMAGE_NAME:$VERSION"


