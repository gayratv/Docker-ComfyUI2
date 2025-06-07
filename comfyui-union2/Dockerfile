# ====== Stage 1: Builder ======
ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"
FROM ${BASE_IMAGE} AS builder

WORKDIR /usr/local/bin
COPY ./bash-scripts/build/*.sh ./
#COPY *.sh ./
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

#RUN --mount=type=cache,target=/root/repo-cache \
#    rm -rf /root/repo-cache/*
#RUN exit 1



# Очистка директории и клонирование ComfyUI
RUN --mount=type=cache,target=/root/repo-cache \
    rm -rf /workspace/* && \
    git-clone-checkout.sh "https://github.com/comfyanonymous/ComfyUI" "$COMFYUI_VERSION" "/root/repo-cache"

WORKDIR /workspace/ComfyUI

COPY nodes.txt  ./

RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    PIP_CACHE_DIR=/root/pip-cache \
    process_repos-install-req-hash.sh "$NODES" false \
    && rm -rf /root/.cache/pip

ARG REQ_MODIFY="base-CUDA-12.4"
COPY requirements-modify ./requirements-modify

ARG PYTORCH_WHEEL="https://download.pytorch.org/whl/cu124"

COPY ./python-prg/*.py ./gayrat_py/

RUN python3 gayrat_py/union-requiere.py \
     && python3 ./gayrat_py/process-req-in.py \
            --requirements-file "requirements.in" \
            --prefixes-file "./requirements-modify/$REQ_MODIFY/remove-lines.txt" \
            --additional-lines-file "./requirements-modify/$REQ_MODIFY/add-lines.txt"

RUN uv pip compile requirements.modify.in -o requirements.out \
        --index-strategy unsafe-best-match \
        --extra-index-url "$PYTORCH_WHEEL" \
        --extra-index-url https://pypi.nvidia.com

RUN python3 ./gayrat_py/pip-pckg-group.py


# Установка пакетов в системную директорию Python 3.11
#    --link-mode=copy \
#    --cache-dir=/root/pip-cache-uv \


# Устанавливаем UV_CACHE_DIR, чтобы uv использовал именно эту директорию для всего своего кеша
ENV UV_CACHE_DIR=/root/pip-cache-uv

RUN --mount=type=cache,target=/root/pip-cache-uv \
    uv pip install \
    --system \
    --index-strategy unsafe-best-match \
    --extra-index-url "$PYTORCH_WHEEL" \
    --extra-index-url https://pypi.nvidia.com \
    -r requirements.out

#    && rm -rf /root/.cache/pip

#в файле
#/workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/cnr_utils.py #есть фрагмент кода
#            if page % 5 == 0:
#                print(f"FETCH ComfyRegistry Data: {page}/{sub_json_obj['totalPages']}")
#надо найти и удалить его

RUN sed -i '/if page % 5 == 0:/,+1d' /workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/cnr_utils.py

RUN python3 /workspace/ComfyUI/gayrat_py/remove_lines.py

#>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=
# ====== Stage 2: Final image ======
#>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=
RUN echo -e "\n\n${COLOR_GREEN}===== Вторая стадия сборки ========${COLOR_RESET}\n"
FROM ${BASE_IMAGE}

# Копируем установленные системные Python-пакеты
RUN echo -e "Копируем установленные системные Python-пакеты"
COPY --from=builder /usr/local/lib/python3.11/dist-packages /usr/local/lib/python3.11/dist-packages

# Копируем рабочую директорию
RUN echo -e "Копируем рабочую директорию"
COPY --from=builder /workspace /workspace

WORKDIR /workspace/ComfyUI
COPY assets-docker/styles.csv ./
COPY input/ ./input/

ENV DOWNLOADS_DIR=/usr/local/bin

WORKDIR /usr/local/bin
COPY ./bash-scripts/build/*.sh $DOWNLOADS_DIR/
COPY ./bash-scripts/*.sh $DOWNLOADS_DIR/
COPY *.sh $DOWNLOADS_DIR/
RUN chmod +x $DOWNLOADS_DIR/*.sh


WORKDIR /workspace/ComfyUI
COPY ./custom-nodes/*.txt ./

ARG NODES

RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    if [ -n "$NODES" ]; then \
        PIP_CACHE_DIR=/root/pip-cache \
        process_repos-install-req-hash.sh "$NODES" true \
        && rm -rf /root/.cache/pip; \
    else \
        echo "Skipping RUN because NODES is set to 'nodes1.txt'"; \
    fi

ARG WORKFLOW_TO_COPY="supir"
COPY workflows/$WORKFLOW_TO_COPY user/default/workflows/$WORKFLOW_TO_COPY
COPY ./user/default/comfy.settings.json user/default/

WORKDIR /workspace/ComfyUI/input
COPY input  ./

WORKDIR /workspace/aria2
COPY aria2 .
RUN chmod +x *.sh \
    && chmod +x ./templates/*.sh \
    && rm -f ./templates/.env

WORKDIR /workspace/templates/models
ARG MODELS
#RUN for dir in */; do [ "$dir" != "$MODELS/" ] && rm -r "$dir"; done

WORKDIR /workspace
RUN echo -e "\n========= POST_INSTALL ===============\n"

ARG POST_INSTALL

COPY post-install/ ./post-install

RUN --mount=type=cache,target=/root/pip-cache \
    if [ -n "$POST_INSTALL" ]; then \
        chmod +x "./post-install/$POST_INSTALL" && \
        echo -e "$COLOR_YELLOW\n\n========= Running $POST_INSTALL ==========$COLOR_RESET"; \
        ./post-install/"$POST_INSTALL"; \
    else \
        echo "Skipping post-install script"; \
    fi

#RUN echo -e "\n\n===========FF========\n" && \
#  ls -la /workspace/ComfyUI/user/default && \
#  ls -la /workspace/ComfyUI/user/default/ComfyUI-Manager
#
#RUN sed -i 's/^security_level = normal/security_level = weak/' /workspace/ComfyUI/user/default/ComfyUI-Manager/config.ini

# УБРАТЬ !!!!
#WORKDIR /workspace/ComfyUI/custom_nodes/ComfyUI_IPAdapter_plus
#COPY ./_temp/utils.py ./

# только для узла Laeyer
#WORKDIR /workspace/ComfyUI/custom_nodes/ComfyUI_LayerStyle_Advance/py
#COPY python-prg/ComfyUI_LayerStyle_Advance/py/gemini.py ./


RUN python3 /workspace/ComfyUI/gayrat_py/remove-models-dirs.py ${MODELS}
#RUN python3 /workspace/ComfyUI/gayrat_py/remove-models-dirs.py ${MODELS} --dry-run

WORKDIR /workspace/ComfyUI



RUN echo "cd /workspace/aria2/templates" >> /root/.bashrc \
  && echo "set -g mouse on" >> /root/.tmux.conf

CMD ["bash"]