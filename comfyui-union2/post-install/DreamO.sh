#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд

pip install --cache-dir=/root/pip-cache timm
rm -rf /root/.cache/pip

