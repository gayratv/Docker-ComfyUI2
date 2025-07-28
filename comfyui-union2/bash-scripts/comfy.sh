#!/bin/bash

cd /workspace/ComfyUI

if [ "$USE_SAGE_ATTENTION" = "1" ]; then
    echo "use-sage-attention переменная задана, запускаем с параметром --use-sage-attention"
    python3 main.py --listen 0.0.0.0 --port 8188 --disable-smart-memory --disable-metadata --use-sage-attention
else
    echo "use-sage-attention переменная не задана, запускаем без параметра --use-sage-attention"
    python3 main.py --listen 0.0.0.0 --port 8188 --disable-smart-memory --disable-metadata
fi

# nano /usr/local/bin/comfy.sh

# для карты 5090 рекомендуется использовать sage-attention
# python main.py --use-sage-attention
# pip install sageattention
# для sageattention нужен Triton

#--disable-metadata
#Отключает добавление технической информации в метаданные сгенерированных изображений.
#Это полезно, если вы не хотите, чтобы в PNG/JPG сохранялись данные о workflow,
#используемых узлах, версиях моделей и т.п.