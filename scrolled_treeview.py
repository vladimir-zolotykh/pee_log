#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""Example how to use (from summary_view module):
from scrolled_treeview import ScrolledTreeview, ContextMenuMixin

class S0:
    pass

class SummaryView(ScrolledTreeview, S0, ContextMenuMixin):
    def __init__(self, parent, **kwds):
        super(SummaryView, self).__init__(parent, **kwds)
        super(S0, self).__init__()  # ContextMenuMixin.__init__
        . . .
    def make_context_menu(self) -> tk.Menu:
        m = tk.Menu(self, tearoff=0)
        m.add_command(label="SummaryView action", command=None)
        return m
"""

from typing import Protocol
from abc import abstractmethod
import tkinter as tk
from tkinter import ttk


class TreeviewProto(Protocol):
    def bind(self, sequence, func=None, add=None):
        ...

    def identify_row(self, y):
        ...

    def selection_set(self, items):
        ...


class ContextMenuMixin(TreeviewProto):
    def __init__(self, *args, **kwargs):
        self.context_menu = self.make_context_menu()
        self.bind('<Button-3>', self.show_context_menu)

    @abstractmethod
    def make_context_menu(self) -> tk.Menu:
        pass

    def show_context_menu(self, event: tk.Event) -> None:
        item_id = self.identify_row(event.y)
        if item_id:
            self.selection_set(item_id)
            try:
                self.context_menu.post(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()


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
