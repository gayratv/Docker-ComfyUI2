# Определяем аргумент для базового образа
ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}



ENV DOWNLOADS_DIR=/usr/local/bin
COPY *.sh $DOWNLOADS_DIR/
RUN chmod +x $DOWNLOADS_DIR/*.sh

WORKDIR /workspace/ComfyUI
COPY nodes*.txt ./

# нунчаки
#RUN --mount=type=cache,target=/root/git-cache \
#    git clone https://github.com/asomoza/image_gen_aux.git /root/git-cache/image_gen_aux

# Stage 1: Clone the repository (only if it doesn't already exist)
RUN --mount=type=cache,target=/root/git-cache \
    if [ ! -d "/root/git-cache/image_gen_aux" ]; then \
        git clone https://github.com/asomoza/image_gen_aux.git /root/git-cache/image_gen_aux; \
    else \
        echo "Directory /root/git-cache/image_gen_aux already exists. Skipping git clone."; \
    fi

# Stage 1: Cache the .whl file
RUN --mount=type=cache,target=/root/wheel-cache \
    if [ ! -f "/root/wheel-cache/nunchaku-0.1.4+torch2.5-cp311-cp311-linux_x86_64.whl" ]; then \
        wget -O /root/wheel-cache/nunchaku-0.1.4+torch2.5-cp311-cp311-linux_x86_64.whl \
        https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.1.4%2Btorch2.5-cp311-cp311-linux_x86_64.whl; \
    else \
        echo "File /root/wheel-cache/nunchaku-0.1.4+torch2.5-cp311-cp311-linux_x86_64.whl already cached. Skipping download."; \
    fi

RUN --mount=type=cache,target=/root/pip-cache \
    --mount=type=cache,target=/root/git-cache \
    --mount=type=cache,target=/root/wheel-cache \
    pip install /root/wheel-cache/nunchaku-0.1.4+torch2.5-cp311-cp311-linux_x86_64.whl \
    && pip install /root/git-cache/image_gen_aux \
    && rm -rf ~/.cache/pip

# Создаем ARG для передачи списка файлов
ARG NODES="nodes-nunchaki.txt"

# Кэшируем зависимости и выполняем установку для каждого файла
RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    PIP_CACHE_DIR=/root/pip-cache \
    process_repos-install-req.sh "$NODES" \
    && rm -rf ~/.cache/pip

WORKDIR /workspace/
COPY nunchaki-test.py ./

WORKDIR /workspace/ComfyUI
COPY workflows/ user/default/workflows/
#COPY comfy.settings.json user/default/

WORKDIR /workspace/aria2
COPY aria2 .
RUN chmod +x *.sh \
    && chmod +x ./templates/*.sh

RUN echo "cd /workspace" >> /root/.bashrc \
  && echo "set -g mouse on" >> ~/.tmux.conf

CMD ["bash"]