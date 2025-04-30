# Определяем аргумент для базового образа
ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}

#RUN rm -rf /root/repo-cache \
#    && rm -rf /root/pip-cache

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
RUN for dir in */; do [ "$dir" != "nunchaku/" ] && rm -r "$dir"; done

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
        PIP_CACHE_DIR=/root/pip-cache; \
        ./post-install/"$POST_INSTALL"; \
    else \
        echo "Skipping post-install script"; \
    fi

WORKDIR /workspace/ComfyUI/custom_nodes
COPY union-requiere.py .
RUN python3 union-requiere.py \
  && rm union-requiere.py


RUN echo "cd /workspace/aria2/templates" >> /root/.bashrc \
  && echo "set -g mouse on" >> ~/.tmux.conf
#  tmux source-file ~/.tmux.conf

CMD ["bash"]