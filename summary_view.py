#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter
from dataclasses import dataclass, asdict, field
from typing import Optional, List
from datetime import datetime
import tkinter as tk
import database as db
from scrolled_treeview import ScrolledTreeview


@dataclass
class SummaryData:
    date: datetime
    count: int = 0              # logs a day
    volume: int = 0             # total volume
    tag: List[str] = field(default_factory=list)
    note: str = ''


CHAR_W = 8                      # assuming 1 char is 8 pix
FIELDS = list(SummaryData.__annotations__)
# FIELDS = {
#     'date': datetime,
#     'count': int, 'volume': int,
#     'tag': str, 'note': str
# }


def field_width(name: str) -> int:
    try:
        type_ = SummaryData.__annotations__[name]
    except KeyError:
        type_ = str
    try:
        return {datetime: 18, int: 5, str: 20}[type_]
    except KeyError:
        return 20


class SummaryView(ScrolledTreeview):
    def __init__(self, parent, **kwds):
        super(SummaryView, self).__init__(parent, **kwds)
        self.bind('<<TreeviewSelect>>', self.on_select)
        self.set_columns()
        self.selected_summary: SummaryData = None

    def set_columns(self):
        self.configure(columns=FIELDS[1:])
        self.heading("#0", text=FIELDS[0])
        w = field_width('date') * CHAR_W
        self.column("#0", minwidth=w, width=w)
        for f in FIELDS[1:]:
            self.heading(f, text=f, command=(lambda cid=f: self.sort_column(
                cid, reverse=True)))
            w = CHAR_W * field_width(f)
            self.column(f, minwidth=w, width=w)

    def insert_log(self, sd: SummaryData) -> str:
        # After .insert has done, everything becomes a string

        iid = self.insert("", tk.END, text=sd.date,
                          values=(sd.count, sd.volume, sd.tag, sd.note))
        return iid              # e.g., 'I001'

    def on_select(self, event):
        try:
            iid = self.selection()[0]  # iid: 'I003'
        except IndexError:
            return
        date = self.item(iid, 'text')
        self.selected_summary = SummaryData(date, *self.item(iid, 'values'))

    def sort_column(self, cid: str, reverse: bool = False):
        """cid: column index ('#0') or column identifier ('date')"""
        values = [(self.set(iid, cid), iid) for iid in self.get_children('')]
        # values: [(val1, iid1), (val2, iid2), ...]
        key = {
            'date': lambda v: datetime.strptime(itemgetter(0)(v),
                                                '%Y-%m-%d %H:%M:%S'),
            'count': lambda v: int(itemgetter(0)(v)),
            'volume': lambda v: int(itemgetter(0)(v)),
            'tag': lambda v: len(itemgetter(0)(v).split()),
            'note': None}[cid]
        values = sorted(values, reverse=reverse, key=key)
        for index, (val, iid) in enumerate(values):
            self.move(iid, '', index)
        self.heading(cid, command=lambda: self.sort_column(cid, not reverse))
