#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


class ScrolledListbox(tk.Listbox):
    def __init__(self, parent, **kwargs):
        box = tk.Frame(parent)
        box.grid(column=0, row=0, sticky=tk.NSEW)
        box.columnconfigure(0, weight=1)
        box.rowconfigure(0, weight=1)
        vbar = tk.Scrollbar(box, orient=tk.VERTICAL)
        vbar.grid(column=1, row=0, sticky=tk.NS)
        hbar = tk.Scrollbar(box, orient=tk.HORIZONTAL)
        hbar.grid(column=0, row=1, sticky=tk.EW)
        hbar.config(command=self.xview)
        vbar.config(command=self.yview)
        kwargs.update({'xscrollcommand': hbar.set, 'yscrollcommand': vbar.set})
        super(ScrolledListbox, self).__init__(box, **kwargs)
