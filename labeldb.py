#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> from log_viewer import ConnectionDiary
>>> con = sqlite3.connect('pee_diary.db', factory=ConnectionDiary)
>>> root = tk.Tk()
>>> labeldb = LabelDb(con, root)
>>> list(labeldb)
['IMET', 'pee', 'Creatine', 'Coffee', 'headache', 'other', 'poo']
>>> labeldb.get_id('душ')
8
>>> del labeldb['душ']
>>> con.commit()
>>> con.close()
"""
import os
import sqlite3                  # noqa
from log_viewer import ConnectionDiary  # noqa
import tkinter as tk                    # noqa
from tkinter.messagebox import askyesno
from typing import Optional


class LabelDb:
    def __init__(self, con, app):
        self.labels_dict = {}
        self.db_con = con
        self.app = app
        self.read_labels_dict()

    def __iter__(self):
        for v in self.labels_dict.values():
            yield v

    def __delitem__(self, label):
        self.del_label(label)

    def del_label(self, label):
        found = None
        for id in self.labels_dict:
            if self.labels_dict[id] == label:
                found = id
                break
        if found:
            # Delete the label only if it is not referenced in the
            # pee_log table.
            n = self.db_con.execute("""
                SELECT COUNT()
                FROM pee_log
                WHERE ? IN (label1_id, label2_id, label3_id);
            """, (id, )).fetchone()[0]
            if n == 0:          # does not have references
                self.db_con.execute("""
                    DELETE FROM
                    LABELS
                    WHERE id = ?
                """, (id, ))
                del self.labels_dict[found]
                self.read_labels_dict()

    def read_labels_dict(self):
        q = '''
            SELECT id, label
            FROM labels
        '''
        self.labels_dict = dict(self.db_con.execute(q).fetchall())

    def as_label(self, id: int) -> str:
        return self.labels_dict[id]

    def get_id(self, label_text: str) -> Optional[int]:
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
        msg = f'Add label "{label_text}"? '
        title = (f"{os.path.basename(__file__)}" if '__file__' in locals()
                 else " >>> ")
        if askyesno(title, msg, parent=self.app):
            self.db_con.execute(ins_sql, (label_text, ))
            self.read_labels_dict()
            return self.get_id(label_text)
        else:
            return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
