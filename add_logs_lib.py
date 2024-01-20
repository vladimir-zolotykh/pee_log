#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> con = connect_pee()
>>> pee_log_16 = '''*** 01/16 ***\\n40\\n300\\n'''
>>> insert_pee(con, *pee_log_16.split('\\n'))
>>> select_pee(con)
[('2023-01-16 04:00:00',), ('2023-01-16 15:00:00',)]
"""
import datetime
import sqlite3
import parse_date


class ConnectionPee(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def make_tables(self):
        self.execute('''
            CREATE TABLE IF NOT EXISTS pee_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
            pee_time TEXT UNIQUE)
        ''')

    def insert_pee(self, pee_time):
        try:
            self.execute('''
                INSERT INTO pee_log (pee_time)
                VALUES (?)
            ''', (pee_time, ))
        except sqlite3.DatabaseError:
            pass

    def select_pee(self):
        pass


def connect_pee(db_file=':memory:'):
    return sqlite3.connect(db_file, factory=ConnectionPee)


def insert_pee(con, *lines):
    con.make_tables()
    hour24 = 0
    for line_no, log_line in enumerate(lines):
        line = log_line.rstrip()
        if not line:
            continue
        if log_line.startswith('***'):
            hour24 = 0
            year, month, day = parse_date.parse_date(line)
        else:
            if len(line) < 4:
                line = '0' + line
            hour, minute = int(line[:2]), int(line[2:])
            if hour < hour24:
                hour += 12
            hour24 = hour
            pee_time = datetime.datetime(year, month, day,
                                         hour24, minute)
            con.insert_pee(pee_time)


def select_pee(con):
    cur = con.cursor()
    cur.execute("""
        SELECT pee_time
        FROM pee_log
    """)
    return cur.fetchall()


def close_pee(con):
    con.commit()
    con.close()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
