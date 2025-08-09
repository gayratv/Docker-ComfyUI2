#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

echo -e "\033[34mБлок коррекции установленных пакетов\033[0m"

python3 -m pip uninstall -y torch torchvision torchaudio

python3 -m pip install --cache-dir=/root/pip-cache \
  torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
#  triton входит в стандартную установку
#python3 -m pip install triton

# ========================== блок коррекции установленных пакетов
python3 -m pip uninstall -y onnxruntime onnxruntime-gpu xformers

python3 -m pip install --cache-dir=/root/pip-cache onnxruntime-gpu hf_transfer

python3 -m pip install  --cache-dir=/root/pip-cache xformers sageattention
# ==========================

rm -rf /root/.cache/pip

