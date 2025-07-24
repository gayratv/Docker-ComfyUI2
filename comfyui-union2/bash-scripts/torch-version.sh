#!/bin/bash

python3 -c "import torch; print(torch.__version__, '+cu'+torch.version.cuda if torch.version.cuda else ' (CPU)')"
