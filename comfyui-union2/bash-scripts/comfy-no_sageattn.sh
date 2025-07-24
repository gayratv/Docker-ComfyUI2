#!/bin/bash

cd /workspace/ComfyUI
python3 main.py --listen 0.0.0.0 --port 8188 --disable-smart-memory --disable-metadata
#python3 main.py --listen 0.0.0.0 --port 8188 --verbose --disable-smart-memory --disable-metadata

# для карты 5090 рекомендуется использовать sage-attention
# python main.py --use-sage-attention
# pip install sageattention
# для sageattention нужен Triton

#--disable-metadata
#Отключает добавление технической информации в метаданные сгенерированных изображений.
#Это полезно, если вы не хотите, чтобы в PNG/JPG сохранялись данные о workflow,
#используемых узлах, версиях моделей и т.п.