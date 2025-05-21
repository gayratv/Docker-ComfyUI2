# ====== Stage 1: Builder ======
ARG BASE_IMAGE="gayrat/comfyui-base-cuda-12-4:v2.0"
FROM ${BASE_IMAGE}

WORKDIR /usr/local/bin
COPY ./bash-scripts/build/*.sh ./
COPY ./bash-scripts/*.sh ./
COPY ./*.sh ./
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



WORKDIR /workspace/
COPY nodes.txt .

ARG NODES=nodes.txt


RUN git clone https://github.com/cocktailpeanut/fluxgym
WORKDIR /workspace/fluxgym
RUN git clone -b sd3 https://github.com/kohya-ss/sd-scripts
#RUN git checkout -b sd3 origin/sd3

ARG PYTORCH_WHEEL="https://download.pytorch.org/whl/cu124"

RUN --mount=type=cache,target=/root/pip-cache \
  pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0  --index-url ${PYTORCH_WHEEL} \
  && pip install xformers  --index-url ${PYTORCH_WHEEL} \
  && pip install typing_extensions \
  && rm -rf /root/.cache/pip

WORKDIR /workspace/fluxgym
RUN --mount=type=cache,target=/root/pip-cache \
    pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

WORKDIR /workspace/fluxgym/sd-scripts

RUN --mount=type=cache,target=/root/pip-cache \
    pip install -r requirements.txt \
    && rm -rf /root/.cache/pip


#rem pip install --no-cache-dir --ignore-installed --force-reinstall --no-warn-conflicts xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu121


WORKDIR /workspace/aria2
COPY aria2 .
RUN chmod +x *.sh \
    && chmod +x ./templates/*.sh \
    && rm -f ./templates/.env

# Добавьте пути в ~/.bashrc
RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64' >> /root/.bashrc && \
    echo 'export PATH=$PATH:/usr/local/cuda/bin' >> /root/.bashrc

# Обновите кэш динамических библиотек
RUN ldconfig


WORKDIR /workspace/fluxgym

RUN echo "cd /workspace/aria2/templates" >> /root/.bashrc \
  && echo "set -g mouse on" >> ~/.tmux.conf

EXPOSE 7860

ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["bash"]