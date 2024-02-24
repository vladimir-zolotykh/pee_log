#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
import tkinter as tk


class LogRecord(BaseModel):
    id: int
    stamp: datetime = datetime.now()
    label: str = 'pee'
    volume: int = 0
    note: str = ''

    def __str__(self):
        '''Return the string {:>5s}|{:20s}|{:>6s}|{:10s}'''

        return '{:>5s}|{:20s}|{:10s}|{:>6s}|{:10s}'.format(
            *(map(str, list(self.dict().values()))))


class LogViewer(tk.Tk):
    log_list_test = [
        ('639', '2024-01-26 13:00:00', 'pee', '439', 'Creatine'),
        ('640', '2024-01-26 13:31:00', 'pee', '581', ''),
        ('641', '2024-01-26 14:00:00', 'pee', '706', '')
    ]

    def __init__(self, *args, **kwargs):
        super().__init__()
        log_list = tk.Listbox(self, width=40, height=25)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        log_list.grid(column=0, row=0, sticky=tk.NSEW)
        for elem in self.log_list_test:
            opt = {k: v for k, v in zip(LogRecord.__fields__, elem)}
            rec = LogRecord(**opt)
            log_list.insert(tk.END, str(rec))
        form = tk.Frame(self)
        form.grid(column=1, row=0, sticky=tk.N)
        for row, fld in enumerate(LogRecord.__fields__):
            _ = tk.Label(form, text=fld)
            _.grid(column=0, row=row)
            _ = tk.Entry(form)
            _.grid(column=1, row=row)


if __name__ == '__main__':
    v = LogViewer()
    v.mainloop()
