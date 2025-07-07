#!/bin/bash
# comfyui-union2/bash-scripts/build/process_repos-install-req.sh

# данная версия также сравнивает хеш последнего комита
# Добавлен третий необязательный параметр для указания директории установки

# --- Параметры ---
GIT_REPO="${1}" # Принимаем URL репозитория как первый аргумент
INSTALL_DEPS="${2:-true}" # Принимаем второй параметр для установки зависимостей, по умолчанию true
BASE_INSTALL_DIR="${3:-/workspace/ComfyUI/custom_nodes/}" # Принимаем третий параметр для пути установки

# --- Проверка параметров ---
if [ -z "$GIT_REPO" ]; then
    echo "ERROR: URL репозитория не указан."
    echo "Пример использования: $0 <URL репозитория> [true|false] [/путь/установки]"
    exit 1
fi

echo "DEBUG: Обработка репозитория: $GIT_REPO"
echo "DEBUG: Устанавливать зависимости: $INSTALL_DEPS"
echo "DEBUG: Базовая директория установки: $BASE_INSTALL_DIR"

# --- Основные переменные ---
REPO_NAME=$(basename "$GIT_REPO" .git | sed 's/\r$//')
INSTALL_DIR="$BASE_INSTALL_DIR"
CACHE_DIR="/root/repo-cache/$REPO_NAME"
CACHED_HASH_FILE="$CACHE_DIR/.last_hash"

echo -e "\e[1;31mDEBUG: имя репозитория: $REPO_NAME\e[0m"
echo "DEBUG: Используется INSTALL_DIR: $INSTALL_DIR"

# --- Логика кеширования и установки ---

# Получаем последний хеш с сервера
REMOTE_HASH=$(git ls-remote "$GIT_REPO" HEAD | awk '{print $1}')
echo "DEBUG: Удаленный хеш для $REPO_NAME: $REMOTE_HASH"

# Проверяем кеш
USE_CACHE=false
if [ -d "$CACHE_DIR" ] && [ -f "$CACHED_HASH_FILE" ]; then
    CACHED_HASH=$(<"$CACHED_HASH_FILE")
    if [ "$CACHED_HASH" = "$REMOTE_HASH" ]; then
        echo -e "\e[1;34mINFO: Кэш актуален для $REPO_NAME (хеш $CACHED_HASH)\e[0m"
        USE_CACHE=true
    else
        echo -e "\e[1;33mINFO: Кэш для $REPO_NAME устарел (кэш=$CACHED_HASH удаленный=$REMOTE_HASH), удаляем...\e[0m"
        rm -rf "$CACHE_DIR"
    fi
fi

# Клонируем из кеша или из сети
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR" || { echo "ERROR: не удалось перейти в $INSTALL_DIR"; exit 1; }

if [ "$USE_CACHE" = true ]; then
    echo -e "\e[1;34mINFO: Копирование $REPO_NAME из кэша\e[0m"
    # создаём папку назначения и копируем _только_ содержимое кеша
    mkdir -p "./$REPO_NAME"
    cp -r "$CACHE_DIR/." "./$REPO_NAME/"
else
    echo "DEBUG: Клонирование репозитория $GIT_REPO..."
    git clone --recurse-submodules "$GIT_REPO"

    echo -e "\e[1;31mDEBUG: Кэширование репозитория в $CACHE_DIR...\e[0m"
    # сбрасываем старый кеш, чтобы не было вложенной папки
    rm -rf "$CACHE_DIR"
    mkdir -p "$CACHE_DIR"
    # копируем все файлы из клона в кеш
    cp -r "./$REPO_NAME/." "$CACHE_DIR/"
    echo "$REMOTE_HASH" > "$CACHED_HASH_FILE"
fi

# Устанавливаем зависимости только если INSTALL_DEPS=true
if [ "$INSTALL_DEPS" = true ]; then
    # Переходим внутрь репозитория
    cd "$REPO_NAME" || { echo "ERROR: не удалось перейти в $REPO_NAME"; exit 1; }

    # Устанавливаем зависимости (если есть requirements.txt)
    if [ -f "requirements.txt" ]; then
        echo "Установка зависимостей Python из requirements.txt (исключая torch)..."
        TMP_REQ=$(mktemp)
        grep -v '^torch' requirements.txt | grep -v '^#' | grep . > "$TMP_REQ"
        if [ -s "$TMP_REQ" ]; then
            python3 -m pip install --cache-dir "${PIP_CACHE_DIR:-/root/pip-cache}" -r "$TMP_REQ" 2> pip_error.log || {
                echo "ERROR: Не удалось установить зависимости. См. pip_error.log."
                rm "$TMP_REQ"
                exit 1
            }
        fi
        rm "$TMP_REQ"
    else
        echo "Файл requirements.txt не найден в $REPO_NAME."
    fi
else
    echo "INFO: Пропуск установки зависимостей для $REPO_NAME по команде."
fi