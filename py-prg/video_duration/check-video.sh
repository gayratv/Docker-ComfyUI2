#!/bin/bash

# проверяет содержит ли видео файл ошибки

for f in *.mp4; do
  ffprobe -v error -i "$f" -f null -
  if [ $? -ne 0 ]; then
    echo "⚠️ Файл $f поврежден или имеет ошибки."
  else
    echo "✅ Файл $f в порядке."
  fi
done