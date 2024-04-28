#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# from dataclasses import dataclass
import os
from typing import Optional     # noqa
from datetime import datetime
import sqlite3
import argparse
import argcomplete
import tkinter as tk
# import tkinter.font as tkFont
from tkinter import ttk         # noqa
from tkinter.messagebox import askyesno
# from scrolled_listbox import ScrolledListbox
from scrolled_treeview import ScrolledTreeview
from time4 import Time4, Time4Var
from combo_db import ComboDb
from logrecord import LogRecord
import labeldb
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, select
# from sqlalchemy import func
import sampletag as SA
# from apeelog2 import Logged, Event
import button_font
from tooltip import Tooltip


class ConnectionDiary(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
        self.labels = labeldb.LabelDb(self, self.app)  # "labels" table

    def make_tables(self):
        self.execute('''
            CREATE TABLE IF NOT EXISTS labels (
                id INTEGER PRIMARY KEY,
                label TEXT NOT NULL UNIQUE
            );
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS pee_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pee_time TEXT,
                label1_id INTEGER,
                label2_id INTEGER,
                label3_id INTEGER,
                volume INTEGER DEFAULT 0,
                note TEXT DEFAULT '')
        ''')

    def read_logs(self):
        # val = LabelDb(log_viewer).label_to_id(val)
        return (LogRecord.from_db(self, row)
                for row in self.execute('SELECT * FROM pee_log'))


class LogViewer(tk.Tk):
    # LOG_FORM_FLD = f'_{fld_name}_var'
    log_list_test = [
        ('639', '2024-01-26 13:00:00', 'pee', '439', 'Creatine'),
        ('640', '2024-01-26 13:31:00', 'pee', '581', ''),
        ('641', '2024-01-26 14:00:00', 'pee', '706', '')
    ]

    # def __init__(self, con, *args, **kwargs):
    def __init__(self, engine):
        super().__init__()
        # self.db_con = con
        self.engine = engine
        # con.app = self          # use case: askyesno(parent=con.app,...
        self.form_vars = {}
        # Better not to mention data structure type in a variable name
        log_list = ScrolledTreeview(self, columns=('id', 'stamp', 'label',
                                                   'volume', 'note'),
                                    selectmode='browse')
        # log_list = ScrolledListbox(self, selectmode=tk.SINGLE, width=60,
        #                            height=25, font=('Courier', 12))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        log_list.grid(column=0, row=0, sticky=tk.NSEW)
        # .bind: two handlers are called: ScrolledTreeview.on_select,
        # then LogViewer.on_treeview_select
        log_list.bind('<<TreeviewSelect>>', self.on_treeview_select, add='+')
        self.log_list = log_list
        self.update_log_list()
        form = tk.Frame(self)
        form.grid(column=1, row=0, sticky=tk.NS)
        row = self.create_form_fields(form)
        row += 1
        buttons_bar = tk.Frame(form)
        form.rowconfigure(row, weight=1)
        buttons_bar.grid(column=0, row=row, columnspan=2, sticky=tk.S)
        update_btn = tk.Button(buttons_bar,
                               text='Update', command=self.edit_log)
        Tooltip(update_btn, """\
Update the existing sample or
create a new one""",
                font=button_font.TooltipFont())
        narrow_btn = tk.Button(buttons_bar,
                               text='Narrow\nto date',
                               command=self.narrow_to_date)
        Tooltip(narrow_btn, """\
Enter the date into "stamp" field above then press me.
Clear the "stamp" to see all logs.""",
                font=button_font.TooltipFont())
        self.script_btn = tk.Menubutton(
            buttons_bar, text='Script', relief=tk.RAISED, bd=2)
        menu = tk.Menu(self.script_btn, tearoff=0)
        self.script_btn.config(menu=menu)
        menu.add_command(label='Blank sample',
                         font=button_font.ButtonFont(),
                         command=self.make_new)
        menu.add_command(label='IMET', font=button_font.ButtonFont(),
                         command=self.make_new)
        # self.erase_btn = tk.Button(buttons_bar, text='new',
        #                            command=self.make_new)
        Tooltip(self.script_btn, """\
Initialize the fields above for the new sample""",
                font=button_font.TooltipFont())
        self.del_btn = tk.Button(
            buttons_bar, text='Del', command=self.del_log, state=tk.DISABLED)
        self.del_btn.grid(column=2, row=0)
        Tooltip(self.del_btn, """\
Delete from the database the existing sample""",
                font=button_font.TooltipFont())
        # >>> tkFont.nametofont('TkDefaultFont').config()['family']
        # 'sans-serif'
        for col, btn in enumerate((update_btn, narrow_btn, self.script_btn,
                                   self.del_btn)):
            size = 6 if btn.cget('text').startswith('Narrow') else 8
            btn.grid(column=col, row=0)
            btn.config(font=button_font.ButtonFont(size=size))

    def narrow_to_date(self):
        # stamp str -> datetime obj
        try:
            req_date = datetime.strptime(
                self.get_var('stamp').get(), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            req_date = None
        self.update_log_list(req_date)

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
            elif fld_name.startswith('label'):
                _ = ComboDb(form, self.engine, textvariable=var)
                _.update_values()
                padx = 2
            else:
                _ = tk.Entry(form, textvariable=var)
                padx = 1
            _.bind("<Double-1>", self.muffle_click)
            _.grid(column=1, row=row, sticky=tk.W, padx=padx, pady=2)
        return row

    def muffle_click(self, event):
        return "break"

    def update_log_list(
            self,
            narrow_to_date: Optional[datetime.date] = None  # %Y-%m-%d
    ):
        """Update Treeview (.log_list)

        delete all view items, read all db records, add them to the view"""

        self.log_list.delete(*self.log_list.get_children(''))
        # Session = SA.sessionmaker(self.engine)
        on_date = True          # all samples
        if narrow_to_date:
            # narrow_to_date datetime obj -> date str
            date_str = narrow_to_date.strftime('%Y-%m-%d')
            on_date = (SA.func.DATE(SA.Sample.time) == date_str)
        with SA.Session(self.engine) as session:
            for rec in session.scalars(SA.select(SA.Sample).where(on_date)):
                labels = [''] * 3
                for i in range(3):
                    try:
                        t = rec.tags[i].text
                    except IndexError:
                        t = ''
                    labels[i] = t
                log = LogRecord(
                    id=rec.id,
                    stamp=rec.time,
                    label1=labels[0],
                    label2=labels[1],
                    label3=labels[2],
                    volume=rec.volume,
                    note=rec.text if rec.text else '')
                self.log_list.insert_log(log)

    def get_var(self, fld_name):
        """Return tk.StringVar "form variable" named FLD_NAME

        variable objects are stored in the self.form_vars
        dictionary. If the variable doesn't exist, it is created"""

        if fld_name not in self.form_vars:
            if fld_name == 'stamp':
                var = Time4Var()
            elif fld_name.startswith('label'):
                var = tk.StringVar()
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

        for fld_name, var in self.form_vars.items():
            if fld_name == 'id':
                Session = SA.sessionmaker(self.engine)
                with Session() as session:
                    id = session.query(SA.func.max(SA.Sample.id)).scalar()
                var.set(str(id + 1) if isinstance(id, int) else '1')
            elif fld_name == 'stamp':
                dt = datetime.now()
                var.set(dt)
            elif fld_name == 'volume':
                var.set('0')
            elif fld_name == 'label1':
                var.set('pee')
            else:
                var.set('')
        self.del_btn.config(state=tk.DISABLED)

    def del_log(self):
        """Delete selected log record"""

        rec = self.get_logrecord()
        if askyesno(f"{os.path.basename(__file__)}",
                    f"Delete log id={rec.id}? ",
                    parent=self):
            Session = SA.sessionmaker(self.engine)
            with Session() as session:
                delete_me = session.scalar(SA.select(SA.Sample).where(
                    SA.Sample.id == rec.id))
                session.delete(delete_me)
                session.commit()
            self.update_log_list()

    def edit_log(self) -> None:
        """Add/update log record (Sample) to "sample" table"""

        rec = self.get_logrecord()
        # with SA.Session(self.engine) as session:
        with SA.session_scope(self.engine) as session:
            sample = session.get(SA.Sample, rec.id)
            if sample:
                if askyesno(f"{os.path.basename(__file__)}",
                            f"Log {rec.id} exists. Update? ",
                            parent=self):
                    SA.update_sample(session, sample, rec)
            else:
                sample = SA.Sample(id=rec.id, time=rec.stamp,
                                   volume=rec.volume, text=rec.note)
                SA.add_sample(session, sample, rec)
        self.update_log_list()

    def update_fields(self, log_rec: LogRecord) -> None:
        """Update form Entry values"""

        for fld_name in LogRecord.__fields__:
            val = getattr(log_rec, fld_name)
            if fld_name == 'volume' and val is None:
                val = ''
            self.set_val(fld_name, val)

    def get_logrecord(self) -> LogRecord:
        '''Get 'form' fields, make a LogRecord from them, return'''

        # return LogRecord.from_list([self.get_var(fld_name).get(parent=self)
        #                             for fld_name in LogRecord.__fields__])
        values = []
        for fld_name in LogRecord.__fields__:
            var = self.get_var(fld_name)
            if fld_name.startswith('label'):
                # values.append(var.get(parent=self))
                values.append(var.get())
            else:
                values.append(var.get())
        return LogRecord.from_list(values)

    def on_treeview_select(self, event):
        log = self.log_list.selected_log
        if log:
            self.update_fields(log)
            self.del_btn.config(state=tk.NORMAL)


parser = argparse.ArgumentParser(
    description="pee_log db veiwer",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--db', help='Database file (.db)',
                    default='./sampletag.db')
parser.add_argument('--echo', action='store_true', default=False,
                    help='Print emitted SQL commands')


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    v = LogViewer(SA.create_engine(f'sqlite:///{args.db}', echo=args.echo))
    v.mainloop()
