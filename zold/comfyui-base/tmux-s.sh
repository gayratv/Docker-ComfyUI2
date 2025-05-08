#!/bin/bash

#mkdir -p /workspace/tmux-0/
#chmod 700 -R /workspace/tmux-0
#export TMUX_TMPDIR=/workspace
#echo $TMUX_TMPDIR
tmux new-session -d -s comfy 'comfy.sh'
tmux new-window -t comfy:1 'bash'
tmux select-window -t comfy:0
tmux attach-session -t comfy