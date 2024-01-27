#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Print records from pee_diary.db database
"""
import argparse
import argcomplete
import sqlite3


class ConnectionDiary(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def select_logs(self):
        return self.execute('''
            SELECT pee_time, volume, note
            FROM pee_log
        ''')


parser = argparse.ArgumentParser(
    description="Print records from pee_diary.db database",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--log-db', default='./pee_diary.db',
                    help='Log database file')
parser.add_argument('--verbose', '-v', action='count', default=0)


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with sqlite3.connect(args.log_db, factory=ConnectionDiary) as conn:
        for row in conn.select_logs():
            print(row)