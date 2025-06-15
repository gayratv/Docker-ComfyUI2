#!/bin/bash

cd /workspace/ComfyUI
python3 main.py --listen 0.0.0.0 --port 8188 --disable-smart-memory --disable-metadata
#python3 main.py --listen 0.0.0.0 --port 8188 --verbose --disable-smart-memory --disable-metadata
