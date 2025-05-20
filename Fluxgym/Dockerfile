# ====== Stage 1: Builder ======
ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"
FROM ${BASE_IMAGE} AS builder

WORKDIR /usr/local/bin
COPY ./bash-scripts/build/*.sh ./
RUN chmod +x ./*.sh

WORKDIR /workspace
ARG COMFYUI_VERSION="latest"
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
COPY nodes.txt .

ARG NODES=nodes.txt

RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    if [ -n "$NODES" ]; then \
        PIP_CACHE_DIR=/root/pip-cache \
        process_repos-install-req-hash.sh "$NODES" true \
        && rm -rf /root/.cache/pip; \
    else \
        echo "Skipping RUN because NODES is set to 'nodes1.txt'"; \
    fi

RUN --mount=type=cache,target=/root/pip-cache \
  pip uninstall -y xformers torch typing_extensions \
  && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126 \
  && pip install xformers --index-url https://download.pytorch.org/whl/cu126 \
  && pip install typing_extensions \
  && rm -rf /root/.cache/pip

#rem pip install --no-cache-dir --ignore-installed --force-reinstall --no-warn-conflicts xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu121


WORKDIR /workspace/aria2
COPY aria2 .
RUN chmod +x *.sh \
    && chmod +x ./templates/*.sh \
    && rm -f ./templates/.env

RUN mv /workspace/ComfyUI/custom_nodes/fluxgym /workspace/ \
  && mv /workspace/ComfyUI/custom_nodes/sd-scripts /workspace/fluxgym/

WORKDIR /workspace/fluxgym

RUN echo "cd /workspace/aria2/templates" >> /root/.bashrc \
  && echo "set -g mouse on" >> ~/.tmux.conf

CMD ["bash"]