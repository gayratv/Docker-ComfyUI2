#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

python3 -m pip install pruna

rm -rf /root/.cache/pip

