FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu22.04

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

# Добавление репозитория deadsnakes и установка Python 3.11

RUN add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y python3.11 python3.11-dev python3.11-venv python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb \
    && dpkg -i cloudflared-linux-amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Обновление pip, setuptools и wheel
RUN python3.11 -m pip install --upgrade pip setuptools wheel \
  && rm -rf ~/.cache/pip

#Установка PyTorch:
RUN pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128 \
    && pip3 install --pre xFormers \
    && pip3 install --pre numpy \
    && rm -rf ~/.cache/pip

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

WORKDIR /root/.config/pip
# COPY old/pip.conf constraints.txt ./

# Добавление alias в .bashrc
RUN printf "alias py='python3'\nalias python='python3'\nalias ptest='cd /workspace/VPS-copy && py pytorch-test.py'\n" >> ~/.bashrc

WORKDIR /workspace
COPY VPS-copy .

# Команда по умолчанию
CMD ["bash"]
