#!/bin/bash

# Проверяем, передан ли первый аргумент (ID инстанса)
if [ -z "$1" ]; then
    echo "Ошибка: Необходимо указать ID инстанса."
    echo "Использование: $0 <instance_id> <image_name>"
    exit 1
fi

# Проверяем, передан ли второй аргумент (имя образа)
if [ -z "$2" ]; then
    echo "Ошибка: Необходимо указать имя образа."
    echo "Использование: $0 <instance_id> <image_name>"
    exit 1
fi

# Используем первый аргумент как ID инстанса
INSTANCE_ID=$1

# Используем второй аргумент как имя образа
IMAGE_NAME=$2

# Создаем инстанс с использованием переданного имени образа
vastai create instance "$INSTANCE_ID" \
    --image "$IMAGE_NAME" \
    --disk 100 \
    --ssh --direct \
    --onstart-cmd 'env >> /etc/environment ; tmux source-file ~/.tmux.conf ; touch ~/.no_auto_tmux; ' \
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

        python3 "./PY-mysql/process_contract(id=$CONTRACT_ID)"
    else
        echo "Не удалось найти значение new_contract в файле."
        exit 1
    fi
else
    echo "Файл vast-create-instance.txt не найден."
    exit 1
fi