# Определяем аргумент для базового образа
ARG BASE_IMAGE="gayrat/cuda-12-4:latest"

# Используем аргумент в качестве имени образа
FROM ${BASE_IMAGE}


WORKDIR /workspace

RUN git clone https://github.com/comfyanonymous/ComfyUI

#    && pip3 install -r requirements.txt \
WORKDIR /workspace/ComfyUI
RUN pip3 install --pre -r  requirements.txt
#RUN pip3 install -r <(grep -v '^ *#\|^torch' requirements.txt | grep .)

#    && rm -rf ~/.cache/pip

WORKDIR /workspace/ComfyUI
# Копирование скрипта для обработки массива данных
COPY process_repos.sh cloudflare.py nodes.txt ./

# Делаем скрипт исполняемым
RUN chmod +x process_repos.sh  \
    && /bin/bash -c "./process_repos.sh nodes.txt" \
    && rm -rf ~/.cache/pip

# Устанавливаем переменную окружения для пути
ENV DOWNLOADS_DIR=/usr/local/bin

# Копируем необходимые файлы в указанную директорию
COPY *.sh $DOWNLOADS_DIR/

RUN chmod +x $DOWNLOADS_DIR/*.sh

COPY nodes*.txt ./

WORKDIR /workspace/ComfyUI

COPY comfy.settings.json user/default/
COPY ptest.sh $DOWNLOADS_DIR/

RUN echo "cd /workspace" >> /root/.bashrc

CMD ["bash"]
