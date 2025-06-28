#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

python3 -m pip uninstall -y numpy
python3 -m pip install --cache-dir=/root/pip-cache -U "numpy==2.2.3"

python3 -m pip install --upgrade diffusers transformers accelerate

#pip install --upgrade diffusers transformers accelerate
#pip install mediapipe
#pip install ultralytics


python3 -m pip install  opencv-python mediapipe scipy ultralytics onnxruntime-gpu transformers scikit-image accelerate

pip list | grep numpy

rm -rf /root/.cache/pip