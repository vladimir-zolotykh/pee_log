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
    volume: Optional[int] = None
    note: str = ''

    def __str__(self):
        values = []
        for field_name, field_value in self.__dict__.items():
            typ = self.__annotations__[field_name]  # int, str, or datetime
            if field_value is None:
                continue
            if typ == int or isinstance(field_value, int):
                values.append(str(field_value))
            elif typ == datetime:
                values.append(datetime.strftime(field_value, '%H%M'))
            else:
                values.append(field_value)
        # skip 'id' field
        return ' '.join((val for val in values[1:] if bool(val)))

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

    @property
    def tags_count(self):
        caps = (f'label{n}' for n in range(1, 4))
        return sum((1 for cap in caps if getattr(self, cap) != ''))

    @property
    def has_tags(self):
        caps = (f'label{n}' for n in range(1, 4))
        return any((getattr(self, cap) != '' for cap in caps))

    @property
    def has_volume(self):
        return isinstance(self.volume, int) and 0 < self.volume

    @property
    def has_note(self):
        return self.note != ''
