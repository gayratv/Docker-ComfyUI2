#!/bin/bash

# Core dependencies
pip install \
  Pillow>=10.3.0 \
  opencv-python-headless>=4.7.0.72 \
  scipy>=1.11.4 \
  numpy==1.26.4 \
  einops>=0.7.0 \
  accelerate>=0.26.0 \
  huggingface_hub>=0.23.4 \
  transformers>=4.45.0 \
  diffusers>=0.31.0 \
  safetensors>=0.4.2 \
  bitsandbytes>=0.41.1 \
  onnxruntime-gpu \
  PyGithub \
  openai>=1.0.0 \
  replicate \
  google-generativeai \
  zhipuai \
  albumentations \
  kornia>=0.7.1 \
  imageio-ffmpeg>=0.4.0 \
  rembg[gpu] \
  segment-anything \
  transparent-background \
  tqdm>=4.62.0 \
  requests>=2.31.0 \
  aiohttp>=3.11.8 \
  psutil \
  typer \
  rich \
  loguru \
  pyyaml \
  configparser>=5.0.0 \
  dill \
  filelock>=3.0.12 \
  json-repair \
  prettytable \
  qrcode \
  wget \
  deepspeed==0.4.0 \
  peft>=0.12.0 \
  loralib>=0.1.2 \
  torchmetrics==0.10.3 \
  torchsde \
  faster_whisper \
  soundfile>=0.12.1 \
  av \
  protobuf==5.26.1


# Дополнительные зависимости
pip install \
  GitPython \
  gradio>=3.0.0 \
  uv \
  fal-client \
  submitit \
  redis \
  boto3==1.34.86 \
  matrix-client==0.4.0 \
  mediapipe \
  svglib \
  trimesh>=4.0.5 \
  colour-science \
  addict \
  omegaconf>=2.3.0 \
  hydra-core>=1.3.2 \
  numba \
  mypy \
  pytest>=7.8.0 \
  pytest-aiohttp \
  pytest-asyncio \
  yapf \
  gguf>=0.13.0 \
  clip-interrogator==0.6.0 \
  color-matcher \
  blind-watermark \
  blobfile \
  ftfy \
  fvcore \
  scenedetect[opencv-headless] \
  pymatting \
  pycryptodome>=3.15.0 \
  pyOpenSSL \
  pyarrow \
  pycocoevalcap \
  pycocotools \
  sentencepiece \
  tokenizers>=0.13.3 \
  torchscale==0.2.0 \
  ultralytics>=8.2.0 \
  watchdog \
  scikit-learn

# Специфические пакеты из вашего списка
pip install \
  comfyui-frontend-package==1.12.14 \
  git+https://github.com/openai/swarm.git \
  git+https://github.com/shadowcz007/SenseVoice-python.git

# Для CUDA-зависимостей [[2]]
pip install --extra-index-url https://pypi.nvidia.com

rm -rf ~/.cache/pip