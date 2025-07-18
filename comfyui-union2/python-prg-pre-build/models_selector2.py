#!/usr/bin/env python3
r"""
Tree‑Selector: просмотр и выбор *.txt‑файлов моделей с крупным шрифтом
=====================================================================

• Показывает древовидную структуру каталога в `ttk.Treeview`.
• Файлы отмечаются / снимаются двойным кликом по строке (☐ → ☑).
• Выбранные элементы можно отобразить во всплывающем окне и в консоли.

Требования ― только стандартная библиотека Python 3 (tkinter).

Измените константу ROOT_DIR ниже, если модели лежат в другом месте.
"""

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, font

# ───── НАСТРОЙКИ ──────────────────────────────────────────────────────
ROOT_DIR = Path(r"F:\_prg\python\Docker-ComfyUI\comfyui-union2\aria2\templates\models")
BASE_FONT_SIZE = 16   # кегль текста в пунктах
SCALING        = 1.0  # общий коэффициент DPI (1.0 = стандартный)

# ───── ПРИЛОЖЕНИЕ ─────────────────────────────────────────────────────
class TreeSelector(tk.Tk):
    def __init__(self, root_path: Path):
        super().__init__()

        # 1) глобальное масштабирование интерфейса
        self.tk.call("tk", "scaling", SCALING)

        # 2) шрифт по умолчанию + отдельный шрифт для дерева/кнопок
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=BASE_FONT_SIZE)
        big_font = font.Font(size=BASE_FONT_SIZE)

        self.title("Выбор .txt‑файлов моделей")
        self.geometry("800x550")

        # ── Treeview с невидимым столбцом `fullpath` ───────────────────
        self.tree = ttk.Treeview(
            self,
            columns=("fullpath",),
            show="tree",
            style="Big.Treeview"
        )
        self.tree.column("fullpath", width=0, stretch=False)  # скрыть столбец
        self.tree.tag_configure("file", font=big_font)

        ysb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        ysb.pack(side="right", fill="y")

        # набор отмеченных относительных путей
        self.checked: set[str] = set()

        # заполнить дерево
        self._populate("", root_path)

        # двойной клик = переключить отметку
        # self.tree.bind("<Double-1>", self._toggle_check)
        self.tree.bind("<Button-1>", self._toggle_check)

        # крупная кнопка
        ttk.Style().configure("Big.TButton", font=big_font)
        ttk.Button(
            self,
            text="Показать выбранные",
            style="Big.TButton",
            command=self.show_selected,
        ).pack(pady=8)

    # ───── внутренние методы ──────────────────────────────────────────
    def _populate(self, parent: str, path: Path) -> None:
        """Рекурсивно добавляет каталоги и *.txt‑файлы в дерево."""
        for p in sorted(path.iterdir()):
            if p.is_dir():
                nid = self.tree.insert(parent, "end", text=p.name, open=False)
                self._populate(nid, p)
            elif p.suffix.lower() == ".txt":
                rel = p.relative_to(ROOT_DIR).as_posix()
                self.tree.insert(
                    parent,
                    "end",
                    text="☐ " + p.name,       # начальная «пустая» галочка
                    values=(rel,),            # относительный путь
                    tags=("file",),
                )

    def _toggle_check(self, event) -> None:
        """Включает/выключает чек‑бокс по двойному клику."""
        item = self.tree.identify_row(event.y)
        if not item or "file" not in self.tree.item(item, "tags"):
            return  # кликнули не по файлу
        text = self.tree.item(item, "text")
        rel_path = self.tree.set(item, "fullpath")
        if text.startswith("☐"):
            self.tree.item(item, text="☑ " + text[2:])
            self.checked.add(rel_path)
        else:
            self.tree.item(item, text="☐ " + text[2:])
            self.checked.discard(rel_path)

    def show_selected(self) -> None:
        """Выводит список отмеченных файлов."""
        if not self.checked:
            messagebox.showinfo("Выбор", "Ничего не выбрано.")
        else:
            chosen = "\n".join(sorted(self.checked))
            messagebox.showinfo("Выбор", chosen)
            print("Выбрано:", *sorted(self.checked), sep="\n")

# ───── ЗАПУСК ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not ROOT_DIR.exists():
        raise SystemExit(f"Каталог {ROOT_DIR} не найден.")
    TreeSelector(ROOT_DIR).mainloop()
