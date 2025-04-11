#!/bin/bash
../aria-start-huggingface.sh ./models/supir-bodrov/hf.txt /workspace/ComfyUI/

../process-models-civitai.sh ./models/supir-bodrov/civitay.txt
../aria-start-civitay.sh ./models/supir-bodrov/civitay.txt /workspace/ComfyUI/
