#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from logrecord import LogRecord

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

    @staticmethod
    def get_annotated_column_width(field):
        typ = LogRecord.__annotations__[field]
        if field == 'note':
            return 30
        try:
            return {int: 5, str: 10, datetime: 18}[typ]
        except KeyError:
            raise ValueError('Invalid LogRecord field width is requested')

    def insert_log(self, log: LogRecord) -> str:
        values = log.as_list()
        iid = self.insert("", tk.END, text=values[0], values=values[1:])
        return iid              # e.g., 'I001'

    def set_columns(self):
        try:
            flds = list(LogRecord.__fields__)
        except NameError:
            flds = ['id', 'stamp', 'label1', 'label2', 'label3', 'volume',
                    'note']
        self.configure(columns=flds[1:])
        self.heading("#0", text=flds[0])
        w = 5 * 8
        self.column("#0", minwidth=w, width=w)
        for f in flds[1:]:
            self.heading(f, text=f)
            w = self.get_annotated_column_width(f)
            w *= 8
            self.column(f, minwidth=w, width=w)
        log = LogRecord.from_list((1, '2024-03-19 20:49', 'pee', '', '', 123,
                                   'a note'))
        self.insert_log(log)
