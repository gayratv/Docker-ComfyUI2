# Стадия 1: Сборка и установка зависимостей
ARG BASE_IMAGE="nvidia/cuda:12.8.1-cudnn-runtime-ubuntu22.04"
FROM ${BASE_IMAGE}

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
    build-essential g++ cmake ninja-build git pkg-config libopenblas-dev libomp-dev \
    libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

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
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/python3.11 /usr/local/bin/python && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

ENV PATH="/root/.local/bin:$PATH"

# Установка pip и wheel
RUN python3.11 -m ensurepip \
    && python3.11 -m pip install --upgrade pip setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

# Установка PyTorch и других зависимостей
RUN --mount=type=cache,target=/root/pip-cache \
    uv pip install \
    --cache-dir=/root/pip-cache  \
    --system \
    --index-strategy unsafe-best-match \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128 \
    && uv pip install --cache-dir=/root/pip-cache --system --index-strategy unsafe-best-match \
    pytz \
    && rm -rf ~/.cache/pip

# xformers пока не буду ставить - убивает torch
#    xformers pytz \

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

# Рабочая директория
WORKDIR /workspace
COPY VPS-copy .

# Команда по умолчанию
CMD ["bash"]