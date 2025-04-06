#!/bin/bash
../process-models-civitai.sh ./models/Perfect-Relighting/civitay.txt
../aria-start-civitay.sh ./models/Perfect-Relighting/civitay.txt /mnt/h/ComfyUI-data/

../aria-start-huggingface.sh ./models/Perfect-Relighting/hugging-face.txt /mnt/h/ComfyUI-data/