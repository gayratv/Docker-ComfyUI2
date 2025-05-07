# Определяем аргумент для базового образа
ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}

#===============================
#===============================


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

RUN --mount=type=cache,target=/root/repo-cache \
    if [ ! -d ".git" ]; then \
        echo "Cloning ComfyUI..." && \
        git clone https://github.com/comfyanonymous/ComfyUI . ; \
    else \
        echo "Using cached repo"; \
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

#===============================

#RUN rm -rf /root/repo-cache \
#    && rm -rf /root/pip-cache

# Создаём кэширующие директории явно
RUN mkdir -p /root/pip-cache/wheels

ENV DOWNLOADS_DIR=/usr/local/bin
COPY *.sh $DOWNLOADS_DIR/
RUN chmod +x $DOWNLOADS_DIR/*.sh

WORKDIR /workspace/ComfyUI
# шаг 11
COPY ./custom-nodes/nodes*.txt ./

# Создаем ARG для передачи списка файлов
ARG NODES="nodes1.txt"

# шаг 12 Кэшируем зависимости и выполняем установку для каждого файла
RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    if [ "$NODES" != "nodes1.txt" ]; then \
        PIP_CACHE_DIR=/root/pip-cache \
        process_repos-install-req.sh "$NODES" \
        && rm -rf /root/.cache/pip; \
    else \
        echo "Skipping RUN because NODES is set to 'nodes1.txt'"; \
    fi

#        process_repos-git-clone.sh "$NODES" \


WORKDIR /workspace/ComfyUI
ARG WORKFLOW_TO_COPY="supir"
COPY workflows/$WORKFLOW_TO_COPY user/default/workflows/$WORKFLOW_TO_COPY
COPY ./user/default/comfy.settings.json user/default/

COPY union-requiere.py VPS-copy  ./

WORKDIR /workspace/ComfyUI/input
COPY input  ./

WORKDIR /workspace/aria2
COPY aria2 .
RUN chmod +x *.sh \
    && chmod +x ./templates/*.sh \
    && rm -f ./templates/.env

WORKDIR /workspace/aria2/templates/models
ARG MODELS="nunchaku"
#RUN for dir in */; do [ "$dir" != "nunchaku/" ] && rm -r "$dir"; done

WORKDIR /workspace
RUN echo -e "\n========= POST_INSTALL ===============\n"
# 21

ARG POST_INSTALL
RUN echo -e "\n\nPOST_INSTALL =|$POST_INSTALL|"

COPY post-install/ ./post-install

RUN --mount=type=cache,target=/root/pip-cache \
    if [ -n "$POST_INSTALL"  ]; then \
        chmod +x "./post-install/$POST_INSTALL" && \
        echo "Running $POST_INSTALL./"; \
        ./post-install/"$POST_INSTALL"; \
        echo -e "--------- ls -la /root/pip-cache/wheels; "; \
#        ls -la /root/pip-cache/wheels; \
    else \
        echo "Skipping post-install script"; \
    fi
#    && echo "Checking cache contents:" \
#    && find /root/pip-cache/wheels -type f -name "*.whl" -exec ls -lh {} \;

WORKDIR /workspace/ComfyUI/custom_nodes
COPY union-requiere.py .
RUN python3 union-requiere.py \
  && rm union-requiere.py


RUN echo "cd /workspace/aria2/templates" >> /root/.bashrc \
  && echo "set -g mouse on" >> ~/.tmux.conf
#  tmux source-file ~/.tmux.conf


CMD ["bash"]