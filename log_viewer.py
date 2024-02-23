#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk


class LogViewer(tk.Tk):
    log_list_test = [
        ('639', '2024-01-26 13:00:00', '439', 'Creatine'),
        ('640', '2024-01-26 13:31:00', '581', ''),
        ('641', '2024-01-26 14:00:00', '706', '')
    ]
    fields = [
        'Date',
        'Label',
        'Volume',
        'Note',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__()
        log_list = tk.Listbox(self, width=40, height=25)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        log_list.grid(column=0, row=0, sticky=tk.NSEW)
        for elem in self.log_list_test:
            line = '{:>5s}|{:20s}|{:>6s}|{:10s}'.format(*elem)
            log_list.insert(tk.END, line)
        form = tk.Frame(self)
        form.grid(column=1, row=0, sticky=tk.N)
        for row, fld in enumerate(self.fields):
            _ = tk.Label(form, text=fld)
            _.grid(column=0, row=row)
            _ = tk.Entry(form)
            _.grid(column=1, row=row)


if __name__ == '__main__':
    v = LogViewer()
    v.mainloop()
