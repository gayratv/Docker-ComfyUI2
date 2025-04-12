# Определяем аргумент для базового образа
ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}

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
        && rm -rf ~/.cache/pip; \
    else \
        echo "Skipping RUN because NODES is set to 'nodes1.txt'"; \
    fi

#        process_repos-git-clone.sh "$NODES" \


WORKDIR /workspace/ComfyUI
COPY workflows/ user/default/workflows/
#COPY comfy.settings.json user/default/

COPY union-requiere.py VPS-copy  ./

WORKDIR /workspace/ComfyUI/input
COPY input  ./

WORKDIR /workspace/aria2
COPY aria2 .
RUN chmod +x *.sh \
    && chmod +x ./templates/*.sh

WORKDIR /workspace/ComfyUI/custom_nodes
COPY union-requiere.py .
RUN python3 union-requiere.py


RUN echo "cd /workspace/aria2/templates" >> /root/.bashrc \
  && echo "set -g mouse on" >> ~/.tmux.conf
#  tmux source-file ~/.tmux.conf

CMD ["bash"]