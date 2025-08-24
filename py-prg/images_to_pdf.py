#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python3 -m pip install --upgrade pillow

'''
Как использовать
# базовый случай: все изображения из папки ./images -> output.pdf

export CODE_DIR="/mnt/f/_prg/python/Docker-ComfyUI/py-prg"
export IMG_DIR="/mnt/f/tempg/_DOWNLOADS"
python3 "$CODE_DIR/images_to_pdf.py" "$IMG_DIR" -o output.pdf

# A4, портрет, поля 10 мм, вписать целиком
python images_to_pdf.py ./images -o album.pdf --page A4 --orientation portrait --margins-mm 10 --fit fit

# Letter, альбомная, заполнить страницу (возможна обрезка), поля 5 мм
python images_to_pdf.py ./images -o album.pdf --page Letter --orientation landscape --margins-mm 5 --fit fill

# Авторазмер по первой картинке + сортировка по времени изменения
python images_to_pdf.py ./images -o out.pdf --page Auto --sort mtime

# Серый цвет и ограничить первыми 300 файлами
python images_to_pdf.py ./images -o out.pdf --grayscale --limit 300

# Разрезать длинные изображения на части высотой 2445 (или своим значением)
python images_to_pdf.py ./images -o out.pdf --long-height 2445
'''

import argparse
import os
import sys
import time
from pathlib import Path
from PIL import Image, ImageOps

# Попытка подключить HEIC/HEIF, если установлен pillow-heif
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except Exception:
    pass

SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".heic", ".heif"}

PAGE_SIZES_MM = {
    "A4": (210, 297),      # мм
    "LETTER": (216, 279),  # мм
}

def mm_to_px(mm, dpi):
    return int(round(mm * dpi / 25.4))

def natural_key(s: str):
    """Естественная сортировка: file2 < file10."""
    import re
    return [int(t) if t.isdigit() else t.lower()
            for t in re.split(r'(\d+)', s)]

def collect_images(input_dir: Path, pattern: str):
    if pattern:
        files = sorted(input_dir.glob(pattern))
    else:
        files = []
        for p in sorted(input_dir.iterdir(), key=lambda p: p.name.lower()):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXT:
                files.append(p)
    return files

def load_and_prepare(img_path: Path):
    img = Image.open(img_path)
    # Учитываем EXIF-поворот
    img = ImageOps.exif_transpose(img)
    # Приводим к RGB (убираем альфу/CMYK/P/…)
    if img.mode not in ("RGB", "L"):
        if img.mode in ("RGBA", "LA"):
            # заливаем на белый фон
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")
    return img

def split_long_image(img: Image.Image, slice_height: int):
    """Разрезает изображение по высоте на части высотой slice_height (последняя может быть короче)."""
    parts = []
    w, h = img.size
    if h <= slice_height:
        return [img]
    for top in range(0, h, slice_height):
        box = (0, top, w, min(top + slice_height, h))
        parts.append(img.crop(box))
    return parts

