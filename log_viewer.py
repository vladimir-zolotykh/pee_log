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

    @classmethod
    def from_list(cls, values):
        opt = {k: v.strip() for k, v in zip(cls.__fields__, values)}
        return cls(**opt)

    def __str__(self):
        '''Return the string {:>5s}|{:20s}|{:>6s}|{:10s}'''

        return '{:>5s}|{:20s}|{:10s}|{:>6s}|{:10s}'.format(
            *(map(str, list(self.dict().values()))))


class LogViewer(tk.Tk):
    # LOG_FORM_FLD = f'_{fld_name}_var'
    log_list_test = [
        ('639', '2024-01-26 13:00:00', 'pee', '439', 'Creatine'),
        ('640', '2024-01-26 13:31:00', 'pee', '581', ''),
        ('641', '2024-01-26 14:00:00', 'pee', '706', '')
    ]

    def __init__(self, *args, **kwargs):
        super().__init__()
        log_list = tk.Listbox(self, selectmode=tk.SINGLE, width=40, height=25)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        log_list.grid(column=0, row=0, sticky=tk.NSEW)
        log_list.bind('<<ListboxSelect>>', self.on_select)
        self.log_list = log_list
        for elem in self.log_list_test:
            rec = LogRecord.from_list(elem)
            log_list.insert(tk.END, str(rec))
        form = tk.Frame(self)
        form.grid(column=1, row=0, sticky=tk.NS)
        for row, fld_name in enumerate(LogRecord.__fields__):
            _ = tk.Label(form, text=fld_name)
            _.grid(column=0, row=row)
            var = tk.StringVar()
            # The name of the tk.StringVar variable holding the
            # corresponding LogRecord attribute,
            # e.g., LogRecord.stamp -> self._stamp_var
            setattr(self, f'_{fld_name}_var', var)
            _ = tk.Entry(form, textvariable=var)
            _.grid(column=1, row=row)
        row += 1
        buttons_bar = tk.Frame(form)
        form.rowconfigure(row, weight=1)
        buttons_bar.grid(column=0, row=row, columnspan=2, sticky=tk.S)
        add_btn = tk.Button(buttons_bar, text='Add', command=self.add_log)
        add_btn.grid(column=0, row=0)
        update_btn = tk.Button(buttons_bar, text='Update',
                               command=self.update_log)
        update_btn.grid(column=1, row=0)

    def add_log(self):
        rec = self.get_logrecord()
        print(f'{rec = }')

    def update_log(self):
        rec = self.get_logrecord()
        print(f'{rec = }')

    def update_fields(self, log_rec: LogRecord):
        for row, fld_name in enumerate(LogRecord.__fields__):
            var = getattr(self, f'_{fld_name}_var')
            var.set(getattr(log_rec, fld_name))

    def get_logrecord(self) -> LogRecord:
        fld_list = []
        for fld_name in LogRecord.__fields__:
            fld_val = getattr(self, f'_{fld_name}_var').get()
            fld_list.append(fld_val)
        return LogRecord.from_list(fld_list)

    def on_select(self, event):
        index = event.widget.curselection()
        if isinstance(index, tuple):
            index = index[0]
        item = event.widget.get(index)
        rec = LogRecord.from_list(item.split('|'))
        self.update_fields(rec)


if __name__ == '__main__':
    v = LogViewer()
    v.mainloop()
