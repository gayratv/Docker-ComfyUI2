#!/bin/bash

set -e  # Выход при ошибке
set -x  # Логирование всех команд


pip install --cache-dir=/root/pip-cache  https://huggingface.co/mit-han-lab/nunchaku/resolve/main/nunchaku-0.3.0%2Btorch2.7-cp311-cp311-linux_x86_64.whl


#cd /workspace/
#git clone https://huggingface.co/mit-han-lab/nunchaku
#cd nunchaku
#
## 4. Устанавливаем пакет из локальной папки, сохраняя кэш в /root/pip-cache
#pip3 install --cache-dir=/root/pip-cache .




pip install --cache-dir=/root/pip-cache  apex
pip install --cache-dir=/root/pip-cache -U "numpy==2.2.3"

rm -rf /root/.cache/pip

