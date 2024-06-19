#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Optional, Callable, Any, Tuple, List
from operator import itemgetter
from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel
import tkinter as tk
from scrolled_treeview import ScrolledTreeview, ContextMenuMixin


# @dataclass
class SummaryData(BaseModel):
    date: datetime
    count: int = 0              # logs a day
    volume: int = 0             # total volume
    tag: List[str] = field(default_factory=list)
    note: List[str] = field(default_factory=list)


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


class S0:
    pass


class SummaryView(ScrolledTreeview, S0, ContextMenuMixin):
    def __init__(self, parent, **kwds):
        # Treeview has '.parent(iid) ' method
        self._parent = parent
        super(SummaryView, self).__init__(parent, **kwds)
        super(S0, self).__init__()  # ContextMenuMixin.__init__
        self.bind('<<TreeviewSelect>>', self.on_select)
        self.set_columns()
        self.selected_summary: Optional[SummaryData] = None

    def make_context_menu(self) -> tk.Menu:
        m = tk.Menu(self, tearoff=0)
        # m.add_command(label="SummaryView action", command=lambda: None)

        def make_closure(parent):
            def narrow_to_date():
                narrow_btn = parent.narrow_btn
                if self.selected_summary:
                    date = self.selected_summary.date
                    parent.set_val('stamp', date)
                return parent.narrow_to_date(narrow_btn)
            return narrow_to_date

        m.add_command(label='Narrow to date',
                      command=make_closure(self._parent))
        return m

    def set_columns(self):
        self.configure(columns=FIELDS[1:])
        self.heading("#0", text=FIELDS[0])
        w = field_width('date') * CHAR_W
        self.column("#0", minwidth=w, width=w)
        for f in FIELDS[1:]:

            def make_closure(cid: str = f) -> Callable[[], None]:
                def sort_column():
                    self.sort_column(cid, reverse=True)
                return sort_column

            self.heading(f, text=f, command=make_closure(cid=f))
            # self.heading(f, text=f, command=(lambda cid=f: self.sort_column(
            #     cid, reverse=True)))
            w = CHAR_W * field_width(f)
            self.column(f, minwidth=w, width=w)

    def insert_log(self, sd: SummaryData) -> str:
        # After .insert has done, everything becomes a string

        iid = self.insert("", tk.END, text=str(sd.date),
                          values=(sd.count, sd.volume, sd.tag, sd.note))
        return iid              # e.g., 'I001'

    def on_select(self, event):
        try:
            iid = self.selection()[0]  # iid: 'I003'
        except IndexError:
            return
        date: str = self.item(iid, 'text')
        # date = '2024-03-02 23:36:00'
        # self.selected_summary = SummaryData(
        #     datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),
        #     *self.item(iid, 'values'))
        values = self.item(iid, 'values')
        self.selected_summary = SummaryData(
            date=datetime.strptime(date, '%Y-%m-%d %H:%M:%S'),
            count=int(values[0]), volume=int(values[1]),
            tag=values[2].split(), note=values[3].split('\n'))

    def sort_column(self, cid: str, reverse: bool = False) -> None:
        """cid: column index ('#0') or column identifier ('date')"""
        values = [(self.set(iid, cid), iid) for iid in self.get_children('')]
        # values: [(val1, iid1), (val2, iid2), ...]
        key = {
            'date': lambda v: datetime.strptime(itemgetter(0)(v),
                                                '%Y-%m-%d %H:%M:%S'),
            'count': lambda v: int(itemgetter(0)(v)),
            'volume': lambda v: int(itemgetter(0)(v)),
            'tag': lambda v: len(itemgetter(0)(v).split()),
            'note': lambda v: v
        }[cid]
        values = sorted(values, reverse=reverse, key=key)
        for index, (val, iid) in enumerate(values):
            self.move(iid, '', index)
        self.heading(cid, command=lambda: self.sort_column(cid, not reverse))
