#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless

pip install --cache-dir=/root/pip-cache opencv-python==4.7.0.72
#pip install --cache-dir=/root/pip-cache -U "numpy==2.2.3"

rm -rf /root/.cache/pip