#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
"""
# import os
from pydantic import BaseModel
from datetime import datetime
# from tkinter.messagebox import askyesno
from typing import Optional


class LogRecord(BaseModel):
    id: int
    stamp: datetime = datetime.now()
    label1: str = 'pee'
    label2: str = ''
    label3: str = ''
    volume: int = Optional[None]
    note: str = ''

    @classmethod
    def from_list(cls, values: list):
        def _strip_if(a):
            return a.strip() if isinstance(a, str) else a

        opt = {k: _strip_if(v) for k, v in zip(cls.__fields__, values)}
        return cls(**opt)

    @classmethod
    def from_db(cls, db, values: list):
        opt = {k: v for k, v in zip(cls.__fields__, values)}
        for label_caption, label_id in opt.items():
            if label_caption.startswith('label'):
                label_text = (db.labels.as_label(label_id)
                              if isinstance(label_id, int) else '')
                opt[label_caption] = label_text
        return cls(**opt)

    def __str__(self):
        '''Return Listbox line at "as it is"'''

        values = list(map(str, list(self.dict().values())))
        values[1] = self.stamp.strftime('%Y-%m-%d %H:%M')
        return '{:>5s}|{:17s}|{:10s}|{:10s}|{:10s}|{:>6s}|{:10s}'.format(
            *values)


# class Labels:
#     def __init__(self, *values):
#         self.labels_db
#         self.labels = values

#     def get_text(self):
#         pass

#     def get_id(self):
#         pass

#     def __getitem__(self, n):
#         return self.labels[n]


# class LogRecordDb:
#     def __init__(self, log_viewer, logrecord: Type[LogRecord]):
#         self.log_viewer = log_viewer
#         self.db_conn = log_viewer.db_con
#         self.logrecord = logrecord
#         for i in range(1, 4):   # self.label<n>_id = 0
#             setattr(self, f'label{i}_id', 0)
#         self.labels_dict = {}

#     def update_id(self):
#         for f in self.logrecord.__fields__:
#             val = getattr(self.logrecord, f)
#             if f.startswith('label') and bool(val):
#                 id = self.db_conn.labeldb.as_id(f)
#                 setattr(self, f'{f}_id', id)

#     def labels_iter(self):
#         for i in range(1, 4):
#             yield self.db_conn.labeldb.as_label(
#                 getattr(self, f'lable{i}_id'))
