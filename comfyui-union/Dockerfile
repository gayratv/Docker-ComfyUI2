ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}

#RUN rm -rf /root/pip-cache \
#    rm -rf /root/repo-cache

WORKDIR /workspace


ARG COMFYUI_VERSION
ARG CUDA_VER="12.4"

# Определяем переменную для тега релиза
ARG COMFY_RELEASE_TAG=latest

# Клонируем репозиторий и переключаемся на нужный релиз
RUN if [ "$COMFY_RELEASE_TAG" = "latest" ]; then \
        git clone https://github.com/comfyanonymous/ComfyUI; \
    else \
        git clone --branch $COMFY_RELEASE_TAG https://github.com/comfyanonymous/ComfyUI; \
    fi

WORKDIR /workspace/ComfyUI

COPY *.sh nodes.txt *.py ./


RUN --mount=type=cache,target=/root/pip-cache \
    --mount=type=cache,target=/root/repo-cache \
    PIP_CACHE_DIR=/root/pip-cache \
    && chmod +x *.sh \
    && ./process_repos-install-req.sh nodes.txt false


WORKDIR /usr/local/bin
COPY *.sh .
RUN chmod +x *.sh


WORKDIR /workspace/ComfyUI

#COPY comfy.settings.json user/default/

RUN echo "cd /workspace" >> /root/.bashrc
#==============================================================

WORKDIR /workspace/ComfyUI
# шаг 11
COPY nodes.txt ./
COPY ./custom-nodes/nodes*.txt ./

# Создаем ARG для передачи списка файлов
ARG NODES

# шаг 12 Кэшируем зависимости и выполняем установку для каждого файла
RUN --mount=type=cache,target=/root/repo-cache \
    --mount=type=cache,target=/root/pip-cache \
    if [ -n "$NODES" ]; then \
        PIP_CACHE_DIR=/root/pip-cache \
        process_repos-install-req.sh "$NODES" false \
        && rm -rf root/.cache/pip; \
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

WORKDIR /workspace/ComfyUI
COPY union-requiere.py requirements-edit.py ./
# 32
ARG FRONTEND_VER
RUN pip3 install requests

#python-packages-to-add \
ARG PY_PACKAGE_ADD
COPY ./requirments-modify ./requirments-modify

# удалить версию frontend
RUN  python3 requirements-edit.py --add_package $PY_PACKAGE_ADD --frontend_ver="\"$FRONTEND_VER\"" \
  && python3 union-requiere.py \
  && rm union-requiere.py

#RUN exit 1

RUN echo "cd /workspace/aria2/templates" >> /root/.bashrc \
  && echo "set -g mouse on" >> ~/.tmux.conf

WORKDIR /workspace/ComfyUI

COPY pip-pckg-group.py process-req-in.py ./

ARG REQ_MODIFY

RUN if [ -n "$REQ_MODIFY" ]; then \
        echo "PROCESS requirements.in"; \
        python3 process-req-in.py \
            --requirements-file "requirements.in" \
            --prefixes-file "./requirments-modify/$REQ_MODIFY/remove-lines.txt" \
            --additional-lines-file "./requirments-modify/$REQ_MODIFY/add-lines.txt"; \
    fi

# Определение ARG для передачи нескольких --extra-index-url
ARG EXTRA_INDEX_URLS

# Разделение EXTRA_INDEX_URLS на отдельные --extra-index-url
RUN echo "$EXTRA_INDEX_URLS" | tr ',' '\n' | xargs -I {} echo "--extra-index-url {}" > /tmp/extra_index_args2 \
    # Объединение всех строк в одну строку
    && tr '\n' ' ' < /tmp/extra_index_args2 > /tmp/extra_index_args \
    # Отладочная информация: вывод содержимого /tmp/extra_index_args
    && echo "Generated extra index arguments:" \
    && cat /tmp/extra_index_args

RUN echo "========== cat /tmp/extra_index_args ==============="

    # Компиляция requirements с использованием переданных URL
RUN uv pip compile requirements.modify.in -o requirements.out \
        --index-strategy unsafe-best-match \
        $(cat /tmp/extra_index_args)

     # Разбиение скомпилированных пакетов на группы
RUN python3 pip-pckg-group.py && \
    # Удаление временных файлов
    rm pip-pckg-group.py process-req-in.py


# ==== Установка зависимостей по группам
# Установка остальных зависимостей

RUN --mount=type=cache,target=/root/pip-cache \
    uv pip install \
    --link-mode=copy \
    --system \
    --cache-dir=/root/pip-cache \
    -r other_requirements.txt \
    && rm -rf /root/.cache/pip

# Установка NVIDIA-зависимостей

RUN --mount=type=cache,target=/root/pip-cache \
    uv pip install \
    --link-mode=copy \
    --system \
    --cache-dir=/root/pip-cache \
    $(cat /tmp/extra_index_args) \
    -r nvidia_requirements.txt \
    && rm -rf /root/.cache/pip

# Установка xformers-зависимостей

RUN --mount=type=cache,target=/root/pip-cache \
    uv pip install \
    --link-mode=copy \
    --system \
    --cache-dir=/root/pip-cache \
    $(cat /tmp/extra_index_args) \
    -r xformers_requirements.txt \
    && rm -rf /root/.cache/pip

# Установка Torch-зависимостей

RUN --mount=type=cache,target=/root/pip-cache \
    uv pip install \
    --link-mode=copy \
    --system \
    --extra-index-url https://download.pytorch.org/whl/cu124 \
    $(cat /tmp/extra_index_args) \
    --cache-dir=/root/pip-cache \
    -r torch_requirements.txt \
    && rm -rf /root/.cache/pip



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

# для UNO
#WORKDIR /workspace/ComfyUI/custom_nodes/ComfyUI-UNO-Wrapper
#COPY configs/UNO/config.json .

CMD ["bash"]