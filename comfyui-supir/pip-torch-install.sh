#!/bin/bash
pip install torch==2.6.0+cu124 torchvision==0.21.0+cu124 torchaudio==2.6.0+cu124 \
  --extra-index-url https://download.pytorch.org/whl/cu124

pip install --upgrade xformers protobuf