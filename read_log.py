#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import sqlite3


parser = argparse.ArgumentParser(
    description='Insert into db',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--log-file', help='Log file path', default='pee_log.txt')
parser.add_argument('--db-file', help='Db file', default='pee_log.db')

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with sqlite3.connect(args.db_file) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pee_log (
                id INTEGER PRIMARY KEY,
                pee_time TEXT)
        ''')
        with open(args.log_file) as log_file:
            for line_no, line_str in enumerate(log_file.readlines()):
                line = line_str.rstrip()
                if not line:
                    continue
                if line_str.startswith('***'):
                    pass
                else:
                    # print(f'{line_no = }, {line = }')
                    conn.execute('''
                        INSERT INTO pee_log (pee_time)
                        VALUES (?)
                    ''', (line, ))
