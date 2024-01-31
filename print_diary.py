#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Print records from pee_diary.db database
"""
import argparse
import argcomplete
import sqlite3
import datetime


class ConnectionDiary(sqlite3.Connection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def select_logs(self, req_date):
        return self.execute('''
            SELECT pee_time, volume, note
            FROM pee_log
            WHERE strftime('%Y-%m-%d', pee_time) = ?
        ''', (datetime.datetime.strftime(req_date, '%Y-%m-%d'), ))


parser = argparse.ArgumentParser(
    description="Print records from pee_diary.db database",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--log-db', default='./pee_diary.db',
                    help='Log database file')
parser.add_argument('--verbose', '-v', action='count', default=0)


def date_type(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')


def print_diary(req_date, log_db=None):
    log_db = "./pee_diary.db" if log_db is None else log_db
    with sqlite3.connect(log_db, factory=ConnectionDiary) as conn:
        for row in conn.select_logs(req_date):
            print(row)


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print_diary(args.log_db)
