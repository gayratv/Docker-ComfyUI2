#!/bin/bash

# Проверяем, существует ли файл
if [[ ! -f "vast-instance-raw.txt" ]]; then
  echo "Файл vast-instance-raw.txt не найден."
  exit 1
fi

# Парсим JSON и экспортируем переменные
VAST_PUBLIC_IPADDR=$(jq -r '.public_ipaddr' vast-instance-raw.txt)
VAST_ACTUAL_STATUS=$(jq -r '.actual_status' vast-instance-raw.txt)
VAST_STATUS_MSG=$(jq -r '.status_msg' vast-instance-raw.txt)
VAST_SSH=$(jq -r '.ports["22/tcp"][0].HostPort' vast-instance-raw.txt)
VAST_COMFY=$(jq -r '.ports["8188/tcp"][0].HostPort' vast-instance-raw.txt)


# Экспортируем переменные окружения
export VAST_PUBLIC_IPADDR
export VAST_ACTUAL_STATUS
export VAST_STATUS_MSG
export VAST_SSH
export VAST_COMFY

# Выводим значения для проверки
echo "VAST_ACTUAL_STATUS=$VAST_ACTUAL_STATUS"
echo "VAST_STATUS_MSG=$VAST_STATUS_MSG"
echo ""
echo "VAST_PUBLIC_IPADDR=$VAST_PUBLIC_IPADDR"
echo "VAST_SSH=$VAST_SSH"
echo "VAST_COMFY=$VAST_COMFY"