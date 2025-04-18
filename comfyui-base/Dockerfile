# Определяем аргумент для базового образа
ARG BASE_IMAGE="comfyui-base-cuda"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}

# Удалить кеш pip перед установкой:
# RUN rm -rf /root/pip-cache-comfy-base/*

# Создание рабочей директории
WORKDIR /workspace
# Создание виртуального окружения
# RUN python -m venv /workspace/.venv --system-site-packages

ARG COMFYUI_VERSION
ARG CUDA_VER="12.4"

RUN git clone https://github.com/comfyanonymous/ComfyUI \
    && if [ -n "$COMFYUI_VERSION" ]; then \
        cd ComfyUI \
        && git checkout "$COMFYUI_VERSION"; \
    fi

WORKDIR /workspace/ComfyUI

COPY *.sh cloudflare.py nodes.txt *.py ./

# удаляет пакеты и версию frontend
#packages_to_remove = {
#    "torch",
#    "torchvision",
#    "torchaudio",
#    "numpy"
#}
# 12
#RUN python3 requirements-edit-full.py
#RUN rm requirements-edit-full.py

RUN --mount=type=cache,target=/root/pip-cache-comfy-base \
    --mount=type=cache,target=/root/pip-cache \
    PIP_CACHE_DIR=/root/pip-cache \
    && chmod +x *.sh \
    && if [ -z "$COMFYUI_VERSION" ]; then python3 requirements-edit-full.py; fi \
    && pip install \
    --cache-dir=/root/pip-cache-comfy-base -r \
    requirements.txt \
    && ./process_repos-install-req.sh nodes.txt \
    && rm -rf ~/.cache/pip

RUN --mount=type=cache,target=/root/pip-cache-comfy-base \
    --mount=type=cache,target=/root/pip-cache \
    PIP_CACHE_DIR=/root/pip-cache \
    && echo -e "\033[0;31m \n\n Установка дополнительных пакетов \033[0m" \
    && uv pip install \
    --link-mode=copy \
    --system \
    --cache-dir=/root/pip-cache-comfy-base \
    onnxruntime onnxruntime-gpu pip-tools \
    && echo -e "\033[0;31m \n\n Установка torch torchvision torchaudio \033[0m" \
    && if [ "$CUDA_VER" = "12.8" ]; then \
        pip install \
        --cache-dir=/root/pip-cache-comfy-base \
        --pre \
        --index-url https://download.pytorch.org/whl/nightly/cu128 \
        torch torchvision torchaudio; \
    else \
        pip install \
        --cache-dir=/root/pip-cache-comfy-base \
        torch torchvision torchaudio; \
    fi \
    && rm -rf ~/.cache/pip


# uv pip install \
#        --link-mode=copy \
#        --system \
#        --cache-dir=/root/pip-cache-comfy-base \
#        --pre \

# Устанавливаем переменную окружения для пути
ENV DOWNLOADS_DIR=/usr/local/bin

# Копируем необходимые файлы в указанную директорию
COPY *.sh $DOWNLOADS_DIR/

RUN chmod +x $DOWNLOADS_DIR/*.sh

COPY nodes*.txt ./

WORKDIR /workspace/ComfyUI

#COPY comfy.settings.json user/default/

RUN echo "cd /workspace" >> /root/.bashrc

CMD ["bash"]
