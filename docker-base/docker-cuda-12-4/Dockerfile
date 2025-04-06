# Базовый образ с CUDA 12.4 и PyTorch 2.4.0
# FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

ARG BASE_IMAGE="pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime"
FROM ${BASE_IMAGE}

RUN apt-get update  \
    && apt-get install -y \
    software-properties-common \
    curl \
    wget \
    aria2 \
    git \
    mc \
    nano \
    ffmpeg \
    nethogs \
    net-tools \
    gpg-agent \
    tmux \
    build-essential g++ cmake ninja-build libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Set non-interactive mode to prevent timezone selection prompts
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
RUN apt-get update \
    && apt-get install -y tzdata \
    && ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime  \
    && dpkg-reconfigure -f noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb \
    && dpkg -i cloudflared-linux-amd64.deb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/.config/pip
#COPY old/pip.conf constraints.txt ./

# Обновление pip, setuptools и wheel
RUN python3.11 -m pip install --upgrade pip setuptools wheel \
  && pip install numpy pytz \
  && rm -rf ~/.cache/pip

#  && pip install xformers==0.0.29.post2 --index-url https://download.pytorch.org/whl/cu124


# Добавление alias в .bashrc
RUN printf "alias py='python3'\nalias python='python3'\nalias ptest='cd /workspace/VPS-copy && py pytorch-test.py'\n" >> ~/.bashrc

WORKDIR /workspace
COPY VPS-copy .

# Команда по умолчанию
CMD ["bash"]
