# Определяем аргумент для базового образа
ARG BASE_IMAGE="comfyui-base-cuda"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}


WORKDIR /workspace

RUN git clone https://github.com/comfyanonymous/ComfyUI

WORKDIR /workspace/ComfyUI

COPY *.sh cloudflare.py nodes.txt requirements-edit.py ./


RUN --mount=type=cache,target=/root/pip-cache-comfy-base \
    --mount=type=cache,target=/root/pip-cache \
    PIP_CACHE_DIR=/root/pip-cache \
    && chmod +x *.sh  \
    && python3 requirements-edit.py \
    && pip3 install --cache-dir=/root/pip-cache-comfy-base -r  requirements.txt \
    && ./process_repos-install-req.sh nodes.txt \
    && pip3 install --cache-dir=/root/pip-cache-comfy-base onnxruntime onnxruntime-gpu pip-tools \
    && rm -rf ~/.cache/pip


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
