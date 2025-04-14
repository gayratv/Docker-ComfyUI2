#!/bin/bash

# Функция для проверки значения VAST_SSH
check_vast_ssh() {
    # Загружаем переменные окружения из файла vast-env-run.sh
    source vast-env-run.sh

    # Проверяем, равно ли значение VAST_SSH "null"
    if [[ "$VAST_SSH" != "null" ]]; then
        echo "VAST_SSH is now set to: $VAST_SSH"
        return 0  # Успешное завершение
    else
        echo "Waiting for VAST_SSH to be set... (current status: $VAST_ACTUAL_STATUS)"
        return 1  # Продолжаем ожидание
    fi
}

# Основной цикл
echo "Starting to monitor VAST_SSH..."
while true; do
    if check_vast_ssh; then
        break  # Выходим из цикла, если VAST_SSH установлено
    fi
    sleep 3  # Ждем 3 секунды перед следующей проверкой
done

echo "Monitoring completed. VAST_SSH is ready."