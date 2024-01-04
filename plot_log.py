#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import sqlite3
import datetime
import matplotlib.pyplot as plt


def count_1hour_logs(conn, req_dt: datetime.datetime):
    """Count all the logs recorded at the REQ_DT.hour"""
    query, fmt = 'SELECT pee_time FROM pee_log', '%Y-%m-%d %H:%M:%S'
    return sum(1 for row in conn.execute(query)
               if datetime.datetime.strptime(row[0], fmt).hour == req_dt.hour)


parser = argparse.ArgumentParser(
    description='Plot log samples',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--db-file', help='Db file', default='pee_log.db')
parser.add_argument(
    '--date', help='Plot samples of that date',
    type=datetime.date.fromisoformat, default='2023-12-30')


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with sqlite3.connect(f"file:{args.db_file}?mode=ro",  uri=True) as conn:
        x = list(range(24))
        y = [0] * 24
        for h in range(24):
            time = datetime.time(h, 0, 0)
            y[h] = count_1hour_logs(conn,
                                    datetime.datetime.combine(args.date, time))
        plt.bar(range(24), y, color='blue', alpha=0.7)
        plt.xlabel('Hour of the day')
        plt.ylabel('Pees')
        plt.title(f'Pee Log {args.date}')
        plt.show()
