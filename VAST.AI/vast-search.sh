#!/bin/bash

cd /mnt/f/_prg/python/Docker-ComfyUI/VAST.AI
source /mnt/f/_prg/python/Docker-ComfyUI/.venv-wsl/bin/activate
export IMAGE_NAME=gayrat/comfyui:v1.5-Fluxtapoz

curl -o vast-search.json -G "https://cloud.vast.ai/api/v0/search/asks/" --data-urlencode \
    'q={
        "gpu_name": {"eq": "RTX 3090"},
        "num_gpus": {"eq": 1},
        "rentable": {"eq": true},
        "cuda_max_good": {"gte": "12.4"},
        "cpu_ram": {"gte": "32000"},
        "inet_down": {"gte": "1000.0"},
        "gpu_frac": {"gte": "0.5"},
        "disk_space": {"gte": "100.0"}
      }'

python3 vast-search-py.py