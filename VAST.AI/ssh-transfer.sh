#!/bin/bash

# cd /mnt/f/_prg/python/Docker-ComfyUI/VAST.AI
# source ./ssh-transfer.sh "ssh -p 40011 root@193.32.95.23 -L 8080:localhost:8080"

input="$1"

# Извлечение порта SSH
VAST_SSH=$(echo "$input" | grep -oP '(?<=-p )\d+')

# Извлечение IP-адреса
VAST_PUBLIC_IPADDR=$(echo "$input" | grep -oP '(?<=root@)[0-9.]+')

# Экспорт переменных
export VAST_SSH
export VAST_PUBLIC_IPADDR

# Вывод результата (опционально)
echo "export VAST_SSH=$VAST_SSH"
echo "export VAST_PUBLIC_IPADDR=$VAST_PUBLIC_IPADDR"

ssh -p $VAST_SSH "root@$VAST_PUBLIC_IPADDR" -i ~/.ssh/mvps/ud_rsa
