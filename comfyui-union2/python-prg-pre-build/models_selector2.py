#!/usr/bin/env python3
r"""
Model‑Task Builder GUI  – колесо мыши работает
=============================================

• Верхняя панель с кнопками (выбрать все, сформировать задание, показать выбранные).
• Слева — дерево *.txt*, справа — блоки (комментарии + URL + out/dir).
• Правую область можно прокручивать как вертикально, так и горизонтально;
  **колесо мыши теперь крутит вертикально**, когда курсор над областью.

Файлы‑задания (_1_out/civitay.txt, _1_out/hf.txt) формируются так же,
как и в предыдущих версиях.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple

import tkinter as tk
from tkinter import ttk, messagebox, font

# ────────── ПУТИ / НАСТРОЙКИ ─────────────────────────────────────────
ROOT_DIR = Path(
    r"F:\_prg\python\Docker-ComfyUI\comfyui-union2\aria2\templates\models"
)
OUT_DIR  = ROOT_DIR / "_1_out"

BASE_SIZE = 14
SCALING   = 1.3

URL_RE = re.compile(r"^\s*(https?://\S+)", re.I)
OUT_RE = re.compile(r"^\s*out\s*=\s*(\S+)", re.I)
DIR_RE = re.compile(r"^\s*dir\s*=\s*(\S.*)$", re.I)


# ═══════════ ПАРСЕР ══════════════════════════════════════════════════
@dataclass
class Block:
    comments: List[str]
    url: str
    out: str | None
    dir: str | None

    def display_lines(self) -> List[str]:
        lines = ["-" * 34, *self.comments, self.url]
        if self.out:
            lines.append(f"    out={self.out}")
        if self.dir:
            lines.append(f"    dir={self.dir}")
        lines.append("-" * 34)
        return lines

    def raw_lines(self) -> List[str]:
        lines = [*self.comments, self.url]
        if self.out:
            lines.append(f"    out={self.out}")
        if self.dir:
            lines.append(f"    dir={self.dir}")
        lines.append("")                        # пустая строка‑разделитель
        return lines


def parse_model_file(path: Path) -> List[Block]:
    """Разбивает текст на блоки (комментарии + URL + опции)."""
    blocks: List[Block] = []

    pending: List[str] = []        # комментарии / строки до следующего URL
    cur_comments: List[str] = []
    cur_url = cur_out = cur_dir = None

    def push_block():
        nonlocal cur_comments, cur_url, cur_out, cur_dir
        if cur_url:
            blocks.append(Block(cur_comments.copy(), cur_url, cur_out, cur_dir))
        cur_comments, cur_url, cur_out, cur_dir = [], None, None, None

    with path.open(encoding="utf8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")

            if not line.strip():            # пустая строка
                push_block()
                pending = []
                continue

            if line.lstrip().startswith("#"):
                pending.append(line)
                continue

            m = URL_RE.match(line)
            if m:
                push_block()
                cur_comments = pending
                pending = []
                cur_url = m.group(1)
                cur_out = cur_dir = None
                continue

            m = OUT_RE.match(line)
            if m:
                if cur_url is None:
                    pending.append(line)    # out= до URL → считать комментарием
                else:
                    cur_out = m.group(1)
                continue

            m = DIR_RE.match(line)
            if m:
                if cur_url is None:
                    pending.append(line)
                else:
                    cur_dir = m.group(1)
                continue

            pending.append(line)            # неизвестная строка ≙ комментарий

    push_block()
    return blocks


# ═══════════ GUI ════════════════════════════════════════════════════
class ModelGUI(tk.Tk):
    def __init__(self, root_path: Path):
        super().__init__()
        self.title("Model Task Builder")
        self.geometry("1300x700")

        # DPI, базовый шрифт
        self.tk.call("tk", "scaling", SCALING)
        font.nametofont("TkDefaultFont").configure(size=BASE_SIZE)
        big_f = font.Font(size=BASE_SIZE)

        # ─── Верхняя панель кнопок ───────────────────────────────────
        bar = tk.Frame(self)
        bar.pack(side="top", fill="x", pady=6)

        ttk.Style().configure("Big.TButton", font=big_f)
        ttk.Button(bar, text="Выбрать все строки",
                   style="Big.TButton", command=self._select_all_blocks).pack(side="left", padx=6)
        ttk.Button(bar, text="Сформировать задание",
                   style="Big.TButton", command=self._make_task).pack(side="left", padx=6)
        ttk.Button(bar, text="Показать выбранные",
                   style="Big.TButton", command=self._show_selected).pack(side="left", padx=6)

        # ─── Рабочая область (grid) ──────────────────────────────────
        work = tk.Frame(self)
        work.pack(side="top", fill="both", expand=True)

        # 1) Левое дерево
        tree_frame = tk.Frame(work)
        tree_frame.grid(row=0, column=0, sticky="ns")

        self.tree = ttk.Treeview(tree_frame, columns=("rel",), show="tree")
        self.tree.column("rel", width=0, stretch=False)
        self.tree.tag_configure("file", font=big_f)
        ysb_tree = ttk.Scrollbar(tree_frame, orient="vertical",
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb_tree.set)
        self.tree.pack(side="left", fill="y")
        ysb_tree.pack(side="right", fill="y")

        # 2) Правая панель с canvas
        right = tk.Frame(work)
        right.grid(row=0, column=1, sticky="nsew")
        work.grid_rowconfigure(0, weight=1)
        work.grid_columnconfigure(1, weight=1)

        self.canvas = tk.Canvas(right, borderwidth=0)
        ysb = ttk.Scrollbar(right, orient="vertical", command=self.canvas.yview)
        xsb = ttk.Scrollbar(right, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        # Расположение
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, columnspan=2, sticky="ew")

        # внутренний контейнер
        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # обновление scroll‑region
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # ── прокрутка колесом мыши ───────────────────────────────────
        def _on_mousewheel(event):
            # Windows / Mac: event.delta, Linux: bind Button-4/5
            delta = event.delta
            if delta == 0:   # Linux case handled separately
                return
            self.canvas.yview_scroll(int(-delta / 120), "units")

        # Windows / macOS
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        # Linux support (button‑4/5)
        self.canvas.bind("<Enter>", lambda e: (
            self.canvas.bind_all("<Button-4>", lambda ev: self.canvas.yview_scroll(-1, "units")),
            self.canvas.bind_all("<Button-5>", lambda ev: self.canvas.yview_scroll(1, "units")),
        ))
        self.canvas.bind("<Leave>", lambda e: (
            self.canvas.unbind_all("<Button-4>"),
            self.canvas.unbind_all("<Button-5>"),
        ))

        # ─── состояния ───────────────────────────────────────────────
        self.file_checked: set[str] = set()
        self.block_vars: Dict[Tuple[str, int], tk.IntVar] = {}

        self._fill_tree("", root_path)
        self.tree.bind("<Button-1>", self._toggle_file)
        self.tree.bind("<<TreeviewSelect>>", self._show_blocks)

    # ── дерево ───────────────────────────────────────────────────────
    def _fill_tree(self, parent: str, path: Path):
        for p in sorted(path.iterdir()):
            if p.is_dir():
                node = self.tree.insert(parent, "end", text=p.name, open=False)
                self._fill_tree(node, p)
            elif p.suffix.lower() == ".txt":
                rel = p.relative_to(ROOT_DIR).as_posix()
                self.tree.insert(parent, "end", text="☐ " + p.name,
                                 values=(rel,), tags=("file",))

    def _toggle_file(self, ev):
        iid = self.tree.identify_row(ev.y)
        if not iid or "file" not in self.tree.item(iid, "tags"):
            return
        text = self.tree.item(iid, "text")
        rel  = self.tree.set(iid, "rel")
        if text.startswith("☐"):
            self.tree.item(iid, text="☑ " + text[2:])
            self.file_checked.add(rel)
        else:
            self.tree.item(iid, text="☐ " + text[2:])
            self.file_checked.discard(rel)

    # ── показ блоков ────────────────────────────────────────────────
    def _show_blocks(self, _=None):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        if "file" not in self.tree.item(iid, "tags"):
            return
        rel = self.tree.set(iid, "rel")
        path = ROOT_DIR / rel

        for w in self.inner.winfo_children():
            w.destroy()
        self.block_vars = {k: v for k, v in self.block_vars.items() if k[0] != rel}

        for idx, blk in enumerate(parse_model_file(path)):
            var = tk.IntVar()
            self.block_vars[(rel, idx)] = var

            row = tk.Frame(self.inner, pady=4)
            tk.Checkbutton(row, variable=var).pack(side="left", anchor="n")

            tk.Label(row, text="\n".join(blk.display_lines()),
                     justify="left", anchor="w",
                     font=("Courier New", BASE_SIZE),
                     wraplength=0).pack(side="left", fill="x", expand=True)
            row.pack(anchor="w", fill="x")

    # ── выбор всех в файле ───────────────────────────────────────────
    def _select_all_blocks(self):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        if "file" not in self.tree.item(iid, "tags"):
            return
        rel = self.tree.set(iid, "rel")

        changed = False
        for (r, _), var in self.block_vars.items():
            if r == rel and not var.get():
                var.set(1)
                changed = True
        if not changed:
            messagebox.showinfo("Инфо", "Все строки уже выбраны.")

    # ── показать выбранное ───────────────────────────────────────────
    def _show_selected(self):
        blocks = [(k, v) for k, v in self.block_vars.items() if v.get()]
        if not blocks and not self.file_checked:
            messagebox.showinfo("Выбор", "Ничего не выбрано.")
            return
        msg = ["Файлы целиком:"] + sorted(self.file_checked) + ["",
               "Блоки:"] + [f"{rel} [#{idx}]" for (rel, idx), _ in blocks]
        messagebox.showinfo("Выбрано", "\n".join(msg))

    # ── формирование civitay.txt / hf.txt ───────────────────────────
    def _make_task(self):
        civ_lines, hf_lines = [], []

        for (rel, idx), var in self.block_vars.items():
            if not var.get():
                continue
            blk = parse_model_file(ROOT_DIR / rel)[idx]
            (hf_lines if blk.url.startswith("https://huggingface.co") else civ_lines).extend(blk.raw_lines())

        for rel in self.file_checked:
            if any(k[0] == rel and v.get() for k, v in self.block_vars.items()):
                continue
            for blk in parse_model_file(ROOT_DIR / rel):
                (hf_lines if blk.url.startswith("https://huggingface.co") else civ_lines).extend(blk.raw_lines())

        if not civ_lines and not hf_lines:
            messagebox.showinfo("Задание", "Нечего записывать — ничего не выбрано.")
            return

        OUT_DIR.mkdir(exist_ok=True)
        if civ_lines:
            (OUT_DIR / "civitay.txt").write_text("\n".join(civ_lines), encoding="utf8")
        if hf_lines:
            (OUT_DIR / "hf.txt").write_text("\n".join(hf_lines), encoding="utf8")

        messagebox.showinfo("Задание", f"Файлы созданы в:\n{OUT_DIR}")


# ═══════════ MAIN ════════════════════════════════════════════════════
if __name__ == "__main__":
    if not ROOT_DIR.exists():
        sys.exit(f"Каталог {ROOT_DIR} не найден.")
    ModelGUI(ROOT_DIR).mainloop()
