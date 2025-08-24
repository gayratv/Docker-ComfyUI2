#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python3 -m pip install --upgrade pillow
"""
export CODE_DIR="/mnt/f/_prg/python/Docker-ComfyUI/py-prg"
export IMG_DIR="/mnt/f/tempg/_DOWNLOADS"
python3 "$CODE_DIR/images_to_pdf2.py" "$IMG_DIR" -o output.pdf --long-height 2445 \
         --auto-trim-sides --auto-trim-tol 10 --auto-trim-minrun 12 \
         --trim-left 260 \
         --trim-right 260

260

Новый функционал:
- --long-height N        — разрезать длинные изображения на слайсы высотой N
- --trim-left N          — жёстко обрезать слева N пикселей
- --trim-right N         — жёстко обрезать справа N пикселей
- --auto-trim-sides      — автоматически обрезать однотонные поля слева/справа
- --auto-trim-tol N      — допуск различий RGB (по каналу) для автообрезки (по умолчанию 8)
- --auto-trim-minrun N   — минимальная ширина однотонной кромки, чтобы считать её полем (по умолчанию 10)

Примеры:
  python images_to_pdf.py ./images -o out.pdf --long-height 2445 \
         --auto-trim-sides --auto-trim-tol 10 --auto-trim-minrun 12

  python images_to_pdf.py ./images -o out.pdf --trim-left 40 --trim-right 40
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Tuple
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
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


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
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")
    return img


def column_is_bg(im: Image.Image, x: int, ref: Tuple[int, int, int], tol: int) -> bool:
    """Колонка x достаточно близка к ref по всем пикселям (RGB) в пределах tol."""
    r_ref, g_ref, b_ref = ref
    w, h = im.size
    # Берём полосу в 1px шириной
    col = im.crop((x, 0, x + 1, h)).convert("RGB").getdata()
    for r, g, b in col:
        if abs(r - r_ref) > tol or abs(g - g_ref) > tol or abs(b - b_ref) > tol:
            return False
    return True


def sample_side_color(im: Image.Image, side: str, band: int = 3) -> Tuple[int, int, int]:
    """Средний цвет первых/последних band колонок."""
    w, h = im.size
    if side == "left":
        box = (0, 0, min(band, w), h)
    else:
        box = (max(0, w - band), 0, w, h)
    region = im.crop(box).convert("RGB")
    pixels = list(region.getdata())
    n = len(pixels)
    r = sum(p[0] for p in pixels) // max(1, n)
    g = sum(p[1] for p in pixels) // max(1, n)
    b = sum(p[2] for p in pixels) // max(1, n)
    return (r, g, b)


def detect_side_margins(im: Image.Image, tol: int = 8, min_run: int = 10) -> Tuple[int, int]:
    """Возвращает (left_px, right_px) — ширины однотонных полей слева/справа."""
    w, h = im.size
    if w == 0:
        return (0, 0)

    left_ref = sample_side_color(im, "left")
    right_ref = sample_side_color(im, "right")

    # Скан слева
    left = 0
    run = 0
    for x in range(w):
        if column_is_bg(im, x, left_ref, tol):
            run += 1
        else:
            left = run if run >= min_run else 0
            break
    else:
        left = w // 2

    # Скан справа
    right = 0
    run = 0
    for x in range(w - 1, -1, -1):
        if column_is_bg(im, x, right_ref, tol):
            run += 1
        else:
            right = run if run >= min_run else 0
            break
    else:
        right = w // 2

    return (left, right)


def apply_side_trims(im: Image.Image, manual_left: int, manual_right: int,
                     auto: bool, tol: int, min_run: int) -> Image.Image:
    w, h = im.size
    left_auto, right_auto = (0, 0)
    if auto:
        left_auto, right_auto = detect_side_margins(im, tol=tol, min_run=min_run)
    x0 = max(0, min(w, manual_left + left_auto))
    x1 = max(x0 + 1, w - max(0, manual_right + right_auto))
    if x1 <= x0:
        return im  # защитимся от некорректной обрезки
    return im.crop((x0, 0, x1, h))


def split_long_image(img: Image.Image, slice_height: int):
    parts = []
    w, h = img.size
    if h <= slice_height:
        return [img]
    for top in range(0, h, slice_height):
        box = (0, top, w, min(top + slice_height, h))
        parts.append(img.crop(box))
    return parts


def resize_to_page(image: Image.Image, page_px: tuple[int, int], margins_px: tuple[int, int, int, int], mode: str):
    pw, ph = page_px
    left, top, right, bottom = margins_px
    tw = max(1, pw - left - right)
    th = max(1, ph - top - bottom)

    if mode == "none":
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
        scale = max(tw / iw, th / ih)
        nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
        img2 = image.resize((nw, nh), Image.LANCZOS)
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
        iw, ih = first_image.size
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
        description="Собрать PDF из изображений с разрезанием длинных и обрезкой боковых полей."
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

    # Разрезание длинных
    parser.add_argument("--long-height", type=int, default=2445, help="Если изображение выше этого порога — будет разрезано на страницы такой высоты (по умолчанию 2445)")

    # Ручная обрезка сторон
    parser.add_argument("--trim-left", type=int, default=0, help="Жёстко обрезать слева N пикселей")
    parser.add_argument("--trim-right", type=int, default=0, help="Жёстко обрезать справа N пикселей")

    # Авто обрезка однотонных боковых полей
    parser.add_argument("--auto-trim-sides", action="store_true", help="Автоматически обрезать однотонные поля слева/справа")
    parser.add_argument("--auto-trim-tol", type=int, default=8, help="Толеранс (по каналу) для автообрезки (по умолчанию 8)")
    parser.add_argument("--auto-trim-minrun", type=int, default=10, help="Мин. ширина однотонной кромки в пикселях (по умолчанию 10)")

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
    # Обрезка боков (auto/manual) применяется до вычисления листа, чтобы подгонять авторазмер точнее
    first = apply_side_trims(
        first,
        manual_left=args.trim_left,
        manual_right=args.trim_right,
        auto=args.auto_trim_sides,
        tol=args.auto_trim_tol,
        min_run=args.auto_trim_minrun,
    )

    if args.orientation == "auto":
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

            # Применяем обрезку боков (auto/manual)
            img = apply_side_trims(
                img,
                manual_left=args.trim_left,
                manual_right=args.trim_right,
                auto=args.auto_trim_sides,
                tol=args.auto_trim_tol,
                min_run=args.auto_trim_minrun,
            )

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
