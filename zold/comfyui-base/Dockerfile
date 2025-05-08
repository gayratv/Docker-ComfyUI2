# Определяем аргумент для базового образа
ARG BASE_IMAGE="comfyui-base-cuda"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}

#RUN rm -rf /root/pip-cache \
#    rm -rf /root/pip-cache-uv \
#    rm -rf /root/repo-cache
#RUN uv cache clean --cache-dir=/root/pip-cache-uv

WORKDIR /usr/local/bin
COPY *.sh ./
RUN chmod +x ./*.sh

WORKDIR /workspace
ARG COMFYUI_VERSION="latest"
ARG CUDA_VER="12.4"

RUN if [ "$COMFYUI_VERSION" = "latest" ]; then \
        git clone https://github.com/comfyanonymous/ComfyUI; \
    else \
        git clone --branch $COMFYUI_VERSION https://github.com/comfyanonymous/ComfyUI; \
    fi

WORKDIR /workspace/ComfyUI

COPY cloudflare.py nodes.txt *.py ./

ARG NODES="nodes.txt"
RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    PIP_CACHE_DIR=/root/pip-cache \
    process_repos-install-req.sh "$NODES" false \
    && rm -rf root/.cache/pip

ARG REQ_MODIFY="base-CUDA-12.4"
COPY requirements-modify ./requirements-modify

RUN  python3 union-requiere.py \
     && python3 process-req-in.py \
            --requirements-file "requirements.in" \
            --prefixes-file "./requirements-modify/$REQ_MODIFY/remove-lines.txt" \
            --additional-lines-file "./requirements-modify/$REQ_MODIFY/add-lines.txt";

RUN uv pip compile requirements.modify.in -o requirements.out \
        --index-strategy unsafe-best-match \
        --extra-index-url https://download.pytorch.org/whl/cu124 \
        --extra-index-url https://pypi.nvidia.com

     # Разбиение скомпилированных пакетов на группы
RUN python3 pip-pckg-group.py

RUN --mount=type=cache,target=/root/pip-cache-uv \
    uv pip install \
    --link-mode=copy \
    --system \
    --cache-dir=/root/pip-cache-uv \
    --index-strategy unsafe-best-match \
    --extra-index-url https://download.pytorch.org/whl/cu124 \
    --extra-index-url https://pypi.nvidia.com \
    -r requirements.out \
#    && rm -rf /root/.cache/pip
    && echo "RUN UV2 --------" \
#RUN --mount=type=cache,target=/root/pip-cache-uv \
    && uv pip install \
    --upgrade \
    --system \
    --cache-dir=/root/pip-cache-uv \
    --index-strategy unsafe-best-match \
    --extra-index-url https://download.pytorch.org/whl/cu124 \
    --extra-index-url https://pypi.nvidia.com \
    numpy \
    && rm -rf /root/.cache/pip

WORKDIR /workspace/ComfyUI

RUN echo "cd /workspace" >> /root/.bashrc

CMD ["bash"]
