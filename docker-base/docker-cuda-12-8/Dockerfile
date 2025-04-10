# Стадия 1: Сборка и установка зависимостей
ARG BASE_IMAGE="nvidia/cuda:12.8.1-cudnn-runtime-ubuntu22.04"
FROM ${BASE_IMAGE} AS builder

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
    && apt-get install -y python3.11 python3.11-dev python3.11-venv \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

# Установка pip и wheel
RUN python3.11 -m ensurepip \
    && python3.11 -m pip install --upgrade pip setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

# Установка PyTorch и других зависимостей
RUN --mount=type=cache,target=/root/pip-cache \
    uv pip install --cache-dir=/root/pip-cache --system --index-strategy unsafe-best-match \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128 \
    && uv pip install --cache-dir=/root/pip-cache --system --index-strategy unsafe-best-match \
    xformers pytz \
    && rm -rf ~/.cache/pip

# Стадия 2: Финальный образ
FROM ${BASE_IMAGE} AS final

# Установка минимально необходимых пакетов
RUN apt-get update \
    && apt-get install -y \
    locales \
    libopenblas-dev libomp-dev \
    libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Копирование Python и установленных зависимостей из первой стадии
COPY --from=builder /usr/bin/python3.11 /usr/bin/python3.11
COPY --from=builder /usr/lib/python3.11 /usr/lib/python3.11
COPY --from=builder /root/.local /root/.local

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