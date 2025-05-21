#!/bin/bash
# данная версия также сравнивает хеш последнего комита

BASE_INSTALL_DIR="/workspace/ComfyUI/custom_nodes/"
NODES_FILE="${1:-nodes.txt}"
INSTALL_REQ="${2:-false}"

if [ ! -f "$NODES_FILE" ]; then
    echo "ERROR: $NODES_FILE not found. Create the file and add repository URLs."
    exit 1
fi

# читаем список репозиториев, убираем пустые строки и комментарии
mapfile -t INSTALL_DATA < <(
    sed '
        s/^[[:space:]]*//;
        s/[[:space:]]*$//;
        /^$/d;
        /^#/d
    ' "$NODES_FILE"
)

echo "DEBUG: Processing the following repositories from $NODES_FILE:"
for GIT_REPO in "${INSTALL_DATA[@]}"; do
    echo "DEBUG: $GIT_REPO"

    REPO_NAME=$(basename "$GIT_REPO" .git | sed 's/\r$//')
    INSTALL_DIR="$BASE_INSTALL_DIR"
    CACHE_DIR="/root/repo-cache/$REPO_NAME"
    CACHED_HASH_FILE="$CACHE_DIR/.last_hash"

    echo -e "\e[1;31mDEBUG: repo name: $REPO_NAME\e[0m"
    echo "DEBUG: Using INSTALL_DIR: $INSTALL_DIR"

    # Получаем последний хеш с сервера
    REMOTE_HASH=$(git ls-remote "$GIT_REPO" HEAD | awk '{print $1}')
    echo "DEBUG: Remote hash for $REPO_NAME is $REMOTE_HASH"

    # Проверяем кеш
    USE_CACHE=false
    if [ -d "$CACHE_DIR" ] && [ -f "$CACHED_HASH_FILE" ]; then
        CACHED_HASH=$(<"$CACHED_HASH_FILE")
        if [ "$CACHED_HASH" = "$REMOTE_HASH" ]; then
            echo -e "\e[1;34mINFO: Cache is up to date for $REPO_NAME (hash $CACHED_HASH)\e[0m"
            USE_CACHE=true
        else
            echo -e "\e[1;33mINFO: Cache outdated for $REPO_NAME (cached=$CACHED_HASH remote=$REMOTE_HASH), removing...\e[0m"
            rm -rf "$CACHE_DIR"
        fi
    fi

    # Клонируем из кеша или из сети
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR" || { echo "ERROR: cannot cd to $INSTALL_DIR"; exit 1; }

    if [ "$USE_CACHE" = true ]; then
        echo -e "\e[1;34mINFO: Copying $REPO_NAME from cache\e[0m"
        # создаём папку назначения и копируем _только_ содержимое кеша
        mkdir -p "./$REPO_NAME"
        cp -r "$CACHE_DIR/." "./$REPO_NAME/"
    else
        echo "DEBUG: Cloning repository $GIT_REPO..."
        git clone --recurse-submodules "$GIT_REPO"

        echo -e "\e[1;31mDEBUG: Caching repository to $CACHE_DIR...\e[0m"
        # сбрасываем старый кеш, чтобы не было вложенной папки
        rm -rf "$CACHE_DIR"
        mkdir -p "$CACHE_DIR"
        # копируем все файлы из клона в кеш
        cp -r "./$REPO_NAME/." "$CACHE_DIR/"
        echo "$REMOTE_HASH" > "$CACHED_HASH_FILE"
    fi

    # Переходим внутрь репозитория
    cd "$REPO_NAME" || { echo "ERROR: cannot cd to $REPO_NAME"; exit 1; }

    # Устанавливаем зависимости, если нужно
    if [ "$INSTALL_REQ" = "true" ] && [ -f "requirements.txt" ]; then
        echo "Installing Python dependencies from requirements.txt (excluding torch)…"
        TMP_REQ=$(mktemp)
        grep -v '^torch' requirements.txt | grep -v '^#' | grep . > "$TMP_REQ"
        pip install --cache-dir "${PIP_CACHE_DIR:-/root/pip-cache}" -r "$TMP_REQ" 2> pip_error.log || {
            echo "ERROR: Failed to install dependencies. See pip_error.log."
            rm "$TMP_REQ"
            exit 1
        }
        rm "$TMP_REQ"
    else
        echo "No requirements.txt found in $REPO_NAME."
    fi

done
