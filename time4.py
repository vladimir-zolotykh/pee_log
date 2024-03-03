#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from datetime import datetime


class Time4(tk.Entry):
    """Combine date (%Y-%m-%d) and time (%H%M)"""

    def __init__(self, parent, textvariable=None):
        box = tk.Frame(parent)
        box.grid(column=0, row=0, sticky=tk.EW)
        box.columnconfigure(0, weight=1)
        self.day_var = tk.StringVar()
        day_entry = tk.Entry(box, width=8, textvariable=self.day_var)
        day_entry.grid(column=0, row=0)
        self.time_var = tk.StringVar()
        time_entry = tk.Entry(box, width=4, textvariable=self.time_var)
        time_entry.grid(column=1, row=0)
        super(Time4, self).__init__(parent, textvariable=textvariable)
        setattr(self, 'grid', getattr(box, 'grid'))

    def get(self):
        day = self.day_var.get()
        time = datetime.strptime(self.time_var.get(),
                                 '%H%M').strftime('%H:%M:%S')
        return (day + time)
    pass
