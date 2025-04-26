#!/bin/bash


# Получаем тег последнего релиза
# Получаем информацию о последнем релизе
RELEASE_INFO=$(curl -s https://api.github.com/repos/comfyanonymous/ComfyUI/releases/latest)

# Извлекаем тег релиза
LATEST_RELEASE=$(echo "$RELEASE_INFO" | jq -r '.tag_name')

# Извлекаем дату публикации
RELEASE_DATE=$(echo "$RELEASE_INFO" | jq -r '.published_at')

# Форматируем дату
FORMATTED_DATE=$(date -d "$RELEASE_DATE" "+%Y-%m-%d")

echo -e "\e[34mBuilding COMFYUI with release tag: $LATEST_RELEASE date: $FORMATTED_DATE \e[0m"

docker build --progress=plain \
    --build-arg BASE_IMAGE="$BASE_IMAGE" \
    --build-arg NODES="$NODES" \
    --build-arg COMFYUI_VERSION="$COMFYUI_VERSION" \
    --build-arg ACE_PLUS_NODE_INSTALL=$ACE_PLUS_NODE_INSTALL \
    --build-arg POST_INSTALL_SH=$POST_INSTALL_SH \
    --build-arg RELEASE_TAG=$LATEST_RELEASE \
    --build-arg REQ_MODIFY=$REQ_MODIFY \
    --build-arg EXTRA_INDEX_URLS=$EXTRA_INDEX_URLS \
    -f /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union/Dockerfile \
    -t $IMAGE_NAME:$VERSION \
    /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union
echo -e "\nсобран образ $IMAGE_NAME:$VERSION"