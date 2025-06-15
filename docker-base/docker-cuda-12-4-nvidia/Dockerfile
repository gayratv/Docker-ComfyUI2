# Стадия 1: Сборка и установка зависимостей
ARG BASE_IMAGE="nvidia/cuda:12.6.3-cudnn-runtime-ubuntu22.04"
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
    tmux \
    rsync \
    mc \
    ffmpeg libavutil-dev  \
    build-essential g++ cmake ninja-build git pkg-config libopenblas-dev libomp-dev \
    libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran \
    && rm -rf /var/lib/apt/lists/*


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
  && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2 \
  && update-alternatives --set python3 /usr/bin/python3.11

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

# Команда по умолчанию
CMD ["bash"]