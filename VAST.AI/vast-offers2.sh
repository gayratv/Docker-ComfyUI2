#!/bin/bash

# Проверяем, что переданы все необходимые аргументы
if [ "$#" -ne 4 ]; then
    echo "Использование: $0 num_gpus gpu_name inet_down cpu_ram"
    echo "Пример: $0 1 RTX_3090 5000 64"
    exit 1
fi

# Присваиваем аргументы переменным (локально)
NUM_GPUS=$1
GPU_NAME=$2
INET_DOWN=$3
CPU_RAM=$4
CUDA_VERS="12.4"

# Файл для сохранения выходных данных vastai search offers
OUTPUT_FILE="vast-search-offers.txt"

# Формируем строку команды
COMMAND="vastai search offers 'num_gpus=$NUM_GPUS' 'gpu_name=$GPU_NAME' 'inet_down>=$INET_DOWN' 'cpu_ram>=$CPU_RAM' 'cuda_vers>=$CUDA_VERS'"

eval "$COMMAND" > "$OUTPUT_FILE"

# 1           2    3  4         5        6      7       8    9     10      11     12         13   14          15      16       17    18        19         20        21     22       23
# ID        CUDA   N  Model     PCIE  cpu_ghz  vCPUs    RAM  Disk  $/hr    DLP    DLP/$   score  NV Driver   Net_up  Net_down  R     Max_Days  mach_id  status    host_id  ports   country
# 1                   4                  6      7       8          10                                                 16                       19                 21                23


awk -F '[ \t]+' '
    NR==1 {
        printf "%-9s %-7s %-8s %-6s %-6s %-10s %-9s %-9s %-9s %-6s %s\n", "ID", "$/hr", "cpu_ghz", "vCPUs", "RAM", "Net_down", "mach_id", "host_id", "Model", "CUDA", "country"
        print "----------------------------------------------------------------------------------------------------------------------------------------------------"
        next
    }
    {
        printf "%-9s %-7s %-8s %-6s %-6s %-10s %-9s %-9s %-9s %-6s %s\n", $1, $10, $6, $7, $8, $16, $19, $21, $4, $2, $23
    }
' "$OUTPUT_FILE"
