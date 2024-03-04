#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from datetime import datetime


class Time4Var(tk.StringVar):
    """
>>> dt = datetime.strptime('2024-03-04 09:10:11', '%Y-%m-%d %H:%M:%S')
>>> dt
datetime.datetime(2024, 3, 4, 9, 10, 11)
>>> v4 = Time4Var.from_datetime(dt)
>>> v4.as_str()
'2024-03-04 09:10:11'
>>> v4.as_datetime()
datetime.datetime(2024, 3, 4, 9, 10, 11)
>>> dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
>>> v4 = Time4Var.from_str(dt_str)
>>> v4.as_str()
'2024-03-04 09:10:11'

    """
    def __init__(self):
        self.day = tk.StringVar()
        self.time4 = tk.StringVar()
        super(Time4Var, self).__init__()

    @classmethod
    def from_str(cls, dt_str: str):
        d = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        t4 = cls()
        day, time4 = d.isoformat(' ').split()
        t4.day.set(day)
        t4.time4.set(time4)
        return t4

    @classmethod
    def from_datetime(cls, dt: datetime):
        """Convert datetime str into Time4Var"""

        t4 = cls()
        t4.day.set(str(dt.date()))
        t4.time4.set(str(dt.time()))
        return t4

    def as_str(self) -> str:
        return f'{self.day.get()} {self.time4.get()}'

    def as_datetime(self) -> datetime:
        return datetime.strptime(self.as_str(), '%Y-%m-%d %H:%M:%S')

    def set(self, day: str, time4: str):
        self.day = day
        self.time4 = time4

    def get(self):
        return self.day, self.time4


class Time4(tk.Entry):
    """Combine date (%Y-%m-%d) and time (%H%M)"""

    def __init__(self, parent):
        box = tk.Frame(parent)
        box.grid(column=0, row=0, sticky=tk.EW)
        box.columnconfigure(0, weight=1)
        self.day_var = tk.StringVar()
        day_entry = tk.Entry(box, width=8, textvariable=self.day_var)
        day_entry.grid(column=0, row=0)
        self.time_var = tk.StringVar()
        time_entry = tk.Entry(box, width=4, textvariable=self.time_var)
        time_entry.grid(column=1, row=0)
        super(Time4, self).__init__(parent)
        setattr(self, 'grid', getattr(box, 'grid'))

    def set4(self, stamp: str):
        d = datetime.strptime('%Y-%m-%d %H:%M:%S', str)
        self.day_var.set(d.date())
        self.time_var.set(d.time())

    def get4(self) -> str:
        day = self.day_var.get()
        time = datetime.strptime(self.time_var.get(),
                                 '%H%M').strftime('%H:%M:%S')
        return (day + time)
