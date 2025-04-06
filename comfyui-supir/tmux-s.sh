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

# Создаем новое окно с bash
tmux new-window -t comfy:1 'bash'

# Создаем новое окно с выполнением переданного скрипта
tmux new-window -t comfy:1 "bash -c 'cd /workspace/aria2/templates && ./$SCRIPT_PATH'"
#tmux new-window -t comfy:1 \
#  "bash -c \"\
#    cd /workspace/aria2/templates && \
#    ./$SCRIPT_PATH; \
#    echo \\\"Скрипт завершен. Запуск интерактивного bash...\\\"; \
#    exec bash\
#  \""

# Выбираем первое окно и подключаемся к сессии
tmux select-window -t comfy:0
tmux attach-session -t comfy
