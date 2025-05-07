#!/bin/bash

echo -e"====== SUPIR-v2-MaskTile.sh ============"

pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python-headless opencv-contrib-python

uv pip install \
    --link-mode=copy \
    --system \
    --cache-dir=/root/pip-cache \
    opencv-contrib-python \
    && rm -rf root/.cache/pip

