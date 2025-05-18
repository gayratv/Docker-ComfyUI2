# ====== Stage 1: Builder ======
ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"
FROM ${BASE_IMAGE}

ENV DOWNLOADS_DIR=/usr/local/bin

WORKDIR /usr/local/bin
COPY ./bash-scripts/build/*.sh $DOWNLOADS_DIR/
COPY ./bash-scripts/*.sh $DOWNLOADS_DIR/
COPY *.sh $DOWNLOADS_DIR/
RUN chmod +x $DOWNLOADS_DIR/*.sh


WORKDIR /workspace
ARG CUDA_VER="12.4"

ARG COLOR_GREEN='\033[32m'
ARG COLOR_RED='\033[31m'
ARG COLOR_YELLOW='\033[33m'
ARG COLOR_BOLD_GREEN='\033[1;32m'
ARG COLOR_RESET='\033[0m'

#RUN --mount=type=cache,target=/root/repo-cache \
#    --mount=type=cache,target=/root/pip-cache \
#    --mount=type=cache,target=/root/pip-cache-uv \
#    rm -rf /root/repo-cache/* && \
#    rm -rf /root/pip-cache/* && \
#    rm -rf /root/pip-cache-uv/*
#RUN exit 1



WORKDIR /workspace/

COPY nodes.txt  ./
ARG NODES=nodes.txt

RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    PIP_CACHE_DIR=/root/pip-cache \
    process_repos-install-req-hash.sh "$NODES" true \
    && rm -rf /root/.cache/pip

ARG POST_INSTALL=framepack.sh

COPY post-install ./post-install


RUN --mount=type=cache,target=/root/pip-cache \
    if [ -n "$POST_INSTALL" ]; then \
        chmod +x "./post-install/$POST_INSTALL" && \
        echo -e "$COLOR_YELLOW\n\n========= Running $POST_INSTALL ==========$COLOR_RESET"; \
        ./post-install/"$POST_INSTALL"; \
    else \
        echo "Skipping post-install script"; \
    fi

RUN echo "cd /workspace/aria2/templates" >> /root/.bashrc \
  && echo "set -g mouse on" >> ~/.tmux.conf

CMD ["bash"]