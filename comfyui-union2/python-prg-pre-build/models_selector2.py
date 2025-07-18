#!/usr/bin/env python3
r"""
Model-Task Builder GUI  (v 2025-07-18)
======================================

• Слева: дерево *.txt*-файлов; клик ☑/☐ — отмечает файл целиком.
• Справа: при выборе файла выводятся *блоки* (комментарии + URL + out/dir);
  у каждого блок-чек-бокс.
• **Выбрать все строки** — отмечает все блоки текущего файла.
• **Сформировать задание** — создаёт подпапку `_1_out` (рядом с моделями)
  и файлы: `civitay.txt` (все выбранные строки с URL *civitai.com*)
  и `hf.txt` (все выбранные строки с URL *huggingface.co*).

Формат блоков гибкий:
* URL начинает новый блок (пустая строка тоже завершает).
* `out=` и `dir=` могут идти в любом порядке или отсутствовать.
* Любые «# …» комментарии перед URL попадают в блок.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple

import tkinter as tk
from tkinter import ttk, messagebox, font

# ────────── НАСТРОЙКИ ────────────────────────────────────────────────
ROOT_DIR = Path(
    r"F:\_prg\python\Docker-ComfyUI\comfyui-union2\aria2\templates\models"
)  # ← смените при необходимости
BASE_SIZE = 14          # кегль шрифта
SCALING   = 1.3         # глобальный масштаб tkinter

OUT_DIR   = ROOT_DIR / "_1_out"   # куда писать civitay.txt / hf.txt
# ──────────────────────────────────────────────────────────────────────

URL_RE = re.compile(r"^\s*(https?://\S+)", re.I)
OUT_RE = re.compile(r"^\s*out\s*=\s*(\S+)", re.I)
DIR_RE = re.compile(r"^\s*dir\s*=\s*(\S.*)$", re.I)


# ═══════════ ПАРСЕР ФАЙЛА ════════════════════════════════════════════
@dataclass
class Block:
    display_lines: List[str]   # как будет показано в GUI
    url: str
    out: str | None
    dir: str | None

    def raw_lines(self) -> List[str]:
        """Строки для записи в итоговый txt-файл."""
        lines = [self.url]
        if self.out:
            lines.append(f"  out={self.out}")
        if self.dir:
            lines.append(f"  dir={self.dir}")
        lines.append("")                 # разделитель
        return lines


def parse_model_file(path: Path) -> List[Block]:
    """Разбивает файл на блоки (новый блок при встрече URL или пустой строке)."""
    blocks: List[Block] = []
    comments, url, out, dir_, disp = [], None, None, None, []

    def flush():
        nonlocal comments, url, out, dir_, disp
        if url:
            blocks.append(Block(["-" * 34, *disp, "-" * 34], url, out, dir_))
        comments, url, out, dir_, disp = [], None, None, None, []

    with path.open(encoding="utf8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")

            if not line.strip():                # пустая строка → конец блока
                flush()
                continue

            if line.lstrip().startswith("#"):
                comments.append(line)
                disp.append(line)
                continue

            m_url = URL_RE.match(line)
            if m_url:
                flush()                         # ⟵ главное: закрыть предыдущий блок
                url = m_url.group(1)
                disp.extend(comments)
                comments.clear()
                disp.append(url)
                continue

            m_out = OUT_RE.match(line)
            if m_out:
                out = m_out.group(1)
                disp.append(f"    out={out}")
                continue

            m_dir = DIR_RE.match(line)
            if m_dir:
                dir_ = m_dir.group(1)
                disp.append(f"    dir={dir_}")
                continue

            disp.append(line)                   # всё прочее просто добавляем

    flush()
    return blocks


# ═══════════ ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ═══════════════════════════════════
class ModelGUI(tk.Tk):
    def __init__(self, root_path: Path):
        super().__init__()
        self.title("Model Task Builder")
        self.geometry("1150x650")

        # DPI / шрифт
        self.tk.call("tk", "scaling", SCALING)
        font.nametofont("TkDefaultFont").configure(size=BASE_SIZE)
        big_f = font.Font(size=BASE_SIZE)

        # ─────────── ЛЕВАЯ ПАНЕЛЬ: дерево файлов ──────────────────────
        left = tk.Frame(self)
        left.pack(side="left", fill="y")

        self.tree = ttk.Treeview(left, columns=("rel",), show="tree")
        self.tree.column("rel", width=0, stretch=False)
        self.tree.tag_configure("file", font=big_f)
        ysb_tree = ttk.Scrollbar(left, orient="vertical",
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb_tree.set)
        self.tree.pack(side="left", fill="y")
        ysb_tree.pack(side="right", fill="y")

        # ─────────── ПРАВАЯ ПАНЕЛЬ: блоки ──────────────────────────────
        right = tk.Frame(self)
        right.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(right, borderwidth=0)
        ysb_blocks = ttk.Scrollbar(right, orient="vertical",
                                   command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=ysb_blocks.set)
        self.inner = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        ysb_blocks.pack(side="right", fill="y")
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # состояния
        self.file_checked: set[str] = set()                         # выбранные файлы
        self.block_vars: Dict[Tuple[str, int], tk.IntVar] = {}      # (rel, idx) → var

        self._fill_tree("", root_path)

        # события
        self.tree.bind("<Button-1>", self._toggle_file)
        self.tree.bind("<<TreeviewSelect>>", self._display_blocks)

        # ─────────── КНОПКИ ───────────────────────────────────────────
        style = ttk.Style()
        style.configure("Big.TButton", font=big_f)

        btns = tk.Frame(self)
        btns.pack(fill="x", pady=6)

        ttk.Button(btns, text="Выбрать все строки",
                   style="Big.TButton", command=self._select_all_blocks).pack(side="left", padx=6)

        ttk.Button(btns, text="Сформировать задание",
                   style="Big.TButton", command=self._make_task).pack(side="left", padx=6)

        ttk.Button(btns, text="Показать выбранные",
                   style="Big.TButton", command=self._show_selected).pack(side="left", padx=6)

    # ──────────── дерево ─────────────────────────────────────────────
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

    # ──────────── отображение блоков ─────────────────────────────────
    def _display_blocks(self, _ev=None):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        if "file" not in self.tree.item(iid, "tags"):
            return
        rel = self.tree.set(iid, "rel")
        path = ROOT_DIR / rel

        # очистка
        for w in self.inner.winfo_children():
            w.destroy()
        self.block_vars = {k: v for k, v in self.block_vars.items()
                           if k[0] != rel}

        for idx, blk in enumerate(parse_model_file(path)):
            var = tk.IntVar()
            self.block_vars[(rel, idx)] = var

            row = tk.Frame(self.inner, pady=4)
            tk.Checkbutton(row, variable=var).pack(side="left", anchor="n")

            tk.Label(row,
                     text="\n".join(blk.display_lines),
                     justify="left", anchor="w",
                     font=("Courier New", BASE_SIZE),
                     wraplength=700
                     ).pack(side="left", fill="x", expand=True)
            row.pack(anchor="w", fill="x")

    # ─────────── выбрать все блоки текущего файла ────────────────────
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

    # ─────────── показать выбранное ──────────────────────────────────
    def _show_selected(self):
        blk_sel = [(k, v) for k, v in self.block_vars.items() if v.get()]
        if not blk_sel and not self.file_checked:
            messagebox.showinfo("Выбор", "Ничего не выбрано.")
            return
        msg = ["Файлы целиком:"] + sorted(self.file_checked) + ["",
               "Блоки:"] + [f"{rel} [#{idx}]" for (rel, idx), _ in blk_sel]
        messagebox.showinfo("Выбрано", "\n".join(msg))

    # ─────────── сформировать задание ────────────────────────────────
    def _make_task(self):
        civ_lines: List[str] = []
        hf_lines: List[str]  = []

        # выбранные блоки
        for (rel, idx), var in self.block_vars.items():
            if not var.get():
                continue
            blk = parse_model_file(ROOT_DIR / rel)[idx]
            (hf_lines if blk.url.startswith("https://huggingface.co")
             else civ_lines).extend(blk.raw_lines())

        # целые файлы (если блоки не выбраны)
        for rel in self.file_checked:
            if any(k[0] == rel and v.get() for k, v in self.block_vars.items()):
                continue
            for blk in parse_model_file(ROOT_DIR / rel):
                (hf_lines if blk.url.startswith("https://huggingface.co")
                 else civ_lines).extend(blk.raw_lines())

        if not civ_lines and not hf_lines:
            messagebox.showinfo("Задание", "Нечего записывать – ничего не выбрано.")
            return

        # создаём директорию и записываем файлы
        OUT_DIR.mkdir(exist_ok=True)
        if civ_lines:
            (OUT_DIR / "civitay.txt").write_text("\n".join(civ_lines), encoding="utf8")
        if hf_lines:
            (OUT_DIR / "hf.txt").write_text("\n".join(hf_lines), encoding="utf8")

        messagebox.showinfo("Задание", f"Файлы созданы в:\n{OUT_DIR}")


# ══════════════════ MAIN ═════════════════════════════════════════════
if __name__ == "__main__":
    if not ROOT_DIR.exists():
        sys.exit(f"Каталог {ROOT_DIR} не найден.")
    ModelGUI(ROOT_DIR).mainloop()
