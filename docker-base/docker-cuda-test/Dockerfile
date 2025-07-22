FROM nvidia/cuda:12.6.3-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

#Устанавливаем Python3 и pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3 python3-distutils python3-dev wget ca-certificates && \
    wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && rm get-pip.py && \
    rm -rf /var/lib/apt/lists/*

#Устанавливаем PyTorch с поддержкой CUDA
RUN --mount=type=cache,target=/root/pip-cache \
  python3 -m pip install --cache-dir=/root/pip-cache \
    torch torchvision \
    --extra-index-url https://download.pytorch.org/whl/cu126

#Копируем скрипт для проверки CUDA
COPY check_cuda.py /opt/check_cuda.py
WORKDIR /opt

#Запускаем при старте
CMD ["python3", "check_cuda.py"]