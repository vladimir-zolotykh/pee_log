#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# from dataclasses import dataclass
import os
from datetime import datetime
from pydantic import BaseModel
import sqlite3
import argparse
import argcomplete
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from scrolled_listbox import ScrolledListbox
from time4 import Time4, Time4Var


class ConnectionDiary(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_tables(self):
        self.execute('''
            CREATE TABLE labels (
                id INTEGER PRIMARY KEY,
                label TEXT NOT NULL UNIQUE
            );
        ''')

        self.execute('''
            CREATE TABLE IF NOT EXISTS pee_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pee_time TEXT,
                label TEXT,
                volume INT DEFAULT 0,
                note TEXT DEFAULT '')
        ''')

    def read_logs(self):
        return (LogRecord.from_list(row)
                for row in self.execute('SELECT * FROM pee_log'))


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
        log_list = ScrolledListbox(self, selectmode=tk.SINGLE, width=60,
                                   height=25, font=('Courier', 12))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        log_list.grid(column=0, row=0, sticky=tk.NSEW)
        log_list.bind('<<ListboxSelect>>', self.on_select)
        self.log_list = log_list
        self.update_log_list()
        form = tk.Frame(self)
        form.grid(column=1, row=0, sticky=tk.NS)
        row = self.create_form_fields(form)
        row += 1
        buttons_bar = tk.Frame(form)
        form.rowconfigure(row, weight=1)
        buttons_bar.grid(column=0, row=row, columnspan=2, sticky=tk.S)
        update_btn = tk.Button(buttons_bar, text='Update',
                               command=self.update_log)
        update_btn.grid(column=0, row=0)
        self.erase_btn = tk.Button(buttons_bar, text='new',
                                   command=self.make_new)
        self.erase_btn.grid(column=1, row=0)
        self.del_btn = tk.Button(buttons_bar, text='Del', command=self.del_log,
                                 state=tk.DISABLED)
        self.del_btn.grid(column=2, row=0)

    def create_form_fields(self, form) -> int:
        """Create form fields and their StringVar -s

        see self.form_vars dict
        """
        for row, fld_name in enumerate(LogRecord.__fields__):
            _ = tk.Label(form, text=fld_name)
            _.grid(column=0, row=row, sticky=tk.E)
            var = self.get_var(fld_name)
            if fld_name == 'stamp':
                _ = Time4(form, time4variable=var)
                padx = 1
            elif fld_name == 'label':
                _ = ttk.Combobox(form, textvariable=var,
                                 values=['pee', 'IMET', 'Creatine', 'Coffee',
                                         'headache', 'other'])
                padx = 2
            else:
                _ = tk.Entry(form, textvariable=var)
                padx = 1
            _.bind("<Double-1>", self.muffle_click)
            _.grid(column=1, row=row, sticky=tk.W, padx=padx, pady=2)
        return row

    def muffle_click(self, event):
        return "break"

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
            if fld_name == 'stamp':
                var = Time4Var()
            else:
                var = tk.StringVar()
            self.form_vars[fld_name] = var
        return self.form_vars[fld_name]

    def set_val(self, fld_name, value=''):
        """Set "form variable" value

        see get_var.__doc__"""

        var = self.get_var(fld_name)
        var.set(value)

    def make_new(self):
        """Set the form field to the defaults"""

        max_sql = '''
            SELECT MAX(id) + 1
            FROM pee_log
        '''

        for fld_name, var in self.form_vars.items():
            if fld_name == 'id':
                var.set(str(self.db_con.execute(max_sql).fetchone()[0]))
            elif fld_name == 'stamp':
                dt = datetime.now()
                var.set(dt)
            elif fld_name == 'volume':
                var.set('0')
            elif fld_name == 'label':
                var.set('pee')
            else:
                var.set('')
        self.del_btn.config(state=tk.DISABLED)

    def del_log(self):
        """Delete selected log record"""

        rec = self.get_logrecord()
        del_sql = '''
            DELETE FROM pee_log
            WHERE id = ?
        '''
        if askyesno(f"{os.path.basename(__file__)}",
                    f"Delete log id={rec.id}? ",
                    parent=self):
            self.db_con.execute(del_sql, (rec.id, ))
        self.update_log_list()

    def update_log(self):
        '''Update the record or add a new

        if ID exists in the db, update the record, otherwise add a new
        record
        '''
        rec = self.get_logrecord()
        ins_cmd = """
            INSERT INTO pee_log (id, pee_time, label, volume, note)
            VALUES (?, ?, ?, ?, ?)
        """
        upd_cmd = """
            UPDATE pee_log
            SET pee_time = ?, label = ?, volume = ?, note = ?
            WHERE id = ?
        """
        try:
            self.db_con.execute(ins_cmd, list(rec.dict().values()))
        except sqlite3.IntegrityError:
            if askyesno(f"{os.path.basename(__file__)}",
                        f"Log {rec.id} exists. Update? ",
                        parent=self):
                _values = list(rec.dict().values())
                self.db_con.execute(upd_cmd, _values[1:] + _values[:1])
        self.update_log_list()

    def update_fields(self, log_rec: LogRecord):
        for row, fld_name in enumerate(LogRecord.__fields__):
            self.set_val(fld_name, getattr(log_rec, fld_name))

    def get_logrecord(self) -> LogRecord:
        '''Get 'form' fields, make a LogRecord from them, return'''

        return LogRecord.from_list([self.get_var(fld_name).get()
                                    for fld_name in LogRecord.__fields__])

    def on_select(self, event):
        selected_lines = self.log_list.curselection()
        if bool(selected_lines):  # ensure selected_lines tuple is not empty
            index = selected_lines[0]
            item = self.log_list.get(index)
            rec = LogRecord.from_list(item.split('|'))
            self.update_fields(rec)
            self.del_btn.config(state=tk.NORMAL)


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
