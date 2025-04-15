#!/bin/bash

cd /workspace
git clone https://github.com/ali-vilab/ACE_plus
cd ./ACE_plus/workflow
mv ./ComfyUI-ACE_Plus /workspace/ComfyUI/custom_nodes
echo -f "\npip install scepter\n"
pip install --cache-dir "${PIP_CACHE_DIR:-/root/pip-cache}" scepter
rm -rf /workspace/ACE_plus