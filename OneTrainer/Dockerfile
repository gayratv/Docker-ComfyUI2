# Note: as of April 2025, this Dockerfile is outdated and requires adjustments

# Inspiration for setup @ https://dev.to/ordigital/nvidia-525-cuda-118-python-310-pytorch-gpu-docker-image-1l4a
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

ENV PYTHONUNBUFFERED=1

# SYSTEM
RUN apt-get update --yes --quiet && DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    software-properties-common \
    apt-utils \
    wget curl vim git ca-certificates kmod \
    nvidia-driver-525 \
 && rm -rf /var/lib/apt/lists/*

RUN apt-get update -y && apt-get install -y \
    aria2 \
    nano \
    ffmpeg \
    locales \
    tmux \
    mc \
    build-essential g++ cmake ninja-build git pkg-config libopenblas-dev libomp-dev \
    libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# PYTHON 3.10
RUN add-apt-repository --yes ppa:deadsnakes/ppa && apt-get update --yes --quiet
RUN DEBIAN_FRONTEND=noninteractive apt-get install --yes --quiet --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    python3.10-lib2to3 \
    python3.10-gdbm \
    python3.10-tk \
    pip

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 999 \
    && update-alternatives --config python3 && ln -s /usr/bin/python3 /usr/bin/python

RUN pip install --upgrade pip

# Create and set the working directory
#RUN mkdir -p /OneTrainer
#WORKDIR /OneTrainer
WORKDIR /

RUN git clone https://github.com/Nerogar/OneTrainer

# Copy the current directory's contents to the container image
#COPY . /OneTrainer
WORKDIR /OneTrainer

# Install requirements
RUN python3 --version

RUN --mount=type=cache,target=/root/pip-cache \
    pip install --cache-dir=/root/pip-cache -r requirements.txt


WORKDIR /usr/local/bin
COPY *.sh ./
RUN chmod +x ./*.sh

WORKDIR /OneTrainer

# Run the training UI
CMD ["python3", "scripts/train_ui.py"]