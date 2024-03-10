#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sqlite3
from log_viewer import ConnectionDiary
from tkinter.messagebox import askyesno


# class LogViewerPhony(tk.Tk):
#     def __init__(self, con=None):
#         super().__init__()
#         if con is None:
#             con = sqlite3.connect('pee_diary.db', factory=ConnectionDiary)
#         self.db_con = con


class LabelDb:
    def __init__(self, con):
        self.db_con = con
        self.read_labels_dict()

    # def __init__(self, log_viewer):
    #     self.log_viewer = log_viewer
    #     self.db_con = log_viewer.db_con
    #     self.labels_dict = {}
    #     self.read_labels_dict()

    def __iter__(self):
        for v in self.labels_dict.values():
            yield v

    def read_labels_dict(self):
        q = '''
            SELECT id, label
            FROM labels
        '''
        self.labels_dict = dict(self.db_con.execute(q).fetchall())

    def as_label(self, id: int) -> str:
        return self.labels_dict[id]

    def as_id(self, label_text: str) -> int:
        """Get ID of the existing LABEL_TEXT in the LABELS table

        insert a new label if needed
        """
        for id, lab in self.labels_dict.items():
            if lab == label_text:
                return id
        ins_sql = '''
            INSERT INTO labels (label)
            VALUES (?)
        '''
        id = None
        try:
            msg = f'Add label "{label_text}"? '
            if not askyesno(f"{os.path.basename(__file__)}",
                            msg, parent=self.log_viewer):
                return id
        except NameError:
            if not input(msg).upper() == 'Y':
                return id
        self.db_con.execute(ins_sql, (label_text, ))
        self.read_labels_dict()
        return self.as_id(label_text)
