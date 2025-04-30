#!/bin/bash

pip install --cache-dir /root/pip-cache  "https://github.com/mit-han-lab/nunchaku/releases/download/v0.2.0/nunchaku-0.2.0+torch2.6-cp311-cp311-linux_x86_64.whl"


# Для Deepl транслятор
#mkdir /temp
#cd /temp
#wget https://go.dev/dl/go1.24.2.linux-amd64.tar.gz
#tar -xzf go1.24.2.linux-amd64.tar.gz -C /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/DeepLXTranslateNode
#cd /workspace/ComfyUI/custom_nodes/ComfyUI_Custom_Nodes_AlekPet/DeepLXTranslateNode
#git clone https://github.com/OwO-Network/DeepLX

#echo 'export IP=127.0.0.1' >> /root/.bashrc
