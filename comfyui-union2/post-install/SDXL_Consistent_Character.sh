#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

python3 -m pip install insightface onnx onnxruntime

rm -rf /root/.cache/pip

