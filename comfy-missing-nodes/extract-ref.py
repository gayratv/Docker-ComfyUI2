#!/usr/bin/env python3
import re
import argparse
import sys

def extract_hrefs(text):
    """
    Ищет все вхождения <a href="...ComfyUI_IPAdapter_plus..." …>
    и возвращает список совпадений атрибута href.
    """
    pattern = re.compile(
        r'<a\s+[^>]*?href\s*=\s*"(?P<href>https://github\.com/[^"]+)"[^>]*?>',
        re.IGNORECASE
    )
    return [m.group('href') for m in pattern.finditer(text)]

def main():
    parser = argparse.ArgumentParser(
        description='Извлекает из HTML-файла все href, содержащие ComfyUI_IPAdapter_plus'
    )
    parser.add_argument(
        '--file', '-f',
        default='t.html',
        help='Путь к входному HTML-файлу (по умолчанию: t.html)',
        metavar='FILE'
    )

    args = parser.parse_args()

    try:
        with open(args.file, encoding='utf-8') as f:
            content = f.read()
    except IOError as e:
        print(f"Ошибка при открытии файла: {e}", file=sys.stderr)
        sys.exit(1)

    hrefs = extract_hrefs(content)
    if not hrefs:
        print("Совпадений не найдено.", file=sys.stderr)
        sys.exit(2)

    for href in hrefs:
        print(href)

if __name__ == '__main__':
    main()
