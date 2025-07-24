# Сборка
FROM cuda-12-6:nvidia-devel AS builder
WORKDIR /workspace/
RUN git clone https://github.com/thu-ml/SageAttention.git
WORKDIR /workspace/SageAttention

RUN python3 -m pip install --upgrade pip

RUN --mount=type=cache,target=/root/pip-cache \
  python3 -m pip install --cache-dir=/root/pip-cache packaging


RUN --mount=type=cache,target=/root/pip-cache \
  python3 -m pip install --cache-dir=/root/pip-cache  torch==2.7.0 torchaudio==2.7.0 \
    --extra-index-url https://download.pytorch.org/whl/cu126

RUN --mount=type=cache,target=/root/pip-cache \
  python3 -m pip install --cache-dir=/root/pip-cache numpy

# parallel compiling (Optional)
ENV TORCH_CUDA_ARCH_LIST="7.5;8.6;8.9"
ENV EXT_PARALLEL=4
ENV NVCC_APPEND_FLAGS="--threads 8"
ENV MAX_JOBS=32


RUN  python3 setup.py install
#RUN --mount=type=cache,target=/root/pip-cache \
#  python3 -m pip install  --cache-dir=/root/pip-cache   -e .
#RUN  python3 -m pip install  -e .


# Стадия 1: Сборка и установка зависимостей
FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu22.04

# Установка необходимых пакетов
RUN apt-get update \
    && apt-get install -y \
    software-properties-common \
    curl \
    wget \
    aria2 \
    git \
    nano \
    ffmpeg \
    locales \
    tmux \
    rsync \
    mc \
    ffmpeg libavutil-dev  \
    build-essential g++ cmake ninja-build git pkg-config libopenblas-dev libomp-dev \
    libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran \
    && rm -rf /var/lib/apt/lists/*


ARG INSTALL_tensorrt="false"

# Устанавливаем переменные окружения, чтобы apt не задавал интерактивных вопросов
ENV DEBIAN_FRONTEND=noninteractive

# Условная установка TensorRT
RUN if [ "${INSTALL_tensorrt}" = "true" ]; then \
      echo ">>> Installing TensorRT as INSTALL_tensorrt=true"; \
      apt-get update && \
      apt-get install -y --no-install-recommends wget gnupg ca-certificates && \
      wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb && \
      dpkg -i cuda-keyring_1.1-1_all.deb && \
      rm cuda-keyring_1.1-1_all.deb && \
      apt-get update && \
      apt-get install -y tensorrt && \
      apt-get clean && \
      rm -rf /var/lib/apt/lists/*; \
    else \
      echo ">>> Skipping TensorRT installation"; \
    fi

# Сбрасываем переменную окружения
ENV DEBIAN_FRONTEND=


# Использование статической сборки FFmpeg
# Скачайте готовую статическую сборку
RUN mkdir -p /tmp && \
    cd /tmp  && \
    wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz   && \
# Распакуйте
    tar xf ffmpeg-release-amd64-static.tar.xz   && \
# Переместите в систему
    cd ffmpeg-*-amd64-static/   && \
    mv ffmpeg /usr/local/bin/   && \
    mv ffprobe /usr/local/bin/   && \
# Сделайте исполняемыми
    chmod +x /usr/local/bin/ffmpeg   && \
    chmod +x /usr/local/bin/ffprobe   && \
# Проверьте версию
    ffmpeg -version


# Set non-interactive mode to prevent timezone selection prompts
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC

# Установка Python 3.11
RUN apt-get update \
    && apt-get install -y tzdata \
    && ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime  \
    && dpkg-reconfigure -f noninteractive tzdata \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y  \
      python3.11 \
      python3.11-dev \
      python3.11-venv \
      python3.11-distutils \
    && curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.11 get-pip.py \
    && rm get-pip.py \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем python3.11 как основной python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
  && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 3 \
  && update-alternatives --set python3 /usr/bin/python3.11

# This RUN instruction should create and manage the /usr/bin/python link
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 3 \
    && update-alternatives --set python /usr/bin/python3.11

# Установка pip и wheel
RUN python3 -m ensurepip --upgrade \
    && python3.11 -m pip install --upgrade pip setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

# Установка минимально необходимых пакетов
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Настройка локали
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PATH="/root/.local/bin:$PATH"

# Установка алиасов
RUN printf "alias py='python3'\nalias python='python3'\nalias ptest='cd /workspace/VPS-copy && py pytorch-test.py'\n" >> ~/.bashrc

RUN python3 -m pip install --upgrade pip

COPY --from=builder /usr/local/lib/python3.11/dist-packages/sageattention* /usr/local/lib/python3.11/dist-packages/

# Команда по умолчанию
CMD ["bash"]