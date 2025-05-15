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

def main(file_inp):
    try:
        with open(file_inp, encoding='utf-8') as f:
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
    file_inp='t.html'
    main(file_inp)
