#!/bin/bash

docker cp "$IMAGE_NAME":/workspace/ComfyUI/requirements.in ./old/
docker cp "$IMAGE_NAME":/workspace/ComfyUI/requirements.modify.in ./old/
docker cp "$IMAGE_NAME":/workspace/ComfyUI/requirements.out ./old/