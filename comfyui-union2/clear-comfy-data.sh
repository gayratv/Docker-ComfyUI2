#!/bin/bash

# 1. Переместить директорию RMBG на уровень выше
mv /mnt/h/ComfyUI-data/models/RMBG /mnt/h/ComfyUI-data/
mv /mnt/h/ComfyUI-data/models/facerestore_models /mnt/h/ComfyUI-data/

# 2. Удалить всё содержимое директории models
rm -rf /mnt/h/ComfyUI-data/models/*

# 3. Вернуть директорию RMBG обратно
mv /mnt/h/ComfyUI-data/RMBG /mnt/h/ComfyUI-data/models/
mv /mnt/h/ComfyUI-data/facerestore_models /mnt/h/ComfyUI-data/models/