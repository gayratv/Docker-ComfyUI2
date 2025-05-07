#!/bin/bash

if [ -f ".env" ]; then
    source .env
else
    echo "Файл .env не найден!"
    exit 1
fi

# Проверяем, что переменная GITHUB_TOKEN установлена
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Переменная GITHUB_TOKEN не найдена в .env файле!"
    exit 1
fi

# Функция для вывода справки
usage() {
    echo "Usage: $0 --GET_RELEASE=<true|false>"
    exit 1
}

# Проверяем, соответствует ли первый аргумент формату --GET_RELEASE=*
if [[ "$1" == --GET_RELEASE=* ]]; then
    GET_RELEASE="${1#*=}"  # Извлекаем значение после "="
fi

LATEST_RELEASE="$COMFY_RELEASE_TAG"
FORMATTED_DATE="2025"

if [[ "$GET_RELEASE" == "true" ]]; then
  # Получаем тег последнего релиза
  # Получаем информацию о последнем релизе

  # Получаем тег последнего релиза
  RELEASE_INFO=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
       https://api.github.com/repos/comfyanonymous/ComfyUI/releases/latest)

  # Извлекаем тег релиза
  LATEST_RELEASE=$(echo "$RELEASE_INFO" | jq -r '.tag_name')

  # Извлекаем дату публикации
  RELEASE_DATE=$(echo "$RELEASE_INFO" | jq -r '.published_at')

  # Форматируем дату
  FORMATTED_DATE=$(date -d "$RELEASE_DATE" "+%Y-%m-%d")
fi


echo -e "\e[34mBuilding COMFYUI with release tag: $LATEST_RELEASE date: $FORMATTED_DATE \e[0m"

docker build --progress=plain \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    --build-arg NODES="$NODES" \
    --build-arg COMFYUI_VERSION="$COMFYUI_VERSION" \
    --build-arg ACE_PLUS_NODE_INSTALL=$ACE_PLUS_NODE_INSTALL \
    --build-arg POST_INSTALL_SH=$POST_INSTALL_SH \
    --build-arg COMFY_RELEASE_TAG=$LATEST_RELEASE \
    --build-arg FRONTEND_VER=$FRONTEND_VER \
    --build-arg REQ_MODIFY=$REQ_MODIFY \
    --build-arg EXTRA_INDEX_URLS=$EXTRA_INDEX_URLS \
    --build-arg PY_PACKAGE_ADD=$PY_PACKAGE_ADD \
    -f /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union/Dockerfile1 \
    -t $IMAGE_NAME:$VERSION \
    /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union
echo -e "\nсобран образ $IMAGE_NAME:$VERSION"