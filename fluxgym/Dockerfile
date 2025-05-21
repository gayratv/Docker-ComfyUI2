# Base image with CUDA 12.4
FROM nvidia/cuda:12.4.1-base-ubuntu22.04

RUN apt-get update -y && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    software-properties-common \
    curl \
    wget \
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

# Define environment variables for UID and GID and local timezone
ENV PUID=${PUID:-1000}
ENV PGID=${PGID:-1000}

# Create a group with the specified GID
RUN groupadd -g "${PGID}" appuser
# Create a user with the specified UID and GID
RUN useradd -m -s /bin/sh -u "${PUID}" -g "${PGID}" appuser

WORKDIR /app

# Get sd-scripts from kohya-ss and install them
RUN --mount=type=cache,target=/root/pip-cache \
    git clone -b sd3 https://github.com/kohya-ss/sd-scripts && \
    cd sd-scripts && \
    pip install --cache-dir=/root/pip-cache  -r ./requirements.txt

# Install main application dependencies
COPY ./requirements.txt ./requirements.txt
RUN --mount=type=cache,target=/root/pip-cache \
    pip install --cache-dir=/root/pip-cache -r ./requirements.txt


# Install Torch, Torchvision, and Torchaudio for CUDA 12.4
RUN --mount=type=cache,target=/root/pip-cache \
    pip install --cache-dir=/root/pip-cache  torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

RUN chown -R appuser:appuser /app

# delete redundant requirements.txt and sd-scripts directory within the container
#RUN rm -r ./sd-scripts
#RUN rm ./requirements.txt

#Run application as non-root
#USER appuser

WORKDIR /app
# Copy fluxgym application code
COPY . ./fluxgym


WORKDIR /usr/local/bin
COPY *.sh ./
RUN chmod +x ./*.sh

EXPOSE 7860

ENV GRADIO_SERVER_NAME="0.0.0.0"

WORKDIR /app/fluxgym

# Run fluxgym Python application
CMD ["python3", "./app.py"]