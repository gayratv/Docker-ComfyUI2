#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд


#WHEEL_URL="https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.0%2Btorch2.7-cp311-cp311-linux_x86_64.whl"
#WHEEL_FILE="/root/pip-cache/nunchaku-0.3.0+torch2.7-cp311-cp311-linux_x86_64.whl"

# nunchaku-0.3.1+torch2.7-cp311-cp311-linux_x86_64.whl
WHEEL_URL="https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.1%2Btorch2.7-cp311-cp311-linux_x86_64.whl"
WHEEL_FILE="/root/pip-cache/nunchaku-0.3.1+torch2.7-cp311-cp311-linux_x86_64.whl"

# Скачиваем только если файла нет
if [ ! -f "$WHEEL_FILE" ]; then
    curl -L -o "$WHEEL_FILE" "$WHEEL_URL"
fi

pip install --cache-dir=/root/pip-cache "$WHEEL_FILE"
pip install --cache-dir=/root/pip-cache apex
pip install --cache-dir=/root/pip-cache -U "numpy==2.2.3"
rm -rf /root/.cache/pip