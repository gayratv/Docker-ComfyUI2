#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

#pip uninstall -y opencv-contrib-python numpy

pip install --cache-dir=/root/pip-cache torchvision
#pip install torchcodec --index-url=https://download.pytorch.org/whl/cu126 --cache-dir=/root/pip-cache
pip install torchcodec --index-url=https://download.pytorch.org/whl/cu128 --cache-dir=/root/pip-cache
# torchcodec 0.4.0+cu128

rm -rf /root/.cache/pip
