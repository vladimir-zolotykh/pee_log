#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from datetime import datetime
from typing import Optional, Union
import tkinter as tk
from tkinter import ttk         # noqa
from logrecord import LogRecord
from scrolled_treeview import ScrolledTreeview


class DetailView(ScrolledTreeview):
    def __init__(self, parent, **kwds):
        super(DetailView, self).__init__(parent, **kwds)
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
        # After .insert has done, everything becomes a string

        volume = '' if log.volume is None else log.volume
        iid = self.insert("", tk.END, text=log.id,
                          values=(log.stamp, volume, *log.as_list()[3:]))
        return iid              # e.g., 'I001'

    def sort_column(self, cid: str, reverse: bool = False):
        """cid: column index ('#0') or column identifier ('stamp')"""

        def none_or_int(volume: Optional[int]) -> Union[int, str]:
            try:
                return int(volume)  # '10'
            except ValueError:
                return 0        # ''

        # [(val1, iid1), (val2, iid2), ...]
        values = [(self.set(iid, cid), iid) for iid in self.get_children('')]
        if cid in [f'label{i}' for i in range(1, 4)] + ['note']:
            # tup: (val, cid)
            key = lambda tup: tup[0]  # noqa
        elif cid == 'volume':
            key = lambda tup: none_or_int(tup[0])  # noqa
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
