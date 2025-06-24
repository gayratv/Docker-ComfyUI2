#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

pip install --cache-dir=/root/pip-cache -U "numpy==2.2.3"

rm -rf /root/.cache/pip