#!/bin/bash

vastai search offers 'num_gpus=1 gpu_name=RTX_3090 inet_down>=1000 cpu_ram>=64' | \
awk 'NR == 1 {print "ID", "CUDA", "Model", "vCPUs", "RAM", "$/hr", "Net_down", "mach_id", "status", "host_id", "ports", "country"; next}
     {print $1, $2, $4, $7, $8, $10, $15, $19, $20, $21, $22, $23}' | \
sort -k6,6n | \
column -t
