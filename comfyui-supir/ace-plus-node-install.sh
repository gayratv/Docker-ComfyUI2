#!/bin/bash

cd /workspace
git clone https://github.com/ali-vilab/ACE_plus
cd ./ACE_plus/workflow
mv ./ComfyUI-ACE_Plus /workspace/ComfyUI/custom_nodes
rm -rf /workspace/ACE_plus


# ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
# transparent-background 1.3.3 requires albucore==0.0.16,
# but you have albucore 0.0.23 which is incompatible.

echo -f "\npip install scepter\n"
cd /workspace
pip install --cache-dir "${PIP_CACHE_DIR:-/root/pip-cache}" transparent-background
pip install --cache-dir "${PIP_CACHE_DIR:-/root/pip-cache}" scepter
# pip install --no-cache-dir scepter

pip uninstall -y opencv-python opencv-python-headless opencv-contrib-python-headless opencv-contrib-python
pip install --no-cache-dir opencv-contrib-python