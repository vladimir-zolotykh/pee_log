#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import datetime
import argparse
import argcomplete
import sqlite3
import parse_date

parser = argparse.ArgumentParser(
    description="Add logs to DB",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('log_file')
parser.add_argument('--verbose', '-v', action='count', default=0)
parser.add_argument(
    '--silence-errors', action='store_true',
    help='''\
        If the input log has a timestamp found in the database, do not
        report this
    ''')
parser.add_argument('--log-db', default='./log_db.db',
                    help='Log database file')


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with open(args.log_file) as log_file:
        with sqlite3.connect(args.log_db) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS pee_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                pee_time TEXT UNIQUE)
            ''')
            hour24 = 0
            for line_no, log_line in enumerate(log_file.readlines()):
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
                    try:
                        conn.execute('''
                            INSERT INTO pee_log (pee_time)
                            VALUES (?)
                        ''', (pee_time, ))
                    except sqlite3.DatabaseError:
                        pass
