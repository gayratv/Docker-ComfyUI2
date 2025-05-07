#!/bin/bash

# Проверяем аргументы
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  echo "Usage: $0 <repo_url> <checkout_target> <cache_dir>"
  echo "Example: $0 https://github.com/comfyanonymous/ComfyUI v1.0.0 /root/repo-cache"
  exit 1
fi

REPO_URL="$1"
CHECKOUT_TARGET="$2"
CACHE_DIR="${3:-/root/repo-cache}"

# Цвета
BLUE='\033[34m'
RESET='\033[0m'

# mkdir -p /root/repo-cache

# === DEBUG OUTPUT ===
echo "DEBUG: Script running in directory: $(pwd)"
echo -e "${BLUE}DEBUG: Parameters passed to script:${RESET}"
echo "       \$0 = $0"
echo "       \$1 (REPO_URL) = $1"
echo "       \$2 (CHECKOUT_TARGET) = $2"
echo "       \$3 (CACHE_DIR) = $3"
# === END DEBUG ===

# Получаем имя репозитория без .git
REPO_NAME=$(basename "$REPO_URL" .git)
REPO_HASH=$(echo -n "$CHECKOUT_TARGET" | sha256sum | awk '{print $1}')
TARGET_CACHE_DIR="$CACHE_DIR/${REPO_NAME}_$REPO_HASH"
echo -e "       TARGET_CACHE_DIR = $TARGET_CACHE_DIR\n"

# Проверяем, есть ли уже закешированная версия
if [ -d "$TARGET_CACHE_DIR" ]; then
  echo -e "${BLUE}Cached version found in $TARGET_CACHE_DIR${RESET}"
  echo "Copying to current directory..."
  mkdir -p "$REPO_NAME"
  cp -r "$TARGET_CACHE_DIR"/* "$REPO_NAME/"
  exit 0
fi

# Клонируем репозиторий в текущую директорию
echo "Cloning repository from $REPO_URL into current directory..."
git clone "$REPO_URL" "$REPO_NAME"

cd $REPO_NAME || exit 1

# Проверяем, является ли CHECKOUT_TARGET тегом
IS_TAG=$(git ls-remote --tags origin "$CHECKOUT_TARGET" | grep -v '{}')

if [[ -n "$IS_TAG" ]]; then
  echo "Found tag: $CHECKOUT_TARGET"
  git checkout "tags/$CHECKOUT_TARGET"
else
  # Проверяем, является ли CHECKOUT_TARGET веткой
  IS_BRANCH=$(git ls-remote --heads origin "$CHECKOUT_TARGET")

  if [[ -n "$IS_BRANCH" ]]; then
    echo "Found branch: $CHECKOUT_TARGET"
    git checkout "$CHECKOUT_TARGET"
  else
    # Проверяем, является ли CHECKOUT_TARGET хешом коммита
    if git rev-parse "$CHECKOUT_TARGET"^{commit} >/dev/null 2>&1; then
      echo "Found commit hash: $CHECKOUT_TARGET"
      git checkout "$CHECKOUT_TARGET"
    else
      echo "Error: '$CHECKOUT_TARGET' is not a valid tag, branch or commit in the repository."
      exit 1
    fi
  fi
fi

# Сохраняем в кеш
cd ..
mkdir -p "$TARGET_CACHE_DIR"
echo "DEBUG   TARGET_CACHE_DIR = $TARGET_CACHE_DIR"
cp -r "${REPO_NAME}"/* "$TARGET_CACHE_DIR"/