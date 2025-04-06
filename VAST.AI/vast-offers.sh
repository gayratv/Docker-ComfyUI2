#!/bin/bash

# Сохраняем заголовок и данные в отдельные переменные
header=$(vastai search offers 'num_gpus=1 gpu_name=RTX_3090 inet_down>=5000 cpu_ram>=64' | \
awk 'NR == 1 {
       printf "ID\tCUDA\tModel\tvCPUs\tRAM\t%s$/hr%s\tNet_down\tmach_id\tstatus\thost_id\tports\tcountry\n", "\033[34m", "\033[0m";
       next
     }')

data=$(vastai search offers 'num_gpus=1 gpu_name=RTX_3090 inet_down>=5000 cpu_ram>=64' | \
awk 'NR > 1 {
       printf "%s\t%s\t%s\t%s\t%s\t%.2f\t%s\t%s\t%s\t%s\t%s\t%s\n",
              $1, $2, $4, $7, $8, $10, $15, $19, $20, $21, $22, $23
     }' | \
sort -k6,6n)

# Выводим заголовок и отсортированные данные
echo "$header"
echo "$data" | column -t -s $'\t'