#!/bin/bash

# Проверяем, что переданы все необходимые аргументы
if [ "$#" -ne 4 ]; then
    echo "Использование: $0 num_gpus gpu_name inet_down cpu_ram"
    echo "Пример: $0 1 RTX_3090 5000 64"
    exit 1
fi

# Присваиваем аргументы переменным
NUM_GPUS=$1
GPU_NAME=$2
INET_DOWN=$3
CPU_RAM=$4

# Файл для сохранения выходных данных vastai search offers
OUTPUT_FILE="vast-search-offers.txt"

# Выполняем запрос к vastai и сохраняем результат в файл
vastai search offers "num_gpus=$NUM_GPUS gpu_name=$GPU_NAME inet_down>=$INET_DOWN cpu_ram>=$CPU_RAM" > "$OUTPUT_FILE"

# Обрабатываем заголовок с фиксированной шириной столбцов
header=$(awk 'NR == 1 {
       printf "%-10s %-6s %-10s %-6s %-6s %-6s %-10s %-8s %-10s %-8s %-6s %-15s\n",
              "ID", "CUDA", "Model", "vCPUs", "RAM", "$/hr", "Net_down", "mach_id", "status", "host_id", "ports", "country";
       next
     }' "$OUTPUT_FILE")

# Обрабатываем данные с фиксированной шириной столбцов
data=$(awk 'NR > 1 {
       printf "%-10s %-6s %-10s %-6s %-6s %-6.2f %-10s %-8s %-10s %-8s %-6s %-15s\n",
              $1, $2, $4, $7, $8, $10, $15, $19, $20, $21, $22, $23
     }' "$OUTPUT_FILE" | sort -k6,6n)

# Выводим заголовок и отсортированные данные
echo "$header"
echo "$data"

# Удаляем временный файл (опционально)
# rm -f "$OUTPUT_FILE"