# Сборка
FROM cuda-12-6:nvidia-devel AS builder
WORKDIR /workspace/
RUN git clone https://github.com/thu-ml/SageAttention.git
WORKDIR /workspace/SageAttention

RUN python3 -m pip install --upgrade pip

RUN --mount=type=cache,target=/root/pip-cache \
  python3 -m pip install --cache-dir=/root/pip-cache packaging


RUN --mount=type=cache,target=/root/pip-cache \
  python3 -m pip install --cache-dir=/root/pip-cache  torch==2.7.0 torchaudio==2.7.0 \
    --extra-index-url https://download.pytorch.org/whl/cu126

RUN --mount=type=cache,target=/root/pip-cache \
  python3 -m pip install --cache-dir=/root/pip-cache numpy

# parallel compiling (Optional)
ENV TORCH_CUDA_ARCH_LIST="8.6;8.9"
ENV EXT_PARALLEL=4
ENV NVCC_APPEND_FLAGS="--threads 8"
ENV MAX_JOBS=32
ENV FORCE_CUDA=1

#export TORCH_CUDA_ARCH_LIST="8.6;8.9"
#export EXT_PARALLEL=4
#export NVCC_APPEND_FLAGS="--threads 8"
#export MAX_JOBS=32
#export FORCE_CUDA=1

#RUN  python3 setup.py install


#RUN --mount=type=cache,target=/root/pip-cache \
#  python3 -m pip install  --cache-dir=/root/pip-cache   -e .
#RUN  python3 -m pip install  -e .


# Команда по умолчанию
CMD ["bash"]