#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

#pip install https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.2.0%2Btorch2.7-cp311-cp311-linux_x86_64.whl
pip install --cache-dir=/root/pip-cache  https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.0%2Btorch2.7-cp311-cp311-linux_x86_64.whl

rm -rf /root/.cache/pip

