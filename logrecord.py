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

    def as_list(self):
        return list(self.__dict__.values())
