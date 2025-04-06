#!/bin/bash

# Проверяем, передан ли первый аргумент (ID инстанса)
if [ -z "$1" ]; then
    echo "Ошибка: Необходимо указать ID инстанса."
    echo "Использование: $0 <instance_id>"
    exit 1
fi

# Используем первый аргумент как ID инстанса
INSTANCE_ID=$1

vastai create instance "$INSTANCE_ID" \
    --image gayrat/comfyui-supir-12-4:v12.5 \
    --disk 160 \
    --ssh --direct \
    --onstart-cmd 'env >> /etc/environment ; tmux source-file ~/.tmux.conf' \
    --env '-p 8188:8188' \
    > vast-create-instance.txt