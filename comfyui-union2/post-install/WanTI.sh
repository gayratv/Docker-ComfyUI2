#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

# цель triton 3.3 и Sage 2.2)
# pip list | grep triton
# =================

python3 -m pip install --cache-dir=/root/pip-cache torch==2.7.0 torchaudio==2.7.0 \
  --extra-index-url https://download.pytorch.org/whl/cu126
# xformers==0.0.30

python3 -m pip install --cache-dir=/root/pip-cache /workspace/wheels/sageattention-*.whl

rm /workspace/wheels/sageattention-*.whl
rm -rf /root/.cache/pip

