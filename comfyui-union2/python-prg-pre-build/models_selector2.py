#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Model‑Task Builder GUI
======================

* Показывает дерево каталогов с *.txt‑листами моделей.
* Позволяет выбирать целые файлы или отдельные блоки и формировать
  `civitay.txt` / `hf.txt`.

ЧТО СДЕЛАНО
-----------
1. «_» заменяется на эмодзи Heavy Minus Sign (➖), так что подчёркивания
   видны даже когда Treeview скрывает mnemonic‑символы.
2. Добавлен обязательный горизонтальный отступ (`indent`) — ведущий символ
   не попадает под пиктограмму раскрытия.
3. Высота строки (`rowheight`) вычисляется динамически:
   ``rowheight = linespace + 10`` — ни эмодзи, ни «хвосты» букв не режутся.
4. Клик по каталогу больше не рушит GUI.
"""

from __future__ import annotations
import re, sys, tkinter as tk
from tkinter import ttk, font, messagebox
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

# ─── настроить пути под себя ──────────────────────────────────────
ROOT_DIR = Path(r"F:/_prg/python/Docker-ComfyUI/comfyui-union2/aria2/templates/models")
OUT_DIR  = ROOT_DIR / "_1_out"

# ─── константы ────────────────────────────────────────────────────
SUB_EMOJI = "➖"                       # чем визуально заменяем подчёркивание
TK_SCALING = 1.3                      # масштаб всей UI

URL_RE, OUT_RE, DIR_RE = (re.compile(p, re.I) for p in (
    r"^\s*(https?://\S+)",            # URL модели
    r"^\s*out\s*=\s*(\S+)",           # out= …
    r"^\s*dir\s*=\s*(\S.*)$"          # dir= …
))

# ─── util ─────────────────────────────────────────────────────────
def emojiize(name: str) -> str:
    """Отображаемо заменяет все '_' на тяжёлый минус."""
    return name.replace("_", SUB_EMOJI)

# ─── dataclass блока ─────────────────────────────────────────────
@dataclass
class Block:
    comments: List[str]
    url: str
    out: str | None
    dir: str | None

    def display(self) -> str:
        lines = ["-" * 34, *self.comments, self.url]
        if self.out:
            lines.append(f"    out={self.out}")
        if self.dir:
            lines.append(f"    dir={self.dir}")
        lines.append("-" * 34)
        return "\n".join(lines)

    def serialize(self) -> List[str]:
        lines = [*self.comments, self.url]
        if self.out:
            lines.append(f"    out={self.out}")
        if self.dir:
            lines.append(f"    dir={self.dir}")
        lines.append("")
        return lines

# ─── разбор .txt‑файла ───────────────────────────────────────────
def parse_model_file(path: Path) -> List[Block]:
    blocks, com = [], []
    url = out = dir_ = None
    def push():
        nonlocal com, url, out, dir_
        if url:
            blocks.append(Block(com.copy(), url, out, dir_))
        com.clear(); url = out = dir_ = None

    for line in path.read_text(encoding="utf8").splitlines():
        if not line.strip():
            push(); continue
        if line.lstrip().startswith("#"):
            com.append(line); continue
        if m := URL_RE.match(line):
            push(); url = m.group(1); continue
        if m := OUT_RE.match(line):
            out = m.group(1); continue
        if m := DIR_RE.match(line):
            dir_ = m.group(1); continue
        com.append(line)
    push(); return blocks

# ─── основное окно ───────────────────────────────────────────────
class GUI(tk.Tk):
    def __init__(self, root_path: Path):
        super().__init__()
        self.title("Model Task Builder"); self.geometry("1300x700")
        self.tk.call("tk", "scaling", TK_SCALING)

        # — оформление шрифтов/высоты
        base_fnt = font.nametofont("TkDefaultFont")
        base_fnt.configure(size=14)
        linespace = base_fnt.metrics("linespace")
        ROW_H = linespace + 10         # запас, чтобы ничего не обрезать

        style = ttk.Style(self)
        style.configure("Treeview", font=base_fnt, rowheight=ROW_H)
        style.configure("Treeview.Item", padding=(0, 4))
        style.configure("TButton", font=base_fnt)

        # — верхняя кнопочная панель
        bar = tk.Frame(self); bar.pack(side="top", fill="x", pady=6)
        ttk.Button(bar, text="Выбрать все строки", command=self._select_all)\
            .pack(side="left", padx=6)
        ttk.Button(bar, text="Сформировать задание", command=self._make_task)\
            .pack(side="left", padx=6)
        ttk.Button(bar, text="Показать выбранные", command=self._show)\
            .pack(side="left", padx=6)

        # — split‑панель
        paned = tk.PanedWindow(self, orient="horizontal"); paned.pack(fill="both", expand=True)

        # левая часть — дерево
        left = tk.Frame(paned); paned.add(left, stretch="always")
        left.grid_rowconfigure(0, weight=1); left.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(left, columns=("rel",), show="tree")
        self.tree.column("rel", width=0, stretch=False)
        try:                            # Tk >= 8.6.12
            self.tree["indent"] = 20
            self._pad = ""
        except tk.TclError:             # старый Tk
            self._pad = "\u00A0" * 3

        sb = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.grid(row=0, column=0, sticky="nsew"); sb.grid(row=0, column=1, sticky="ns")

        # правая часть — Canvas
        right = tk.Frame(paned); paned.add(right, stretch="always")
        right.grid_rowconfigure(0, weight=1); right.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(right, borderwidth=0)
        ycan = ttk.Scrollbar(right, orient="vertical", command=self.canvas.yview)
        xcan = ttk.Scrollbar(right, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=ycan.set, xscrollcommand=xcan.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        ycan.grid(row=0, column=1, sticky="ns"); xcan.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>",
                        lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Enter>",
            lambda _:
            self.canvas.bind_all(
                "<MouseWheel>",
                lambda e: self.canvas.yview_scroll(-e.delta // 120, "units"), add="+"))
        self.canvas.bind("<Leave>", lambda _: self.canvas.unbind_all("<MouseWheel>"))

        # состояния
        self.file_checked: set[str] = set()
        self.block_vars: Dict[Tuple[str, int], tk.IntVar] = {}

        self._fill("", root_path)
        self.tree.bind("<Button-1>", self._toggle)
        self.tree.bind("<<TreeviewSelect>>", self._display)

    # ── заполнить дерево ─────────────────────────────────────────
    def _fill(self, parent: str, path: Path):
        for p in sorted(path.iterdir()):
            if p.is_dir():
                label = self._pad + emojiize(p.name)
                node = self.tree.insert(parent, "end", text=label, open=False)
                self._fill(node, p)
            elif p.suffix.lower() == ".txt":
                rel = p.relative_to(ROOT_DIR).as_posix()
                self.tree.insert(parent, "end",
                                 text="☐ " + emojiize(p.name),
                                 values=(rel,), tags=("file",))

    # ── чекбоксы в дереве ───────────────────────────────────────
    def _toggle(self, e):
        iid = self.tree.identify_row(e.y)
        if not iid or "file" not in self.tree.item(iid, "tags"): return
        rel = self.tree.set(iid, "rel"); text = self.tree.item(iid, "text")
        if text.startswith("☐"):
            self.tree.item(iid, text="☑ " + text[2:]); self.file_checked.add(rel)
        else:
            self.tree.item(iid, text="☐ " + text[2:]); self.file_checked.discard(rel)

    # ── показать содержимое выбранного файла ─────────────────────
    def _display(self, _=None):
        sel = self.tree.selection()
        if not sel: return
        iid = sel[0]
        if "file" not in self.tree.item(iid, "tags"): return
        rel = self.tree.set(iid, "rel"); path = ROOT_DIR / rel

        for w in self.inner.winfo_children(): w.destroy()
        self.block_vars = {k: v for k, v in self.block_vars.items() if k[0] != rel}

        for idx, blk in enumerate(parse_model_file(path)):
            var = tk.IntVar(); self.block_vars[(rel, idx)] = var
            row = tk.Frame(self.inner, pady=4)
            tk.Checkbutton(row, variable=var).pack(side="left", anchor="n")
            tk.Label(row, text=blk.display(), justify="left",
                     font=("Courier New", 12), anchor="w")\
                .pack(side="left", fill="x", expand=True)
            row.pack(anchor="w", fill="x")

    # ── выделить все строки файла ────────────────────────────────
    def _select_all(self):
        sel = self.tree.selection()
        if not sel: return
        rel = self.tree.set(sel[0], "rel"); changed = False
        for (r, _), v in self.block_vars.items():
            if r == rel and not v.get(): v.set(1); changed = True
        if not changed:
            messagebox.showinfo("Инфо", "Все строки уже выбраны.")

    # ── показать, что выбрано ─────────────────────────────────────
    def _show(self):
        blocks = [(k, v) for k, v in self.block_vars.items() if v.get()]
        if not blocks and not self.file_checked:
            messagebox.showinfo("Выбор", "Ничего не выбрано."); return
        msg = ["Файлы целиком:", *sorted(self.file_checked), "",
               "Блоки:", *[f"{rel} [#{idx}]" for (rel, idx), _ in blocks]]
        messagebox.showinfo("Выбрано", "\n".join(msg))

    # ── сформировать civitay.txt / hf.txt ─────────────────────────
    def _make_task(self):
        civ: List[str] = []; hf: List[str] = []

        for (rel, idx), v in self.block_vars.items():
            if v.get():
                blk = parse_model_file(ROOT_DIR / rel)[idx]
                (hf if blk.url.startswith("https://huggingface.co") else civ)\
                    .extend(blk.serialize())

        for rel in self.file_checked:
            if any(k[0] == rel and v.get() for k, v in self.block_vars.items()):
                continue
            for blk in parse_model_file(ROOT_DIR / rel):
                (hf if blk.url.startswith("https://huggingface.co") else civ)\
                    .extend(blk.serialize())

        if not civ and not hf:
            messagebox.showinfo("Задание", "Нечего записывать — ничего не выбрано.")
            return

        OUT_DIR.mkdir(exist_ok=True)
        if civ: (OUT_DIR / "civitay.txt").write_text("\n".join(civ), encoding="utf8")
        if hf:  (OUT_DIR / "hf.txt").write_text("\n".join(hf),  encoding="utf8")
        messagebox.showinfo("Задание", f"Файлы созданы в:\n{OUT_DIR}")

# ─── запуск программы ────────────────────────────────────────────
if __name__ == "__main__":
    if not ROOT_DIR.exists():
        sys.exit(f"{ROOT_DIR} not found.")
    GUI(ROOT_DIR).mainloop()
