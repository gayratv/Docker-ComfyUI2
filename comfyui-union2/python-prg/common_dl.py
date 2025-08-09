#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Разбор входных данных aria2 и разделение на civitai.txt и hf.txt + запуск aria2c.

Как это работает:
    - Вход — текстовый файл с блоками. Каждый блок начинается строкой-URL:
        https://civitai.com ...  или  https://huggingface.co ...
      Далее в блоке могут идти строки вида:
        out=...
        dir=...
      Порядок строк произвольный, допускаются отступы. Новый блок начинается,
      когда встречается очередная строка, начинающаяся с "https://".
    - Для civitai:
        * URL очищается; к нему добавляется параметр &token={CIVITAI_TOKEN}, если его ещё нет;
        * блок записывается в civitai.txt.
    - Для huggingface:
        * блок записывается в hf.txt.
    - Преобразование пути dir=:
        dir=models/...  →  dir={prefix}/models/...
        где {prefix} задаётся через --prefix (по умолчанию /workspace/ComfyUI/).
    - Переменные окружения обязательны: CIVITAI_TOKEN и HF_TOKEN.
      Если одна из них отсутствует — скрипт завершится с сообщением об ошибке.
    - После формирования файлов запускается aria2c (напрямую, без перехвата вывода):
        * для hf.txt:
            aria2c --input-file=hf.txt ... --header="Authorization: Bearer $HF_TOKEN"
        * для civitai.txt:
            aria2c --input-file=civitai.txt ... (без заголовка)

Пример входных данных:
    # 🌟 antelopev2 🌟
    https://huggingface.co/Gayrat1968/antelopev2/resolve/main/1k3d68.onnx
          dir=models/insightface/models/antelopev2
          out=1k3d68.onnx

    # LORA SDXL Storyboard Sketch
    https://civitai.com/api/download/models/182532?type=Model&format=SafeTensor
        out=Storyboard_sketch.safetensors
        dir=models/loras/SDXL

Пример запуска:
    export CIVITAI_TOKEN="ваш_civitai_token"
    export HF_TOKEN="ваш_hf_token"
    python3 script.py input.txt

cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/python-prg/download-models
python3 common_dl.py models.txt --prefix /mnt/d/_tmp
    # Результат: civitai.txt и hf.txt + автоматическая загрузка через aria2c

Параметры:
    input          (позиционный, обязателен) — путь к файлу с данными aria2
    --prefix       Префикс для dir= (по умолчанию /workspace/ComfyUI/)
    --civitai-out  Выходной файл для civitai (по умолчанию civitai.txt)
    --hf-out       Выходной файл для huggingface (по умолчанию hf.txt)
