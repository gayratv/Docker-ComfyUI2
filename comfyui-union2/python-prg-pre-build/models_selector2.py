#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model‑Task Builder GUI (2025‑07‑18)
===================================

* Левый блок — дерево каталогов с *.txt*‑файлами.
* Правый блок — содержимое выбранного файла, разбитое на «блоки»
  (комментарии + URL + out/dir) — у каждого чек‑бокс.
* Горизонтальная **сплит‑панель** (`tk.PanedWindow`) — можно
  тянуть разделитель и менять ширину обеих частей.
* Колёсико мыши прокручивает правую область (Win / macOS / Linux).
* Кнопки сверху:
  ▸ **Выбрать все строки** — отмечает все блоки текущего файла.
  ▸ **Сформировать задание** — создаёт `_1_out/civitay.txt`
    и `_1_out/hf.txt` с отмеченными строками.
  ▸ **Показать выбранные** — диалог со списком отмеченного.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import tkinter as tk
from tkinter import ttk, font, messagebox

# ───── пути и базовые настройки ─────────────────────────────────────
ROOT_DIR = Path(
    r"F:\_prg\python\Docker-ComfyUI\comfyui-union2\aria2\templates\models"
)
OUT_DIR = ROOT_DIR / "_1_out"

BASE_FONT_SIZE = 14
SCALING = 1.3  # DPI‑масштаб для high‑DPI экранов

URL_RE = re.compile(r"^\s*(https?://\S+)", re.I)
OUT_RE = re.compile(r"^\s*out\s*=\s*(\S+)", re.I)
DIR_RE = re.compile(r"^\s*dir\s*=\s*(\S.*)$", re.I)

# ───── модель блока ────────────────────────────────────────────────
@dataclass
class Block:
    comments: List[str]
    url: str
    out: str | None
    dir: str | None

    # строки для правой панели
    def display(self) -> List[str]:
        lines = ["-" * 34, *self.comments, self.url]
        if self.out:
            lines.append(f"    out={self.out}")
        if self.dir:
            lines.append(f"    dir={self.dir}")
        lines.append("-" * 34)
        return lines

    # строки для записи в txt‑задание
    def serialize(self) -> List[str]:
        lines = [*self.comments, self.url]
        if self.out:
            lines.append(f"    out={self.out}")
        if self.dir:
            lines.append(f"    dir={self.dir}")
        lines.append("")  # пустая строка‑разделитель
        return lines


def parse_model_file(path: Path) -> List[Block]:
    """Разбирает файл на блоки комментариев + URL + опций."""
    blocks: List[Block] = []
    pending_comments: List[str] = []
    comments: List[str] = []
    url = out = dir_ = None

    def flush():
        nonlocal comments, url, out, dir_
        if url:
            blocks.append(Block(comments.copy(), url, out, dir_))
        comments.clear()
        url = out = dir_ = None

    with path.open(encoding="utf8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")

            if not line.strip():                        # пустая строка
                flush()
                pending_comments = []
                continue

            if line.lstrip().startswith("#"):           # комментарий
                pending_comments.append(line)
                continue

            m = URL_RE.match(line)
            if m:
                flush()
                comments = pending_comments
                pending_comments = []
                url = m.group(1)
                continue

            m = OUT_RE.match(line)
            if m:
                if url is None:
                    pending_comments.append(line)
                else:
                    out = m.group(1)
                continue

            m = DIR_RE.match(line)
            if m:
                if url is None:
                    pending_comments.append(line)
                else:
                    dir_ = m.group(1)
                continue

            pending_comments.append(line)               # всё остальное — комментарий

    flush()
    return blocks


