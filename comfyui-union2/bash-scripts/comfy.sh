#!/bin/bash

cd /workspace/ComfyUI
python3 main.py --listen 0.0.0.0 --port 8188 --disable-smart-memory --disable-metadata
#python3 main.py --listen 0.0.0.0 --port 8188 --verbose --disable-smart-memory --disable-metadata

# для карты 5090 рекомендуется использовать sage-attention
# python main.py --use-sage-attention
# pip install sageattention
# для sageattention нужен Triton