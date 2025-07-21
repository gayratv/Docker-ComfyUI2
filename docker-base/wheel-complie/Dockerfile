# --- ЭТАП 1: СБОРЩИК (BUILDER) ---
# Используем полный образ 'devel' для установки и компиляции зависимостей.
# AS builder - это имя, по которому мы будем обращаться к этому этапу.
# ПРЕДПОЛАГАЕТСЯ, ЧТО В ЭТОМ ОБРАЗЕ УЖЕ ЕСТЬ git, cmake, python3.11, pip.
FROM cuda-12-6:nvidia-devel AS builder

# Устанавливаем wget и unzip. Это необходимо для скачивания
# исходного кода Triton в виде архива, что является более надежным методом, чем git clone.
RUN apt-get update && apt-get install -y --no-install-recommends wget unzip && rm -rf /var/lib/apt/lists/*

# Создаём и активируем виртуальное окружение Python.
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Обновляем pip и устанавливаем базовые пакеты для сборки с использованием кэша
RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade pip wheel setuptools ninja

# Устанавливаем PyTorch 2.7.0 для CUDA 12.6 с использованием кэша
RUN --mount=type=cache,target=/root/.cache/pip pip install torch==2.7.0 --index-url https://download.pytorch.org/whl/cu126

# --- Сборка Triton ---
WORKDIR /build
# Скачиваем и распаковываем исходный код Triton вместо git clone
RUN wget https://github.com/openai/triton/archive/refs/heads/main.zip -O triton.zip && \
    unzip triton.zip && \
    rm triton.zip

# ИСПРАВЛЕНИЕ: Переходим в КОРНЕВУЮ директорию репозитория Triton, где лежит pyproject.toml
WORKDIR /build/triton-main

# ОТЛАДКА: Показываем содержимое текущей директории, чтобы убедиться, что pyproject.toml на месте
RUN ls -la

# Собираем wheel-файл из корневой директории
RUN --mount=type=cache,target=/root/.cache/pip pip wheel . -w /build/wheels

# --- Сборка bitsandbytes для конкретных архитектур ---
WORKDIR /build
# Для bitsandbytes оставляем git clone, так как с ним проблем не было
RUN git clone https://github.com/TimDettmers/bitsandbytes.git

# Переходим в директорию с исходным кодом
WORKDIR /build/bitsandbytes

# Задаем архитектуры CUDA, для которых будем компилировать
# 7.5 = Turing (Quadro RTX 4000)
# 8.6 = Ampere (RTX 3090)
# 8.9 = Ada Lovelace (RTX 4090)
# 9.0 = Blackwell (предположительно для RTX 5090)
ENV BNB_CUDA_VERSION="75;86;89;90"

# Собираем wheel-файл
RUN --mount=type=cache,target=/root/.cache/pip pip wheel . -w /build/wheels


# --- ЭТАП 2: ЭКСПОРТЕР ---
# Используем минимальный образ 'scratch', который не содержит ничего лишнего.
# Он нужен только для того, чтобы из него можно было скопировать результат.
FROM scratch

# Копируем собранные wheel-файлы из этапа сборщика (--from=builder)
COPY --from=builder /build/wheels /wheels
