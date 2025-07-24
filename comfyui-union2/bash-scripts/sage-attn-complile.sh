#!/bin/bash

cd /workspace
git clone https://github.com/thu-ml/SageAttention.git
cd /workspace/SageAttention

# Карты 3090 4090
export TORCH_CUDA_ARCH_LIST="8.6;8.9+PTX"

#для карты 5090
#export TORCH_CUDA_ARCH_LIST="12.0+PTX"

export EXT_PARALLEL=4
export NVCC_APPEND_FLAGS="--threads 8"
export MAX_JOBS=32
export FORCE_CUDA=1

#python3 -m pip install -e .

python3 setup.py install

#python3 setup.py bdist_wheel

pip list | grep sage
pip list | grep onnx
pip list | grep torch
