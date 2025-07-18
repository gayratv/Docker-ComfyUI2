#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model‑Task Builder GUI — увеличенный вертикальный интервал
==========================================================

Изменение — строки в левом дереве стали выше (`rowheight=26` + верх/низ padding 4 px),
поэтому под каталогами вроде “upscalers” заметно больше места.
Остальной функционал (сплит‑панель, колёсико, формирование civitay/hf.txt)
остался прежним.
"""

from __future__ import annotations
import re, sys, tkinter as tk
from tkinter import ttk, font, messagebox
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT_DIR = Path(r"F:\_prg\python\Docker-ComfyUI\comfyui-union2\aria2\templates\models")
OUT_DIR  = ROOT_DIR / "_1_out"
BASE_SIZE, SCALING = 14, 1.3
URL_RE, OUT_RE, DIR_RE = (re.compile(p, re.I) for p in (
    r"^\s*(https?://\S+)", r"^\s*out\s*=\s*(\S+)", r"^\s*dir\s*=\s*(\S.*)$"))

# ─── модель блока ───────────────────────────────────────────────────
@dataclass
class Block:
    comments: List[str]; url: str; out: str | None; dir: str | None
    def display(self)->List[str]:
        lines=["-"*34,*self.comments,self.url]
        if self.out: lines.append(f"    out={self.out}")
        if self.dir: lines.append(f"    dir={self.dir}")
        lines.append("-"*34); return lines
    def serialize(self)->List[str]:
        lines=[*self.comments,self.url]
        if self.out: lines.append(f"    out={self.out}")
        if self.dir: lines.append(f"    dir={self.dir}")
        lines.append(""); return lines

def parse_model_file(path: Path) -> List[Block]:
    blocks,pending,com,url,out,dir_ = [],[],[],None,None,None
    def push():
        nonlocal com,url,out,dir_
        if url: blocks.append(Block(com.copy(),url,out,dir_))
        com.clear(); url=out=dir_=None
    for line in path.read_text(encoding="utf8").splitlines():
        if not line.strip(): push(); pending=[]; continue
        if line.lstrip().startswith("#"): pending.append(line); continue
        if m:=URL_RE.match(line): push(); com=pending; pending=[]; url=m.group(1); continue
        if m:=OUT_RE.match(line):
            if url is None: pending.append(line)
            else: out=m.group(1); continue
        if m:=DIR_RE.match(line):
            if url is None: pending.append(line)
            else: dir_=m.group(1); continue
        pending.append(line)
    push(); return blocks

# ─── основное окно ──────────────────────────────────────────────────
class GUI(tk.Tk):
    def __init__(self, root: Path):
        super().__init__()
        self.title("Model Task Builder"); self.geometry("1300x700")
        self.tk.call("tk","scaling",SCALING)
        font.nametofont("TkDefaultFont").configure(size=BASE_SIZE)
        bigf=font.Font(size=BASE_SIZE)

        # ── стиль Treeview: увеличиваем высоту строки ───────────────
        style=ttk.Style(self)
        style.configure("Treeview", font=bigf, rowheight=26)            # высота строки
        style.configure("Treeview.Item", padding=(0,4))                 # верх/низ padding

        # ── верхние кнопки ──────────────────────────────────────────
        bar=tk.Frame(self); bar.pack(side="top",fill="x",pady=6)
        ttk.Style().configure("B.TButton",font=bigf)
        ttk.Button(bar,text="Выбрать все строки",style="B.TButton",
                   command=self._select_all).pack(side="left",padx=6)
        ttk.Button(bar,text="Сформировать задание",style="B.TButton",
                   command=self._make_task).pack(side="left",padx=6)
        ttk.Button(bar,text="Показать выбранные",style="B.TButton",
                   command=self._show).pack(side="left",padx=6)

        # ── панель splitter ─────────────────────────────────────────
        paned=tk.PanedWindow(self,orient="horizontal"); paned.pack(fill="both",expand=True)

        # левая створка
        left=tk.Frame(paned); paned.add(left,stretch="always")
        left.grid_rowconfigure(0,weight=1); left.grid_columnconfigure(0,weight=1)
        self.tree=ttk.Treeview(left,columns=("rel",),show="tree")
        self.tree.column("rel",width=0,stretch=False); self.tree.tag_configure("file",font=bigf)
        ytree=ttk.Scrollbar(left,orient="vertical",command=self.tree.yview)
        self.tree.configure(yscrollcommand=ytree.set)
        self.tree.grid(row=0,column=0,sticky="nsew"); ytree.grid(row=0,column=1,sticky="ns")

        # правая створка
        right=tk.Frame(paned); paned.add(right,stretch="always")
        right.grid_rowconfigure(0,weight=1); right.grid_columnconfigure(0,weight=1)
        self.canvas=tk.Canvas(right,borderwidth=0)
        ycan=ttk.Scrollbar(right,orient="vertical",command=self.canvas.yview)
        xcan=ttk.Scrollbar(right,orient="horizontal",command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=ycan.set,xscrollcommand=xcan.set)
        self.canvas.grid(row=0,column=0,sticky="nsew"); ycan.grid(row=0,column=1,sticky="ns"); xcan.grid(row=1,column=0,columnspan=2,sticky="ew")
        self.inner=tk.Frame(self.canvas); self.canvas.create_window((0,0),window=self.inner,anchor="nw")
        self.inner.bind("<Configure>",lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # колесо мыши
        self.canvas.bind("<Enter>",lambda _:
            self.canvas.bind_all("<MouseWheel>",lambda e:self.canvas.yview_scroll(-e.delta//120,"units"),add="+"))
        self.canvas.bind("<Leave>",lambda _:self.canvas.unbind_all("<MouseWheel>"))

        # состояния
        self.file_checked:set[str]=set(); self.block_vars:Dict[Tuple[str,int],tk.IntVar]={}
        self._fill("",root); self.tree.bind("<Button-1>",self._toggle)
        self.tree.bind("<<TreeviewSelect>>",self._display)

    # ── заполнение дерева ──────────────────────────────────────────
    def _fill(self,parent:str,path:Path):
        for p in sorted(path.iterdir()):
            if p.is_dir():
                n=self.tree.insert(parent,"end",text=p.name,open=False)
                self._fill(n,p)
            elif p.suffix.lower()==".txt":
                rel=p.relative_to(ROOT_DIR).as_posix()
                self.tree.insert(parent,"end",text="☐ "+p.name,values=(rel,),tags=("file",))

    def _toggle(self,e):
        iid=self.tree.identify_row(e.y)
        if not iid or "file" not in self.tree.item(iid,"tags"): return
        rel=self.tree.set(iid,"rel"); txt=self.tree.item(iid,"text")
        if txt.startswith("☐"):
            self.tree.item(iid,text="☑ "+txt[2:]); self.file_checked.add(rel)
        else:
            self.tree.item(iid,text="☐ "+txt[2:]); self.file_checked.discard(rel)

    # ── отображение блоков ─────────────────────────────────────────
    def _display(self,_=None):
        sel=self.tree.selection()
        if not sel: return
        rel=self.tree.set(sel[0],"rel"); path=ROOT_DIR/rel
        for w in self.inner.winfo_children(): w.destroy()
        self.block_vars={k:v for k,v in self.block_vars.items() if k[0]!=rel}
        for idx,blk in enumerate(parse_model_file(path)):
            var=tk.IntVar(); self.block_vars[(rel,idx)]=var
            row=tk.Frame(self.inner,pady=4)
            tk.Checkbutton(row,variable=var).pack(side="left",anchor="n")
            tk.Label(row,text="\n".join(blk.display()),justify="left",anchor="w",
                     font=("Courier New",BASE_SIZE),wraplength=0
                     ).pack(side="left",fill="x",expand=True)
            row.pack(anchor="w",fill="x")

    # ── кнопка «выбрать все» ───────────────────────────────────────
    def _select_all(self):
        sel=self.tree.selection()
        if not sel: return
        rel=self.tree.set(sel[0],"rel"); changed=False
        for (r,_),v in self.block_vars.items():
            if r==rel and not v.get(): v.set(1); changed=True
        if not changed: messagebox.showinfo("Инфо","Все строки уже выбраны.")

    def _show(self):
        blocks=[(k,v) for k,v in self.block_vars.items() if v.get()]
        if not blocks and not self.file_checked:
            messagebox.showinfo("Выбор","Ничего не выбрано."); return
        msg=["Файлы целиком:",*sorted(self.file_checked),"","Блоки:",
             *[f"{rel} [#{idx}]" for (rel,idx),_ in blocks]]
        messagebox.showinfo("Выбрано","\n".join(msg))

    # ── формирование civitay.txt / hf.txt ──────────────────────────
    def _make_task(self):
        civ,hf=[],[]
        for (rel,idx),v in self.block_vars.items():
            if v.get():
                blk=parse_model_file(ROOT_DIR/rel)[idx]
                (hf if blk.url.startswith("https://huggingface.co") else civ).extend(blk.serialize())
        for rel in self.file_checked:
            if any(k[0]==rel and v.get() for k,v in self.block_vars.items()): continue
            for blk in parse_model_file(ROOT_DIR/rel):
                (hf if blk.url.startswith("https://huggingface.co") else civ).extend(blk.serialize())
        if not civ and not hf:
            messagebox.showinfo("Задание","Нечего записывать — ничего не выбрано."); return
        OUT_DIR.mkdir(exist_ok=True)
        if civ: (OUT_DIR/"civitay.txt").write_text("\n".join(civ),encoding="utf8")
        if hf:  (OUT_DIR/"hf.txt").write_text("\n".join(hf),encoding="utf8")
        messagebox.showinfo("Задание",f"Файлы созданы в:\n{OUT_DIR}")

# ─── запуск ─────────────────────────────────────────────────────────
if __name__=="__main__":
    if not ROOT_DIR.exists(): sys.exit(f"{ROOT_DIR} не найден.")
    GUI(ROOT_DIR).mainloop()