def resize_to_page(image: Image.Image, page_px: tuple[int, int], margins_px: tuple[int, int, int, int], mode: str):
    """
    mode: "fit" — вписать целиком (с полями),
          "fill" — заполнить страницу (возможна обрезка),
          "none" — не менять размер, центрировать.
    """
    pw, ph = page_px
    left, top, right, bottom = margins_px
    tw = max(1, pw - left - right)
    th = max(1, ph - top - bottom)

    if mode == "none":
        # Просто разместим по центру поля
        canvas = Image.new("RGB", (pw, ph), (255, 255, 255))
        x = left + (tw - image.width) // 2
        y = top + (th - image.height) // 2
        canvas.paste(image, (x, y))
        return canvas

    iw, ih = image.size
    if mode == "fit":
        scale = min(tw / iw, th / ih)
        nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
        img2 = image.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new("RGB", (pw, ph), (255, 255, 255))
        x = left + (tw - nw) // 2
        y = top + (th - nh) // 2
        canvas.paste(img2, (x, y))
        return canvas

    if mode == "fill":
        # Масштабируем, затем обрезаем по центру в окно (tw x th)
        scale = max(tw / iw, th / ih)
        nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
        img2 = image.resize((nw, nh), Image.LANCZOS)
        # Обрезаем до (tw x th) из центра
        cx, cy = nw // 2, nh // 2
        left_crop = max(0, cx - tw // 2)
        top_crop = max(0, cy - th // 2)
        img2 = img2.crop((left_crop, top_crop, left_crop + tw, top_crop + th))
        canvas = Image.new("RGB", (pw, ph), (255, 255, 255))
        canvas.paste(img2, (left, top))
        return canvas

    raise ValueError("Unknown resize mode")

def compute_page_size(args, first_image: Image.Image):
    dpi = args.dpi
    margins_mm = tuple(float(m) for m in args.margins_mm.split(","))
    if len(margins_mm) == 1:
        ml = mt = mr = mb = margins_mm[0]
    elif len(margins_mm) == 2:
        ml = mr = margins_mm[0]
        mt = mb = margins_mm[1]
    elif len(margins_mm) == 4:
        ml, mt, mr, mb = margins_mm
    else:
        raise ValueError("margins-mm должен быть из 1, 2 или 4 чисел")

    if args.page.upper() == "AUTO":
        # Страница под размер изображения при указанном DPI + поля
        iw, ih = first_image.size
        # Размер страницы = поля + картинка (в режиме fit она уменьшится, но база — от первой)
        pw = mm_to_px(ml + mr, dpi) + iw
        ph = mm_to_px(mt + mb, dpi) + ih
        orientation = args.orientation.upper()
        if orientation == "PORTRAIT" and pw > ph:
            pw, ph = ph, pw
        elif orientation == "LANDSCAPE" and ph > pw:
            pw, ph = ph, pw
    else:
        base = PAGE_SIZES_MM.get(args.page.upper())
        if not base:
            raise ValueError(f"Неизвестный размер страницы: {args.page}")
        w_mm, h_mm = base
        orientation = args.orientation.upper()
        if orientation == "LANDSCAPE":
            w_mm, h_mm = h_mm, w_mm
        pw = mm_to_px(w_mm, dpi)
        ph = mm_to_px(h_mm, dpi)

    margins_px = (
        mm_to_px(ml, dpi),
        mm_to_px(mt, dpi),
        mm_to_px(mr, dpi),
        mm_to_px(mb, dpi),
    )
    return (pw, ph), margins_px

def main():
    parser = argparse.ArgumentParser(
        description="Собрать PDF из изображений с возможным разрезанием длинных картинок."
    )
    parser.add_argument("input_dir", type=str, help="Папка с изображениями")
    parser.add_argument("-o", "--output", type=str, default="output.pdf", help="Имя выходного PDF")
    parser.add_argument("-p", "--pattern", type=str, default="", help="Шаблон отбора, напр. '*.jpg' (если пусто — все поддерживаемые)")
    parser.add_argument("--sort", choices=["name", "natural", "mtime"], default="natural", help="Сортировка файлов")
    parser.add_argument("--page", default="A4", help="Размер страницы: A4, Letter, Auto")
    parser.add_argument("--orientation", choices=["auto", "portrait", "landscape"], default="auto", help="Ориентация страницы")
    parser.add_argument("--fit", choices=["fit", "fill", "none"], default="fit", help="Режим размещения изображения на странице")
    parser.add_argument("--margins-mm", default="10", help="Поля, мм: один (10), два (10,15) или четыре (10,15,10,15)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI страницы (влияет на итоговое разрешение PDF)")
    parser.add_argument("--grayscale", action="store_true", help="Конвертировать страницы в градации серого")
    parser.add_argument("--limit", type=int, default=0, help="Ограничить кол-во изображений (0 — без лимита)")

    # Новая опция: если высота изображения > long-height, разрезать на части высотой long-height
    parser.add_argument("--long-height", type=int, default=2445, help="Если изображение выше этого порога — будет разрезано на страницы такой высоты (по умолчанию 2445)")

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"❌ Папка не найдена: {input_dir}")
        sys.exit(1)

    files = collect_images(input_dir, args.pattern)
    if not files:
        print("❌ Изображений не найдено.")
        sys.exit(1)

    # Сортировка
    if args.sort == "mtime":
        files.sort(key=lambda p: p.stat().st_mtime)
    elif args.sort == "name":
        files.sort(key=lambda p: p.name.lower())
    else:  # natural
        files.sort(key=lambda p: natural_key(p.name))

    if args.limit > 0:
        files = files[:args.limit]

    # Подготовим первую страницу, чтобы вычислить размер листа
    first = load_and_prepare(files[0])
    if args.orientation == "auto":
        # Автоориентация по первой картинке
        args.orientation = "landscape" if first.width >= first.height else "portrait"

    page_px, margins_px = compute_page_size(args, first)

    pages = []
    total = len(files)
    start_t = time.time()

    for idx, fp in enumerate(files, 1):
        try:
            img = load_and_prepare(fp)
            if args.grayscale:
                img = img.convert("L").convert("RGB")

            # Если картинка длиннее порога — режем на части по высоте long-height
            parts = split_long_image(img, args.long_height) if img.height > args.long_height else [img]

            for part in parts:
                page = resize_to_page(part, page_px, margins_px, args.fit)
                pages.append(page)

            if idx % 25 == 0 or idx == total:
                print(f"… обработано {idx}/{total}")
        except Exception as e:
            print(f"⚠️ Пропуск {fp.name}: {e}")

    if not pages:
        print("❌ Нет валидных изображений для PDF.")
        sys.exit(1)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем мультистраничный PDF
    first_page = pages[0]
    other_pages = pages[1:]
    first_page.save(
        out,
        save_all=True,
        append_images=other_pages,
        resolution=args.dpi,
        quality=95,
    )

    dt = time.time() - start_t
    print(f"✅ Готово: {out} | страниц: {len(pages)} | заняло: {dt:.1f} c")

if __name__ == "__main__":
    main()
