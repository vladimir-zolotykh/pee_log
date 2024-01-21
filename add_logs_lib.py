#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> con = connect_pee()
>>> pee_log_14 = '''*** 2024/01/14 ***\\n1708\\n1847\\n'''
>>> insert_pee(con, *pee_log_14.split('\\n'))
>>> select_pee(con)
[('2024-01-14 17:08:00',), ('2024-01-14 18:47:00',)]
>>> con.close()
>>> con = connect_pee()
>>> # Check that crossing the midday is noticed
>>> pee_log_15 = '*** 2024/01/15 ***\\n1256\\n120\\n'
>>> insert_pee(con, *pee_log_15.split('\\n'))
>>> select_pee(con)
[('2024-01-15 12:56:00',), ('2024-01-15 13:20:00',)]
>>> con.close()
>>> con = connect_pee()
>>> # Check times aroung midnight
>>> pee_log_16 = '*** 2024/01/16 ***\\n1200\\n1250\\n110\\n'
>>> insert_pee(con, *pee_log_16.split('\\n'))
>>> select_pee(con)
[('2024-01-16 12:00:00',), ('2024-01-16 12:50:00',), ('2024-01-16 01:10:00',)]
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
