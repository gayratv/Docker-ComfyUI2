#!/bin/bash
# Входной параметр (строка подключения)
# пример ssh -p 54396 root@180.1.36.175 -L 8080:localhost:8080
SSH_STRING="$1"

# Извлечение порта
export SSH_PORT=$(echo "$SSH_STRING" | awk -F" " '{for(i=1;i<=NF;i++) if($i=="-p") print $(i+1)}')

# Извлечение пользователя и хоста
export SSH_USER_HOST=$(echo "$SSH_STRING" | awk '{for(i=1;i<=NF;i++) if($i ~ /@/) print $i}')

# Путь к SSH-ключу
export SSH_KEY="~/.ssh/mvps/ud_rsa"

# Вывод переменных для проверки
echo "Экспортированные переменные:"
echo "SSH_PORT=$SSH_PORT"
echo "SSH_USER_HOST=$SSH_USER_HOST"
echo "SSH_KEY=$SSH_KEY"
