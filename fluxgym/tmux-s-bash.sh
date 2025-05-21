#!/bin/bash

# Запускаем tmux сессию
tmux new-session -d -s comfy 'fluxgym.sh'
tmux new-window -t comfy:1 "bash"

# Выбираем первое окно и подключаемся к сессии
tmux select-window -t comfy:0
tmux attach-session -t comfy