# ───── GUI ───────────────────────────────────────────────────────────
class ModelGUI(tk.Tk):
    def __init__(self, root_path: Path):
        super().__init__()
        self.title("Model Task Builder")
        self.geometry("1300x700")

        self.tk.call("tk", "scaling", SCALING)
        font.nametofont("TkDefaultFont").configure(size=BASE_FONT_SIZE)
        self.fixed_font = font.Font(size=BASE_FONT_SIZE)

        # верхняя панель кнопок
        self._build_topbar()

        # раздвижной PanedWindow
        self._build_panes(root_path)

        # состояния
        self.file_checked: set[str] = set()
        self.block_vars: Dict[Tuple[str, int], tk.IntVar] = {}

    # ────────── UI helpers ──────────────────────────────────────────
    def _build_topbar(self):
        bar = tk.Frame(self)
        bar.pack(side="top", fill="x", pady=6)

        ttk.Style().configure("Big.TButton", font=self.fixed_font)

        ttk.Button(bar, text="Выбрать все строки",
                   style="Big.TButton", command=self.select_all_blocks
                   ).pack(side="left", padx=6)

        ttk.Button(bar, text="Сформировать задание",
                   style="Big.TButton", command=self.make_task
                   ).pack(side="left", padx=6)

        ttk.Button(bar, text="Показать выбранные",
                   style="Big.TButton", command=self.show_selected
                   ).pack(side="left", padx=6)

    def _build_panes(self, root_path: Path):
        paned = tk.PanedWindow(self, orient="horizontal")
        paned.pack(side="top", fill="both", expand=True)

        # левая створка: дерево
        left = tk.Frame(paned)
        try:
            paned.add(left, minsize=120, stretch="always")  # Tk 8.6+; если жалуется – убрать minsize
        except tk.TclError:
            paned.add(left, stretch="always")

        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(left, columns=("rel",), show="tree")
        self.tree.column("rel", width=0, stretch=False)
        self.tree.tag_configure("file", font=self.fixed_font)

        y_tree = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y_tree.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_tree.grid(row=0, column=1, sticky="ns")

        self._populate_tree("", root_path)
        self.tree.bind("<Button-1>", self.toggle_file)
        self.tree.bind("<<TreeviewSelect>>", self.display_blocks)

        # правая створка: canvas
        right = tk.Frame(paned)
        paned.add(right, stretch="always")

        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(right, borderwidth=0)
        y_canvas = ttk.Scrollbar(right, orient="vertical", command=self.canvas.yview)
        x_canvas = ttk.Scrollbar(right, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=y_canvas.set, xscrollcommand=x_canvas.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        y_canvas.grid(row=0, column=1, sticky="ns")
        x_canvas.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # прокрутка колесом мыши
        self._bind_mousewheel()

    def _bind_mousewheel(self):
        # Windows / macOS
        def on_wheel(event): self.canvas.yview_scroll(int(-event.delta / 120), "units")
        self.canvas.bind("<Enter>", lambda _:
                         self.canvas.bind_all("<MouseWheel>", on_wheel, add="+"))
        self.canvas.bind("<Leave>", lambda _:
                         self.canvas.unbind_all("<MouseWheel>"))

        # Linux Button‑4/5
        self.canvas.bind("<Enter>", lambda _:
                         (self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"), add="+"),
                          self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"), add="+")))
        self.canvas.bind("<Leave>", lambda _:
                         (self.canvas.unbind_all("<Button-4>"),
                          self.canvas.unbind_all("<Button-5>")))

    # ────────── дерево ──────────────────────────────────────────────
    def _populate_tree(self, parent: str, path: Path):
        for p in sorted(path.iterdir()):
            if p.is_dir():
                node = self.tree.insert(parent, "end", text=p.name, open=False)
                self._populate_tree(node, p)
            elif p.suffix.lower() == ".txt":
                rel = p.relative_to(ROOT_DIR).as_posix()
                self.tree.insert(parent, "end", text="☐ " + p.name,
                                 values=(rel,), tags=("file",))

    def toggle_file(self, event):
        iid = self.tree.identify_row(event.y)
        if not iid or "file" not in self.tree.item(iid, "tags"):
            return
        rel = self.tree.set(iid, "rel")
        current = self.tree.item(iid, "text")
        if current.startswith("☐"):
            self.tree.item(iid, text="☑ " + current[2:])
            self.file_checked.add(rel)
        else:
            self.tree.item(iid, text="☐ " + current[2:])
            self.file_checked.discard(rel)

    # ────────── отображение блоков ──────────────────────────────────
    def display_blocks(self, _=None):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        if "file" not in self.tree.item(iid, "tags"):
            return
        rel = self.tree.set(iid, "rel")
        file_path = ROOT_DIR / rel

        # очистить прежний вывод
        for w in self.inner.winfo_children():
            w.destroy()
        self.block_vars = {k: v for k, v in self.block_vars.items() if k[0] != rel}

        for idx, blk in enumerate(parse_model_file(file_path)):
            var = tk.IntVar()
            self.block_vars[(rel, idx)] = var

            row = tk.Frame(self.inner, pady=4)
            tk.Checkbutton(row, variable=var).pack(side="left", anchor="n")
            tk.Label(row,
                     text="\n".join(blk.display()),
                     justify="left",
                     anchor="w",
                     font=("Courier New", BASE_FONT_SIZE),
                     wraplength=0  # не переносить длинные URL
                     ).pack(side="left", fill="x", expand=True)
            row.pack(anchor="w", fill="x")

    # ────────── команды кнопок ──────────────────────────────────────
    def select_all_blocks(self):
        sel = self.tree.selection()
        if not sel:
            return
        rel = self.tree.set(sel[0], "rel")
        updated = False
        for (r, _), var in self.block_vars.items():
            if r == rel and not var.get():
                var.set(1)
                updated = True
        if not updated:
            messagebox.showinfo("Инфо", "Все строки уже выбраны.")

    def show_selected(self):
        chosen_blocks = [(k, v) for k, v in self.block_vars.items() if v.get()]
        if not chosen_blocks and not self.file_checked:
            messagebox.showinfo("Выбор", "Ничего не выбрано.")
            return
        parts = ["Файлы целиком:", *sorted(self.file_checked), "",
                 "Блоки:"]
        parts.extend(f"{rel}  [#{idx}]" for (rel, idx), _ in chosen_blocks)
        messagebox.showinfo("Выбрано", "\n".join(parts))

    def make_task(self):
        civ_lines: List[str] = []
        hf_lines: List[str] = []

        # отмеченные блоки
        for (rel, idx), var in self.block_vars.items():
            if var.get():
                blk = parse_model_file(ROOT_DIR / rel)[idx]
                (hf_lines if blk.url.startswith("https://huggingface.co") else civ_lines
                 ).extend(blk.serialize())

        # целиком выбранные файлы
        for rel in self.file_checked:
            if any(k[0] == rel and v.get() for k, v in self.block_vars.items()):
                continue  # если в файле уже выбраны блоки, файл целиком не нужен
            for blk in parse_model_file(ROOT_DIR / rel):
                (hf_lines if blk.url.startswith("https://huggingface.co") else civ_lines
                 ).extend(blk.serialize())

        if not civ_lines and not hf_lines:
            messagebox.showinfo("Задание", "Нечего записывать — ничего не выбрано.")
            return

        OUT_DIR.mkdir(exist_ok=True)
        if civ_lines:
            (OUT_DIR / "civitay.txt").write_text("\n".join(civ_lines), encoding="utf8")
        if hf_lines:
            (OUT_DIR / "hf.txt").write_text("\n".join(hf_lines), encoding="utf8")

        messagebox.showinfo("Задание", f"Файлы созданы в:\n{OUT_DIR}")

# ───── main ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not ROOT_DIR.exists():
        sys.exit(f"Каталог {ROOT_DIR} не найден.")
    ModelGUI(ROOT_DIR).mainloop()
