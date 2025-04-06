#!/bin/bash
../aria-start-huggingface.sh ./models/bg-replacer-v3/bg-replacer-v3-hf-models.txt
../process-models-civitai.sh ./models/bg-replacer-v3/bg-replacer-v3-civitay-models.txt
../aria-start-civitay.sh ./models/bg-replacer-v3/bg-replacer-v3-civitay-models-token.txt