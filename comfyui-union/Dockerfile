ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}

#RUN rm -rf /root/pip-cache \
#    rm -rf /root/repo-cache

WORKDIR /workspace


ARG COMFYUI_VERSION
ARG CUDA_VER="12.4"

RUN git clone https://github.com/comfyanonymous/ComfyUI \
    && if [ -n "$COMFYUI_VERSION" ]; then \
        cd ComfyUI \
        && git checkout "$COMFYUI_VERSION"; \
    fi

WORKDIR /workspace/ComfyUI

COPY *.sh nodes.txt *.py ./


RUN --mount=type=cache,target=/root/pip-cache \
    --mount=type=cache,target=/root/repo-cache \
    PIP_CACHE_DIR=/root/pip-cache \
    && chmod +x *.sh \
    && ./process_repos-install-req.sh nodes.txt false


#RUN --mount=type=cache,target=/root/pip-cache \
#    --mount=type=cache,target=/root/repo-cache \
#    PIP_CACHE_DIR=/root/pip-cache \
#    && echo -e "\033[0;31m \n\n Установка дополнительных пакетов \033[0m" \
#    && uv pip install \
#    --link-mode=copy \
#    --system \
#    --cache-dir=/root/pip-cache-comfy-base \
#    onnxruntime onnxruntime-gpu pip-tools \
#    && echo -e "\033[0;31m \n\n Установка torch torchvision torchaudio \033[0m" \
#    && if [ "$CUDA_VER" = "12.8" ]; then \
#        pip install \
#        --cache-dir=/root/pip-cache-comfy-base \
#        --pre \
#        --index-url https://download.pytorch.org/whl/nightly/cu128 \
#        torch torchvision torchaudio; \
#    else \
#        pip install \
#        --cache-dir=/root/pip-cache-comfy-base \
#        torch torchvision torchaudio; \
#    fi \
#    && rm -rf ~/.cache/pip


WORKDIR /usr/local/bin
COPY *.sh .
RUN chmod +x *.sh


WORKDIR /workspace/ComfyUI

#COPY comfy.settings.json user/default/

RUN echo "cd /workspace" >> /root/.bashrc
#==============================================================

WORKDIR /workspace/ComfyUI
# шаг 11
COPY nodes.txt python-packages-to-add.txt ./
COPY ./custom-nodes/nodes*.txt ./

# Создаем ARG для передачи списка файлов
ARG NODES="nodes1.txt"

# шаг 12 Кэшируем зависимости и выполняем установку для каждого файла
RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    if [ "$NODES" != "nodes1.txt" ]; then \
        PIP_CACHE_DIR=/root/pip-cache \
        process_repos-install-req.sh "$NODES" false \
        && rm -rf root/.cache/pip; \
    else \
        echo "Skipping RUN because NODES is set to 'nodes1.txt'"; \
    fi

RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    if [ -d "./custom_nodes/cg-use-everywhere" ]; then \
        cd ./custom_nodes/cg-use-everywhere  \
        && git checkout frontend1.16; \
    else \
        echo "Directory cg-use-everywhere does not exist, skipping git checkout."; \
    fi


WORKDIR /workspace/ComfyUI
COPY workflows/ user/default/workflows/
COPY ./user/default/comfy.settings.json user/default/

WORKDIR /workspace/aria2
COPY aria2 .
RUN chmod +x *.sh \
    && chmod +x ./templates/*.sh

WORKDIR /workspace
RUN echo -e "\n========= ACE 23-24===============\n"
# 21
ARG ACE_PLUS_NODE_INSTALL
RUN --mount=type=cache,target=/root/pip-cache \
    if [ "$ACE_PLUS_NODE_INSTALL" = "true" ]; then \
        echo "Running ace-plus-node-install.sh"; \
        PIP_CACHE_DIR=/root/pip-cache; \
        ace-plus-node-install.sh; \
    else \
        echo "Skipping ace-plus-node-install.sh"; \
    fi

WORKDIR /workspace/ComfyUI
COPY union-requiere.py requirements-edit.py ./
#
# удалить версию frontend
RUN  python3 requirements-edit.py \
  && python3 union-requiere.py \
  && rm union-requiere.py

# получим файл requirements.out


RUN echo "cd /workspace/aria2/templates" >> /root/.bashrc \
  && echo "set -g mouse on" >> ~/.tmux.conf

WORKDIR /workspace/ComfyUI

#    --no-build-isolation \
RUN uv pip compile requirements.in -o requirements.out \
    --index-strategy unsafe-best-match

#COPY requirements.out .
RUN --mount=type=cache,target=/root/pip-cache \
    uv pip install \
    --link-mode=copy \
    --system \
    --cache-dir=/root/pip-cache \
    -r requirements.out \
    && rm -rf ~/.cache/pip

#
# ========= POSTINSTALL
#
ARG POST_INSTALL_SH

WORKDIR /workspace
COPY additional-setup/*.sh ./
RUN chmod +x *.sh

RUN --mount=type=cache,target=/root/pip-cache \
    if [ -n "${POST_INSTALL_SH}" ]; then \
        chmod +x *.sh ; \
        ./"${POST_INSTALL_SH}"; \
    fi

WORKDIR /workspace/ComfyUI/custom_nodes/ComfyUI-UNO-Wrapper
COPY configs/UNO/config.json .

CMD ["bash"]