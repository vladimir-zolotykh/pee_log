#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
import tkinter as tk
import sqlite3
import argparse
import argcomplete


class ConnectionDiary(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read_logs(self):
        return (LogRecord.from_list(row[:2] + ('pee', ) + row[2:])
                for row in self.execute('select * from pee_log'))


class LogRecord(BaseModel):
    id: int
    stamp: datetime = datetime.now()
    label: str = 'pee'
    volume: int = 0
    note: str = ''

    @classmethod
    def from_list(cls, values):
        def _strip_if(a):
            return a.strip() if isinstance(a, str) else a

        opt = {k: _strip_if(v) for k, v in zip(cls.__fields__, values)}
        return cls(**opt)

    def __str__(self):
        '''Return Listbox line at "as it is"'''

        values = list(map(str, list(self.dict().values())))
        values[1] = self.stamp.strftime('%Y-%m-%d %H:%M')
        return '{:>5s}|{:17s}|{:10s}|{:>6s}|{:10s}'.format(*values)


class LogViewer(tk.Tk):
    # LOG_FORM_FLD = f'_{fld_name}_var'
    log_list_test = [
        ('639', '2024-01-26 13:00:00', 'pee', '439', 'Creatine'),
        ('640', '2024-01-26 13:31:00', 'pee', '581', ''),
        ('641', '2024-01-26 14:00:00', 'pee', '706', '')
    ]

    def __init__(self, con, *args, **kwargs):
        super().__init__()
        self.db_con = con
        self.form_vars = {}
        # form variables (StringVar), id, stamp, etc. (see LogRecord)
        log_list = tk.Listbox(self, selectmode=tk.SINGLE, width=60, height=25,
                              font=('Courier', 12))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        log_list.grid(column=0, row=0, sticky=tk.NSEW)
        log_list.bind('<<ListboxSelect>>', self.on_select)
        self.log_list = log_list
        self.update_log_list()
        form = tk.Frame(self)
        form.grid(column=1, row=0, sticky=tk.NS)
        for row, fld_name in enumerate(LogRecord.__fields__):
            _ = tk.Label(form, text=fld_name)
            _.grid(column=0, row=row)
            var = self.get_var(fld_name)
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

    def update_log_list(self):
        """Update Listbox (.log_list)

        clear the list, read all db records, insert them into the list"""

        self.log_list.delete(0, tk.END)
        for log in self.db_con.read_logs():
            self.log_list.insert(tk.END, str(log))

    def get_var(self, fld_name):
        """Return tk.StringVar "form variable" named FLD_NAME

        variable objects are stored in the self.form_vars
        dictionary. If the variable doesn't exist, it is created"""

        if fld_name not in self.form_vars:
            self.form_vars[fld_name] = tk.StringVar()
        return self.form_vars[fld_name]

    def set_val(self, fld_name, value=''):
        """Set "form variable" value

        see get_var.__doc__"""

        var = self.get_var(fld_name)
        var.set(value)

    def add_log(self):
        rec = self.get_logrecord()
        print(f'{rec = }')

    def update_log(self):
        rec = self.get_logrecord()
        print(f'{rec = }')

    def update_fields(self, log_rec: LogRecord):
        for row, fld_name in enumerate(LogRecord.__fields__):
            self.set_val(fld_name, getattr(log_rec, fld_name))

    def get_logrecord(self) -> LogRecord:
        return LogRecord.from_list([self.get_var(fld_name).get()
                                    for fld_name in LogRecord.__fields__])

    def on_select(self, event):
        index = event.widget.curselection()
        if isinstance(index, tuple):
            index = index[0]
        item = event.widget.get(index)
        rec = LogRecord.from_list(item.split('|'))
        self.update_fields(rec)


parser = argparse.ArgumentParser(
    description="pee_log db veiwer",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--db', help='Database file (.db)',
                    default='./pee_diary.db')


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with sqlite3.connect(args.db, factory=ConnectionDiary) as con:
        v = LogViewer(con)
        v.mainloop()
