#!/bin/bash

set -e  # Выход при ошибке

echo -e "\n===================\n"
echo -e "\033[34mБлок коррекции установленных пакетов\033[0m"

set -x  # Логирование всех команд

python3 -m pip uninstall -y torch torchvision torchaudio

python3 -m pip install --cache-dir=/root/pip-cache \
  torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

rm -rf /root/.cache/pip

