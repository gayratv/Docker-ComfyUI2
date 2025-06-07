#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

#pip install https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.2.0%2Btorch2.7-cp311-cp311-linux_x86_64.whl
pip install --cache-dir=/root/pip-cache  https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.0%2Btorch2.7-cp311-cp311-linux_x86_64.whl

# nunchaku-0.3.0+torch2.7-cp311-cp311-linux_x86_64.whl
# https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.0%2Btorch2.7-cp311-cp311-linux_x86_64.whl

#thinc 8.3.6 requires numpy<3.0.0,>=2.0.0, but you have numpy 1.26.4 which is incompatible.
#mediapipe 0.10.21 requires numpy<2, but you have numpy 2.2.0 which is incompatible.

pip install --cache-dir=/root/pip-cache  apex numpy==2.0.0

rm -rf /root/.cache/pip

