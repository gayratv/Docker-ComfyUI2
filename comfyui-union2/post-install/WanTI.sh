#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

# цель triton 3.3 и Sage 2.2)


python3 -m pip uninstall -y triton torch torchaudio sageattention

# Для карты 5090
#python3 -m pip install --cache-dir=/root/pip-cache triton==3.3.1 torch==2.7.1 torchaudio==2.7.1 \
#  --extra-index-url https://download.pytorch.org/whl/cu128

python3 -m pip install --cache-dir=/root/pip-cache triton==3.3.1 torch==2.7.1 torchaudio==2.7.1 \
  --extra-index-url https://download.pytorch.org/whl/cu126


# xformers==0.0.30

# Для карты 5090
#python3 -m pip install --cache-dir=/root/pip-cache /workspace/wheels/sageattention_wheel/Kija/sageattention-*.whl
python3 -m pip install --cache-dir=/root/pip-cache /workspace/wheels/sageattention_wheel/sageattention-*.whl

# обновим Frontend
python3 -m pip uninstall -y comfyui-frontend-package
python3 -m pip install --cache-dir=/root/pip-cache pip install comfyui-frontend-package==1.25.1



#rm /workspace/wheels/sageattention-*.whl
rm -rf /root/.cache/pip

