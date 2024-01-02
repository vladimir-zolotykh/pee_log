#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import sqlite3
import datetime
import matplotlib.pyplot as plt


def count_1hour_logs(req_dt: datetime.datetime):
    """Count all the logs recorded at the hour REQ_DT.hour hour"""

    return len(list(filter(
        lambda d: d.hour == req_dt.hour,
        (datetime.datetime.strptime(d[0], '%Y-%m-%d %H:%M:%S')
         for d in conn.execute('SELECT pee_time FROM pee_log')))))


parser = argparse.ArgumentParser(
    description='Plot log samples',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--db-file', help='Db file', default='pee_log.db')
parser.add_argument(
    '--date', help='Plot samples of that date',
    default=datetime.date.fromisoformat('2023-12-31'))

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with sqlite3.connect(f"file:{args.db_file}?mode=ro",  uri=True) as conn:
        x = list(range(24))
        y = [0] * 24
        for h in range(24):
            time = datetime.time(h, 0, 0)
            y[h] = count_1hour_logs(datetime.datetime.combine(args.date, time))
        plt.plot(x, y, label=args.date)
        plt.xlabel('Hours')
        plt.ylabel('Pee')
        plt.title('Pee')
        plt.legend()
        plt.show()
