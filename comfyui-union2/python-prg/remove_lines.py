import os
import re

filename = "/workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/manager_util.py"
# filename =r"D:\1\ComfyUI-Manager\glob\manager_util.py"

# Регулярные выражения для поиска строк (с любыми отступами)
line1 = re.compile(r'^\s*if not silent:\s*$')
line2 = re.compile(r'^\s*logging\.info\(f"\[ComfyUI-Manager\] default cache updated: \{.*?\}"\)')


with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    # Проверяем совпадение первой строки
    if line1.match(lines[i]):
        # Проверяем, есть ли вторая строка после неё
        if i + 1 < len(lines) and line2.match(lines[i+1]):
            i += 2  # Пропускаем обе строки
            continue
    new_lines.append(lines[i])
    i += 1

# Перезаписываем файл
with open(filename, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Готово: строки удалены из '{filename}'")


filename = "/workspace/ComfyUI/custom_nodes/ComfyUI-Manager/glob/manager_server.py"
# filename =r"D:\1\ComfyUI-Manager\glob\manager_server.py"

# Регулярное выражение для поиска нужной строки (с любыми отступами)

target_line = re.compile(
    r'^\s*logging\.info\(f"\[ComfyUI-Manager\] default cache updated: \{uri\}"\)'
)

with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if not target_line.match(line):
        new_lines.append(line)

with open(filename, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Готово: строка удалена из '{filename}'")

# python3 remove_lines.py