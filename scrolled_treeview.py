#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk


class ScrolledTreeview(ttk.Treeview):
    def __init__(self, parent, **kwds):
        box = tk.Frame(parent)
        box.grid(column=0, row=0, sticky=tk.NSEW)
        box.columnconfigure(0, weight=1)
        box.rowconfigure(0, weight=1)
        vbar = tk.Scrollbar(box, orient=tk.VERTICAL, command=self.yview)
        vbar.grid(column=1, row=0, sticky=tk.NS)
        hbar = tk.Scrollbar(box, orient=tk.HORIZONTAL, command=self.xview)
        hbar.grid(column=0, row=1, stick=tk.EW)
        kwds.update({'yscrollcommand': vbar.set, 'xscrollcommand': hbar.set})
        super(ScrolledTreeview, self).__init__(box, **kwds)
        self.grid(column=0, row=0, sticky=tk.NSEW)
        for m in ('grid', 'grid_configure', 'grid_forget'):
            setattr(self, m, getattr(box, m))
        self.set_columns()

    def set_columns(self):
        try:
            flds = list(LogRecord.__fields__)
        except NameError:
            flds = ['id', 'stamp', 'label1', 'label2', 'label3', 'volume',
                    'note']
        self.configure(columns=flds[1:])
        self.heading("#0", text=flds[0])
        for f in flds[1:]:
            self.heading(f, text=f)
        self.insert(
            "",
            tk.END,
            text="1",
            values=('2024-03-19 20:49', 'pee', None, None, 123, 'a note')
        )
