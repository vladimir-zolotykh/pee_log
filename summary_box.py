#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import List, Literal
from contextlib import contextmanager
import tkinter as tk


@contextmanager
def text_state(text: tk.Text, state: Literal['normal', 'disabled']) -> tk.Text:
    prev_state = text.cget('state')
    text.config(state=state)
    yield text
    text.config(state=prev_state)


class SummaryBox():
    def __init__(self, box: tk.Frame):

        tk.Label(box, text='Date').grid(column=0, row=0, sticky=tk.E)
        self.date_var = tk.StringVar()
        date = tk.Entry(box, width=12, textvariable=self.date_var,
                        state='readonly')
        date.grid(column=1, row=0, sticky=tk.W)
        # self.date = '2024-02-12'

        tk.Label(box, text='Count').grid(column=0, row=1, sticky=tk.E)
        self.count_var = tk.StringVar()
        count = tk.Entry(box, width=4, textvariable=self.count_var,
                         state='readonly')
        count.grid(column=1, row=1, sticky=tk.W)
        # self.count = '23'

        tk.Label(box, text='Tag').grid(column=0, row=2, sticky=tk.E)
        self.tag_text = tk.Text(box, width=20, height=5, state='disabled')
        self.tag_text.grid(column=1, row=2, sticky=tk.W)
        # self.tag = 'IMET\npee\nMefenamic_acid'.split('\n')

        tk.Label(box, text='Note').grid(column=0, row=3, sticky=tk.E)
        self.note_text = tk.Text(box, width=20, height=5, state='disabled')
        self.note_text.grid(column=1, row=3, sticky=tk.W)
        # self.note = 'Lost sefl control\nСильно болит голова'.split('\n')

    @property
    def date(self) -> str:
        return self.date_var.get()

    @date.setter
    def date(self, value: str) -> None:
        self.date_var.set(value)

    @property
    def count(self) -> str:
        return self.count_var.get()

    @count.setter
    def count(self, value: str) -> None:
        self.count_var.set(value)

    @property
    def tag(self) -> List[str]:
        return self.tags_text.get().split('\n')

    @tag.setter
    def tag(self, value: List[str]) -> None:
        with text_state(self.tag_text, 'normal') as text:
            text.insert('0.0', '\n'.join(value))

    @property
    def note(self) -> List[str]:
        return self.note_text.get('0.0', tk.END).split('\n')

    @note.setter
    def note(self, value: List[str]) -> None:
        with text_state(self.note_text, 'normal') as text:
            text.insert('0.0', '\n'.join(value))