"""

import argparse
import os
import sys
import subprocess
from typing import List, Dict, Optional


def abort(message: str, code: int = 1) -> None:
    """Завершить работу с сообщением об ошибке."""
    print(f"Ошибка: {message}", file=sys.stderr)
    sys.exit(code)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Разбор aria2 input: разделить на civitai.txt и hf.txt, "
                    "переписать dir с префиксом, добавить civitai token и запустить aria2c."
    )
    p.add_argument(
        "input",
        help="Путь к входному файлу с данными aria2"
    )
    p.add_argument(
        "--prefix",
        default="/workspace/ComfyUI/",
        help="Префикс для dir= (по умолчанию: /workspace/ComfyUI/)"
    )
    p.add_argument(
        "--civitai-out",
        default="civitai2.txt",
        help="Файл вывода для civitai (по умолчанию civitai.txt)"
    )
    p.add_argument(
        "--hf-out",
        default="hf2.txt",
        help="Файл вывода для huggingface (по умолчанию hf.txt)"
    )
    return p.parse_args()


class Block:
    def __init__(self) -> None:
        self.url: Optional[str] = None
        self.kv: Dict[str, str] = {}  # 'out' and 'dir'
        self.source: Optional[str] = None  # 'civitai' | 'hf' | None

    def is_empty(self) -> bool:
        return (self.url is None or not self.url.strip()) and not self.kv

    def finalize(self, prefix: str, civitai_token: str) -> None:
        if not self.url:
            return

        url = self.url.strip()
        if not url:
            return

        # определить источник
        if url.startswith("https://civitai.com"):
            self.source = "civitai"
            if "token=" not in url:
                sep = "&" if ("?" in url) else "?"
                url = f"{url}{sep}token={civitai_token}"
        elif url.startswith("https://huggingface.co"):
            self.source = "hf"
        else:
            self.source = None

        self.url = url  # сохранить очищенный/модифицированный URL

        # нормализовать dir=
        if "dir" in self.kv:
            value = self.kv["dir"].replace("\\", "/").lstrip("/")
            pref = prefix.replace("\\", "/")
            if not pref.endswith("/"):
                pref += "/"
            self.kv["dir"] = f"{pref}{value}"


def read_input_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        abort(f"входной файл не найден: {path}")
    except PermissionError:
        abort(f"нет прав на чтение файла: {path}")
    except OSError as e:
        abort(f"не удалось прочитать файл '{path}': {e.strerror}")


def iterate_blocks(lines: List[str]) -> List[Block]:
    blocks: List[Block] = []
    cur = Block()

    def push_current():
        nonlocal cur
        if not cur.is_empty():
            blocks.append(cur)
        cur = Block()

    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("https://"):
            push_current()
            cur.url = line
            continue

        if "=" in line:
            kv_line = line.strip()  # убираем пробелы по краям перед парсингом
            if kv_line.startswith(("out", "dir")):
                key, _, val = kv_line.partition("=")
                key = key.strip()
                val = val.strip()
                if key in ("out", "dir") and val:
                    cur.kv[key] = val
                continue

    push_current()
    return blocks


def format_block_for_aria2(b: Block) -> str:
    # порядок вывода: URL, затем out, затем dir (aria2 принимает в любом порядке)
    parts = [b.url] if b.url else []
    if "out" in b.kv:
        parts.append(f" out={b.kv['out']}")
    if "dir" in b.kv:
        parts.append(f" dir={b.kv['dir']}")
    return "\n".join(parts) + "\n"


def run_aria2_for_hf(new_model_file: str) -> int:
    """Запуск aria2c для HuggingFace (с auth header), вывод напрямую в терминал."""
    try:
        hf_token = os.environ["HF_TOKEN"]
    except KeyError:
        abort("не установлена переменная окружения HF_TOKEN")

    cmd = [
        "aria2c",
        f"--input-file={new_model_file}",
        "--allow-overwrite=false",
        "--auto-file-renaming=false",
        "--continue=true",
        "--max-connection-per-server=5",
        "--conditional-get=true",
        f"--header=Authorization: Bearer {hf_token}",
    ]
    try:
        # Вывод не перенаправляем — aria2 сам рисует прогресс
        completed = subprocess.run(cmd)
        return completed.returncode
    except FileNotFoundError:
        abort("aria2c не найден в PATH. Установите aria2 и повторите попытку.")
    except OSError as e:
        abort(f"ошибка запуска aria2c: {e.strerror}")


def run_aria2_for_civitai(new_model_file: str) -> int:
    """Запуск aria2c для Civitai (без auth header), вывод напрямую в терминал."""
    cmd = [
        "aria2c",
        f"--input-file={new_model_file}",
        "--allow-overwrite=false",
        "--auto-file-renaming=false",
        "--continue=true",
        "--max-connection-per-server=4",
        "--conditional-get=true",
    ]
    try:
        completed = subprocess.run(cmd)
        return completed.returncode
    except FileNotFoundError:
        abort("aria2c не найден в PATH. Установите aria2 и повторите попытку.")
    except OSError as e:
        abort(f"ошибка запуска aria2c: {e.strerror}")


def main():
    args = parse_args()

    civitai_token = os.environ.get("CIVITAI_TOKEN")
    hf_token = os.getenv("HF_TOKEN")
    if not civitai_token:
        abort("не установлена переменная окружения CIVITAI_TOKEN")
    if not hf_token:
        abort("не установлена переменная окружения HF_TOKEN")

    text = read_input_text(args.input)
    if not text.strip():
        abort("входной файл пустой")

    blocks = iterate_blocks(text.splitlines())
    civitai_blocks: List[str] = []
    hf_blocks: List[str] = []

    for b in blocks:
        b.finalize(prefix=args.prefix, civitai_token=civitai_token)  # type: ignore[arg-type]
        if not b.url or not b.source:
            continue
        content = format_block_for_aria2(b)
        if b.source == "civitai":
            civitai_blocks.append(content)
        elif b.source == "hf":
            hf_blocks.append(content)

    if not civitai_blocks and not hf_blocks:
        abort("не найдено ни одного блока с URL https://civitai.com или https://huggingface.co")

    try:
        if civitai_blocks:
            with open(args.civitai_out, "w", encoding="utf-8") as f:
                f.writelines(civitai_blocks)
        if hf_blocks:
            with open(args.hf_out, "w", encoding="utf-8") as f:
                f.writelines(hf_blocks)
    except PermissionError as e:
        abort(f"нет прав на запись выходных файлов: {e}")
    except OSError as e:
        abort(f"ошибка записи выходных файлов: {e.strerror}")

    # Запуски aria2c напрямую (виден родной прогресс)
    if hf_blocks:
        print("\n=== Загрузка из HuggingFace (aria2c / hf.txt) ===")
        code = run_aria2_for_hf(args.hf_out)
        if code != 0:
            abort(f"aria2c завершился с ошибкой (hf.txt), код {code}", code)

    if civitai_blocks:
        print("\n=== Загрузка из Civitai (aria2c / civitai.txt) ===")
        code = run_aria2_for_civitai(args.civitai_out)
        if code != 0:
            abort(f"aria2c завершился с ошибкой (civitai.txt), код {code}", code)


if __name__ == "__main__":
    main()
