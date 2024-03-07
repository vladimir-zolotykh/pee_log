#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno


class ComboVar(tk.StringVar):
    def __init__(self, db_con):
        self.db_con = db_con
        super().__init__()

    def get(self, parent=None):
        # Search for line get(parent=self)
        self.parent = parent
        val = super().get()
        sql_exists = '''
            SELECT EXISTS(SELECT 1 FROM labels WHERE label=?)
        '''
        sql_insert = '''
            INSERT INTO labels(label)
            VALUES (?)
        '''
        exists = self.db_con.execute(sql_exists, (val, )).fetchone()[0]
        if not bool(exists):
            if askyesno(f"{os.path.basename(__file__)}",
                        f"Add label {val}? ",
                        parent=parent):
                self.db_con.execute(sql_insert, (val, ))


class ComboDb(ttk.Combobox):
    values_default = ['pee', 'IMET', 'Creatine', 'Coffee', 'headache', 'other']

    def __init__(self, parent, db_con, **kwargs):
        self.parent = parent    # LogViewer obj
        self.db_con = db_con    # where is the labels table
        if 'values' not in kwargs:
            kwargs.update({'values': self.values_default})
        super(ComboDb, self).__init__(parent, **kwargs)

    def update_values(self):
        sql = '''
            SELECT *
            FROM labels
            ORDER by label

        '''
        labels_dict = {id: lab for id, lab in self.db_con.execute(sql)}
        self.config(values=list(labels_dict.values()))
