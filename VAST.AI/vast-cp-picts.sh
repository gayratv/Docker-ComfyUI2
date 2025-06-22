#!/bin/bash

source vast-env-run-fill-env.sh

HOST_SAVE_DIR=/mnt/f/_prg/python/Docker-ComfyUI/VAST.AI/output/out/
mkdir -p "${HOST_SAVE_DIR}"
scp -r -P $VAST_SSH -i ~/.ssh/mvps/ud_rsa "root@$VAST_PUBLIC_IPADDR:/workspace/ComfyUI/output/" "${HOST_SAVE_DIR}"
