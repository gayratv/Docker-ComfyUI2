#!/usr/bin/env python3
r"""
Графический выбор *.txt‑файлов моделей (tkinter).

Путь по‑умолчанию: F:\_prg\python\Docker-ComfyUI\comfyui-union2\aria2\templates\models
"""

from pathlib import Path
import sys
import tkinter as tk
from tkinter import ttk, messagebox

ROOT_DIR = Path(
    r"F:\_prg\python\Docker-ComfyUI\comfyui-union2\aria2\templates\models"
).expanduser()


def build_tree(root: Path) -> dict:
    tree: dict = {}
    for path in root.rglob("*.txt"):
        parts = path.relative_to(root).parts
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault("_files", []).append("/".join(parts))
    return tree


class SelectorApp(tk.Tk):
    def __init__(self, root_path: Path):
        super().__init__()
        self.title("Выбор .txt‑файлов моделей")
        self.geometry("640x720")

        canvas = tk.Canvas(self, borderwidth=0)
        vbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        self.inner = tk.Frame(canvas)

        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)
        vbar.pack(side="right", fill="y")

        self.inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        # Список кортежей (var, относительный_путь)
        self.items: list[tuple[tk.IntVar, str]] = []
        self._populate(self.inner, build_tree(root_path))

        ttk.Button(self, text="Показать выбранные", command=self.show_selected).pack(
            pady=10
        )

    # ------------------------------------------------------------------ private
    def _populate(self, parent: tk.Widget, subtree: dict, indent: int = 0):
        for key in sorted(subtree):
            if key == "_files":
                for rel_path in sorted(subtree["_files"]):
                    var = tk.IntVar()
                    chk = tk.Checkbutton(
                        parent,
                        text=rel_path.split("/")[-1],
                        variable=var,
                        onvalue=1,
                        offvalue=0,
                    )
                    chk.pack(anchor="w", padx=indent + 20)
                    self.items.append((var, rel_path))
            else:
                ttk.Label(
                    parent, text=key, font=("TkDefaultFont", 10, "bold")
                ).pack(anchor="w", padx=indent + 5, pady=2)
                sub = tk.Frame(parent)
                sub.pack(anchor="w")
                self._populate(sub, subtree[key], indent + 15)

    def show_selected(self):
        chosen = [p for var, p in self.items if var.get()]
        if not chosen:
            messagebox.showinfo("Выбор", "Ничего не выбрано.")
        else:
            messagebox.showinfo("Выбор", "\n".join(chosen))
            print("Выбрано:")
            for p in chosen:
                print(p)


if __name__ == "__main__":
    if not ROOT_DIR.exists():
        sys.exit(f"Каталог {ROOT_DIR} не найден.")
    SelectorApp(ROOT_DIR).mainloop()
