#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from tkinter import ttk
import sampletag as SA


class ComboDb(ttk.Combobox):
    values_default = ['pee', 'IMET', 'Creatine', 'Coffee', 'headache', 'other']

    def __init__(self, parent, engine, **kwds):
        self.parent, self.engine = parent, engine
        # super(ComboDb, self).__init__(parent, values=self.values_default,
        #                               **kwds)
        super(ComboDb, self).__init__(parent, values=[], **kwds)
        self.bind('<Enter>', lambda event: self.update_values())
        self.update_values()

    def update_values(self) -> None:
        # Session = SA.sessionmaker(self.engine)
        with SA.Session(self.engine) as session:
            values = [tag.text for tag in session.scalars(SA.select(SA.Tag))]
        self.config(values=values)
