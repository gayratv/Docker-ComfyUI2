#!/bin/bash

source /workspace/.venv/bin/activate
cd /workspace/ComfyUI
python main.py  --listen 0.0.0.0 --port 8188
