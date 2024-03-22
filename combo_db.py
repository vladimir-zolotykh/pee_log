#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from tkinter import ttk
from sqlalchemy.orm import Session
from sqlalchemy import select
from apeelog2 import Event


# class ComboVar(tk.StringVar):
#     def __init__(self, db_con):
#         self.db_con = db_con
#         super().__init__()

#     def get(self):
#         val = super().get()
#         return val


class ComboDb(ttk.Combobox):
    values_default = ['pee', 'IMET', 'Creatine', 'Coffee', 'headache', 'other']

    def __init__(self, parent, engine, **kwds):
        self.parent, self.engine = parent, engine
        super(ComboDb, self).__init__(parent, values=self.values_default,
                                      **kwds)
        self.update_values()

    def update_values(self) -> None:
        with Session(self.engine) as session:
            values = [event.text for event in session.scalars(select(Event))]
        self.config(values=values)

    # def update_values(self):
    #     sql = '''
    #         SELECT *
    #         FROM labels
    #         ORDER by label

    #     '''
    #     labels_dict = {id: lab for id, lab in self.db_con.execute(sql)}
    #     self.config(values=list(labels_dict.values()))
