#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Add records to pee_diary.db database

Read all logs for one day given at the command line. Duplicated
records are silently overwritten.
"""
import argparse
import argcomplete
import sqlite3
import parse_log_re


class ConnectionDiary(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_tables()

    def make_tables(self):
        self.execute('''
            CREATE TABLE IF NOT EXISTS pee_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
            pee_time TEXT,
            volume INT DEFAULT 0,
            note TEXT DEFAULT '')
        ''')

    def insert_log(self, pee_time, volume=None, note=''):
        try:
            self.execute('''
                INSERT INTO pee_log (pee_time)
                VALUES (?)
            ''', (pee_time, ))
        except sqlite3.IntegrityError as e:
            print(f"SQLite IntegrityError: {e}")


parser = argparse.ArgumentParser(
    description="Add one day logs to the DB",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('log_file')
parser.add_argument('--log-db', default='./pee_diary.db',
                    help='Log database file')
parser.add_argument('--verbose', '-v', action='count', default=0)


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with open(args.log_file) as log_file:
        with sqlite3.connect(args.log_db, factory=ConnectionDiary) as conn:
            log_str = log_file.read()
            parse_res = parse_log_re.parse_log_re(log_str)
            for ts_vol_note in parse_log_re.log_to_timestamps(
                    parse_res[0][0], *parse_res[0][1]):
                ts = ts_vol_note[0]
                vol = ts_vol_note[1]
                note = ts_vol_note[2] if 2 < len(ts_vol_note) else ''
                conn.insert_log(ts, vol, note)
