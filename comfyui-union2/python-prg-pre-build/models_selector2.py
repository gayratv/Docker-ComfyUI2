#!/usr/bin/env python3
r"""Выбор .txt‑файлов в ttk.Treeview с «галочками»."""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

ROOT_DIR = Path(r"F:\_prg\python\Docker-ComfyUI\comfyui-union2\aria2\templates\models")

class TreeSelector(tk.Tk):
    def __init__(self, root_path: Path):
        super().__init__()
        self.title("Выбор .txt‑файлов моделей")
        self.geometry("700x500")

        # ── Treeview ────────────────────────────────────────────────────────
        # columns=("fullpath",) → логический столбец для хранения пути
        self.tree = ttk.Treeview(self, columns=("fullpath",), show="tree")
        # «прячем» столбец: ширина 0 и убираем растяжение
        self.tree.column("fullpath", width=0, stretch=False)

        ysb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        ysb.pack(side="right", fill="y")

        self.checked: set[str] = set()
        self._populate("", root_path)

        self.tree.bind("<Double-1>", self._toggle_check)
        ttk.Button(self, text="Показать выбранные", command=self.show_selected
                   ).pack(pady=6)

    # ---------------------------------------------------------------- utils
    def _populate(self, parent: str, path: Path):
        """Рекурсивно заполняет дерево."""
        for p in sorted(path.iterdir()):
            if p.is_dir():
                nid = self.tree.insert(parent, "end", text=p.name, open=False)
                self._populate(nid, p)
            elif p.suffix == ".txt":
                rel = p.relative_to(ROOT_DIR).as_posix()
                # значения передаём сразу через `values=…`
                fid = self.tree.insert(
                    parent,
                    "end",
                    text="☐ " + p.name,
                    values=(rel,),
                    tags=("file",),
                )

    def _toggle_check(self, event):
        item = self.tree.identify_row(event.y)
        if not item or "file" not in self.tree.item(item, "tags"):
            return
        text = self.tree.item(item, "text")
        rel_path = self.tree.set(item, "fullpath")   # достаём значение из скрытого столбца
        if text.startswith("☐"):
            self.tree.item(item, text="☑ " + text[2:])
            self.checked.add(rel_path)
        else:
            self.tree.item(item, text="☐ " + text[2:])
            self.checked.discard(rel_path)

    def show_selected(self):
        if not self.checked:
            messagebox.showinfo("Выбор", "Ничего не выбрано.")
        else:
            messagebox.showinfo("Выбор", "\n".join(sorted(self.checked)))
            print("Выбрано:", *sorted(self.checked), sep="\n")

if __name__ == "__main__":
    if not ROOT_DIR.exists():
        raise SystemExit(f"Каталог {ROOT_DIR} не найден.")
    TreeSelector(ROOT_DIR).mainloop()
