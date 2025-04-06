#!/bin/bash
../aria-start-huggingface.sh ./models/Blend-Human-into-Background-Image-with-ACE-Plus-Redux/hugging-face.txt
../process-models-civitai.sh ./models/Blend-Human-into-Background-Image-with-ACE-Plus-Redux/civitay.txt
../aria-start-civitay.sh ./models/Blend-Human-into-Background-Image-with-ACE-Plus-Redux/civitay-token.txt