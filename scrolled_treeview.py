#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from logrecord import LogRecord


class ScrolledTreeview(ttk.Treeview):
    def __init__(self, parent, **kwds):
        # self.selected_log: selected record converted to LogRecord
        self.selected_log: LogRecord = None
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
        self.bind('<<TreeviewSelect>>', self.on_select)
        self.set_columns()

    def on_select(self, event):
        try:
            iid = self.selection()[0]  # iid: 'I003'
        except IndexError:
            return
        log_id = self.item(iid, 'text')
        log = LogRecord.from_list([log_id, *self.item(iid, 'values')])
        self.selected_log = log

    @staticmethod
    def get_annotated_column_width(field):
        typ = LogRecord.__annotations__[field]
        if field == 'note':
            return 30
        try:
            return {int: 5, str: 10, datetime: 18}[typ]
        except KeyError:
            if field == 'volume':
                return 5
            else:
                raise

    def insert_log(self, log: LogRecord) -> str:
        # values = log.as_list()

        # 'values' are of different types, e.g., values[1] -
        # datetime.datetime, values[2] - None or int, values[3] - str,
        # etc.

        # iid = self.insert("", tk.END, text=values[0], values=values[1:])
        volume = '' if log.volume is None else log.volume
        iid = self.insert("", tk.END, text=log.id,
                          values=(log.stamp, volume, *log.as_list()[4:]))
        return iid              # e.g., 'I001'

    def sort_column(self, cid: str, reverse: bool = False):
        """cid: column index ('#0') or column identifier ('stamp')"""

        # [(val1, iid1), (val2, iid2), ...]
        values = [(self.set(iid, cid), iid) for iid in self.get_children('')]
        if cid in [f'label{i}' for i in range(1, 4)] + ['note']:
            # tup: (val, cid)
            key = lambda tup: tup[0]  # noqa
        elif cid == 'volume':
            key = lambda tup: int(tup[0])  # noqa
        elif cid == 'stamp':
            key = (lambda tup: datetime.strptime(  # noqa
                tup[0], '%Y-%m-%d %H:%M:%S'))
        else:
            key = None
        values = sorted(values, reverse=reverse, key=key)
        for index, (val, iid) in enumerate(values):
            self.move(iid, '', index)
        self.heading(cid, command=lambda: self.sort_column(cid, not reverse))

    def set_columns(self):
        flds = list(LogRecord.__fields__)
        self.configure(columns=flds[1:])
        self.heading("#0", text=flds[0])
        w = 7 * 8
        self.column("#0", minwidth=w, width=w)
        for f in flds[1:]:
            self.heading(f, text=f, command=(lambda cid=f: self.sort_column(
                cid, reverse=True)))
            w = self.get_annotated_column_width(f)
            w *= 8              # assuming 1 char is 8 pix
            self.column(f, minwidth=w, width=w)
