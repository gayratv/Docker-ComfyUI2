# ----------------------------------------------------------------------------
# Dockerfile: CUDA 12.8 + Python 3.12 + полный набор dev‑/media‑библиотек
# ----------------------------------------------------------------------------

ARG BASE_IMAGE="nvidia/cuda:12.8.1-cudnn-devel-ubuntu22.04"
FROM ${BASE_IMAGE}

# Неинтерактивный режим APT и фиксированная тайм‑зона
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC

# ----------------------------------------------------------------------------
# Системные инструменты, библиотеки разработки и мультимедиа‑зависимости
# ----------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # --- базовые утилиты -------------------------------------------------- \
    # add-apt-repository, управление PPA
    software-properties-common \
    # make, gcc/g++, ld и др.
    build-essential \
    # явный C++‑компилятор
    g++ \
    # система генерации проектов
    cmake \
    # быстрая система сборки
    ninja-build \
    # cflags/ldflags для lib’ов
    pkg-config \
    # контроль версий
    git \
    # HTTP‑клиент
    curl \
    # альтернативный загрузчик
    wget \
    # многопоточный загрузчик
    aria2 \
    # текстовый редактор
    nano \
    # терминальный мультиплексор
    tmux \
    # синхронизация файлов
    rsync \
    # файловый менеджер
    mc \
    # генерация локалей
    locales \
    # корневые TLS‑сертификаты
    ca-certificates \
    # --- мультимедиа / FFmpeg -------------------------------------------- \
    # системный FFmpeg
    ffmpeg \
    # util‑lib
    libavutil-dev \
    # кодеки
    libavcodec-dev \
    # контейнеры
    libavformat-dev \
    # масштабирование/цвет
    libswscale-dev \
    # Video4Linux2
    libv4l-dev \
    # Xvid MPEG‑4
    libxvidcore-dev \
    # x264 H.264
    libx264-dev \
    # --- библиотеки изображений ----------------------------------------- \
    # JPEG
    libjpeg-dev \
    # PNG
    libpng-dev \
    # TIFF
    libtiff-dev \
    # --- математика / BLAS / параллелизм -------------------------------- \
    # OpenBLAS
    libopenblas-dev \
    # OpenMP runtime
    libomp-dev \
    # ATLAS BLAS
    libatlas-base-dev \
    # Fortran компилятор
    gfortran \
    # --- системные зависимости Python ----------------------------------- \
    # OpenSSL
    libssl-dev \
    # zlib
    zlib1g-dev \
    # bzip2
    libbz2-dev \
    # readline
    libreadline-dev \
    # SQLite3
    libsqlite3-dev \
    # ncurses
    libncursesw5-dev \
    # xz/lzma
    xz-utils \
    # Tk GUI
    tk-dev \
    # FFI
    libffi-dev \
    # LZMA headers
    liblzma-dev \
    # gdbm
    libgdbm-dev \
    # gdbm legacy compat
    libgdbm-compat-dev && \
    # новый компилятор C++
    add-apt-repository -y ppa:ubuntu-toolchain-r/test && \
    apt install -y libstdc++6 gcc-13 g++-13 && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------------------------
# Скачиваем и ставим статическую сборку FFmpeg
# ----------------------------------------------------------------------------
RUN mkdir -p /tmp/ffmpeg && \
    cd /tmp/ffmpeg && \
    wget -q https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz && \
    tar xf ffmpeg-release-amd64-static.tar.xz --strip-components=1 && \
    mv ffmpeg ffprobe /usr/local/bin/ && \
    chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
    cd / && rm -rf /tmp/ffmpeg

# ----------------------------------------------------------------------------
# Установка Python 3.12 + pip + uv
# ----------------------------------------------------------------------------
RUN add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    # пакет python3.12-distutils с версии 3.12 больше не поставляется — distutils удалён из stdlib
    # достаточно базовых пакетов python3.12, dev и venv
    apt-get install -y --no-install-recommends \
        python3.12 \
        python3.12-dev \
        python3.12-venv && \
    curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && \
    python3.12 /tmp/get-pip.py && \
    rm /tmp/get-pip.py && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------------------------
# Симлинки: python / python3 → 3.12
# ----------------------------------------------------------------------------
RUN ln -sf /usr/bin/python3.12 /usr/bin/python3 && \
    ln -sf /usr/bin/python3.12 /usr/bin/python

# ----------------------------------------------------------------------------
# Обновляем pip и базовые инструменты сборки Python‑пакетов
# ----------------------------------------------------------------------------
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel build

# ----------------------------------------------------------------------------
# Генерируем локаль en_US.UTF‑8
# ----------------------------------------------------------------------------
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen && update-locale LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PATH="/root/.local/bin:$PATH"

# ----------------------------------------------------------------------------
# Удобные алиасы (опционально)
# ----------------------------------------------------------------------------
RUN echo "alias py='python3'" >> ~/.bashrc && \
    echo "alias python='python3'" >> ~/.bashrc && \
    echo "alias ptv='python3 -m venv .venv && source .venv/bin/activate'" >> ~/.bashrc

# Команда по умолчанию
CMD ["bash"]
