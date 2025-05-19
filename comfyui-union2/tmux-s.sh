#!/bin/bash

# Проверяем аргументы
if [ -z "$1" ]; then
  echo "Ошибка: Не указано имя модели."
  exit 1
fi

MODEL_NAME="$1"

# source выполняется ДО создания tmux-сессии
if [ "$2" = "local" ]; then
  source ../load-env.sh
  echo -e "CIVITAI_TOKEN : $CIVITAI_TOKEN \n"
fi

# Убиваем старую сессию
tmux kill-session -t comfy 2>/dev/null

# Создаём новую фоновую сессию (уже с нужным окружением)
tmux new-session -d -s comfy

# Первое окно
tmux send-keys -t comfy:0 "comfy.sh; echo 'Нажми Enter'; read" C-m

# Второе окно
tmux new-window -t comfy -n "Download" \
  "bash -c './dl_common.sh \"$MODEL_NAME\"; echo \"Нажми Enter\"; read'"

# Третье окно
tmux new-window -t comfy -n "bash" "bash"

# Подключаемся
tmux select-window -t comfy:0
tmux attach-session -t comfy

# tmux-s.sh ControlNet-Flux-Tools-OreX local