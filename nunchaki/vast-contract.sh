#!/bin/bash


# Проверяем, передан ли первый аргумент (ID инстанса)
if [ -z "$1" ]; then
    echo "Ошибка: Необходимо указать ID инстанса."
    echo "Использование: $0 <instance_id>"
    exit 1
fi

# Используем первый аргумент как ID инстанса
INSTANCE_ID=$1

# --image gayrat/comfyui-supir-12-4:v12.5 \
vastai create instance "$INSTANCE_ID" \
    --image gayrat/nunchaki:v1.2 \
    --disk 160 \
    --ssh --direct \
    --onstart-cmd 'env >> /etc/environment ; tmux source-file ~/.tmux.conf' \
    --env '-p 8188:8188' \
    > vast-create-instance.txt

# Проверяем, существует ли файл
if [[ -f "vast-create-instance.txt" ]]; then
    # Извлекаем число после 'new_contract': с помощью grep и sed
    contract_id=$(grep -oP "'new_contract': \K\d+" vast-create-instance.txt)

    # Проверяем, что значение успешно извлечено
    if [[ -n "$contract_id" ]]; then
        # Экспортируем значение в переменную окружения
        export CONTRACT_ID="$contract_id"
        echo "CONTRACT_ID=$CONTRACT_ID успешно экспортирован."
    else
        echo "Не удалось найти значение new_contract в файле."
#        exit 1
    fi
else
    echo "Файл vast-create-instance.txt не найден."
#    exit 1
fi