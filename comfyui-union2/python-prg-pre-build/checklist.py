# source /mnt/f/_prg/python/Docker-ComfyUI/.venv/bin/activate
# cd /mnt/f/_prg/python/Docker-ComfyUI/comfyui-union2/python-prg-pre-build/
# python3 checklist.py

import os
import sys
import termios
import tty


class Checklist:
    def __init__(self, items):
        self.items = [{"text": item, "checked": False} for item in items]
        self.selected_index = 0

    def display(self):
        os.system('clear')  # Clear the terminal screen
        print("Используйте стрелки Вверх/Вниз для навигации, Пробел для выбора/снятия выбора.")
        # Добавлена строка с подсказкой
        print("Для окончания выбора нажмите Enter.\n")

        for i, item in enumerate(self.items):
            checkbox = "[x]" if item["checked"] else "[ ]"
            if i == self.selected_index:
                print(f"> {checkbox} {item['text']}")
            else:
                print(f"  {checkbox} {item['text']}")

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # ANSI escape code for arrow keys
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def run(self):
        while True:
            self.display()
            key = self.get_key()

            if key == '\x1b[A':  # Up arrow
                self.selected_index = max(0, self.selected_index - 1)
            elif key == '\x1b[B':  # Down arrow
                self.selected_index = min(len(self.items) - 1, self.selected_index + 1)
            elif key == ' ':  # Spacebar
                self.items[self.selected_index]["checked"] = not self.items[self.selected_index]["checked"]
            elif key == '\r':  # Enter key
                break
            elif key == '\x03':  # Ctrl+C to exit
                print("\nВыход.")
                sys.exit(0)

        return [item["text"] for item in self.items if item["checked"]]


# --- Как использовать ---
if __name__ == "__main__":
    my_list = [
        "Купить молоко",
        "Заплатить за интернет",
        "Позвонить другу",
        "Написать отчёт",
        "Пойти на тренировку"
    ]

    checklist = Checklist(my_list)
    selected_items = checklist.run()

    os.system('clear')  # Очистить экран перед показом результатов
    print("Вы выбрали следующие пункты:")
    if selected_items:
        for item in selected_items:
            print(f"- {item}")
    else:
        print("Ничего не выбрано.")