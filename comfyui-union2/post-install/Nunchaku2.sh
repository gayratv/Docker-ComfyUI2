#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

# pip install torch==2.6 torchvision==0.21 torchaudio==2.6

# nunchaku-0.3.1+torch2.7-cp311-cp311-linux_x86_64.whl

python3 -m pip install --cache-dir=/root/pip-cache xformers

python3 -m pip install --cache-dir=/root/pip-cache \
  https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.1%2Btorch2.7-cp311-cp311-linux_x86_64.whl

rm -rf /root/.cache/pip

