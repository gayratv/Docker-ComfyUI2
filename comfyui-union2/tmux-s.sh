#!/bin/bash

# Проверяем, передан ли параметр (путь к скрипту)
if [ -z "$1" ]; then
  echo "Ошибка: Необходимо указать путь к скрипту как параметр."
  echo "Пример использования: $0 ComfyUI-Fluxtapoz.sh"
  exit 1
fi

SCRIPT_PATH="$1"

# Создаем директорию для tmux (если нужно)
# mkdir -p /workspace/tmux-0/
# chmod 700 -R /workspace/tmux-0
# export TMUX_TMPDIR=/workspace
# echo $TMUX_TMPDIR

# Запускаем tmux сессию
tmux new-session -d -s comfy 'comfy.sh'



tmux new-window -t comfy:1 "bash -c 'cd /workspace/aria2/templates && ./$SCRIPT_PATH'"

# Выбираем первое окно и подключаемся к сессии
tmux select-window -t comfy:0
tmux attach-session -t comfy

# nano /usr/local/bin/tmux-s.sh
# tmux-s.sh ComfyUI-Fluxtapoz.sh