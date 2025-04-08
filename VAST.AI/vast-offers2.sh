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

# QUESTION="'num_gpus=$NUM_GPUS' 'gpu_name=$GPU_NAME' 'inet_down>=$INET_DOWN' 'cpu_ram>=$CPU_RAM' 'cuda_vers>=12.4'"
# QUESTION=("num_gpus=$NUM_GPUS" "gpu_name=$GPU_NAME" "inet_down>=$INET_DOWN" "cpu_ram>=$CPU_RAM" "cuda_vers>=12.4")
#QUESTION=("'num_gpus=$NUM_GPUS'" "'gpu_name=$GPU_NAME'" "'inet_down>=$INET_DOWN'" "'cpu_ram>=$CPU_RAM'" "'cuda_vers>=12.4'")
#echo "vastai search offers ${QUESTION[@]}"
# vastai search offers 'num_gpus=1' 'gpu_name=RTX_4090' 'inet_down>=5000' 'cpu_ram>=32' 'cuda_vers>=12.4'

# vastai search offers "$QUESTION" > "$OUTPUT_FILE"
# eval vastai search offers $QUESTION > "$OUTPUT_FILE"
#vastai search offers "${QUESTION[@]}" > "$OUTPUT_FILE"

QUESTION=("num_gpus=$NUM_GPUS" "gpu_name=$GPU_NAME" "inet_down>=$INET_DOWN" "cpu_ram>=$CPU_RAM" "cuda_vers>=12.4")
#bash -c 'vastai search offers '"${QUESTION[@]}"' > "$OUTPUT_FILE"'
#bash -c 'vastai search offers '"${QUESTION[@]}"' > vast-search-offers.txt'
bash -c "vastai search offers ${QUESTION[@]} > vast-search-offers.txt"

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