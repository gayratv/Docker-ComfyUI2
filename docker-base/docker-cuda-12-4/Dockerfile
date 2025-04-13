ARG BASE_IMAGE_docker_base="pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime"
FROM ${BASE_IMAGE_docker_base}

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
    locales \
    build-essential python3 python3-pip python3-dev libssl-dev libffi-dev zlib1g-dev libbz2-dev \
    && rm -rf /var/lib/apt/lists/*

# libssl-dev : Для работы с SSL/TLS.
# libffi-dev : Для работы с внешними функциями интерфейса (FFI).
# zlib1g-dev : Для работы с сжатием данных.
# libbz2-dev : Для работы с форматом Bzip2. \

# Set non-interactive mode to prevent timezone selection prompts
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
RUN apt-get update \
    && apt-get install -y tzdata \
    && ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime  \
    && dpkg-reconfigure -f noninteractive tzdata \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb \
    && dpkg -i cloudflared-linux-amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# WORKDIR /root/.config/pip
# COPY old/pip.conf constraints.txt ./

# Обновление pip, setuptools и wheel
RUN python3.11 -m pip install --upgrade pip setuptools wheel \
  && pip install pytz \
  && rm -rf ~/.cache/pip

#  && pip install xformers==0.0.29.post2 --index-url https://download.pytorch.org/whl/cu124


# Добавление alias в .bashrc
RUN printf "alias py='python3'\nalias python='python3'\nalias ptest='cd /workspace/VPS-copy && py pytorch-test.py'\n" >> ~/.bashrc

WORKDIR /workspace
COPY VPS-copy .

# Команда по умолчанию
CMD ["bash"]
