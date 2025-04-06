#!/bin/bash
#source ../load-env.sh
../process-models-civitai.sh ./models/SUPIR-v2-MaskTile/SUPIR-v2-MaskTile-models-civitay.txt
../aria-start-civitay.sh ./models/SUPIR-v2-MaskTile/SUPIR-v2-MaskTile-models-civitay-token.txt
../aria-start-huggingface.sh ./models/SUPIR-v2-MaskTile/SUPIR-v2-MaskTile-models-hf.txt