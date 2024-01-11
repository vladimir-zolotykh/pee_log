#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import sqlite3
import datetime
from pprint import pprint
import matplotlib.pyplot as plt
from hitcounter import HitCounter


parser = argparse.ArgumentParser(
    description='Plot log samples',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--db-file', help='Db file', default='pee_log.db')
parser.add_argument(
    '--date', help='Plot samples of that date',
    type=datetime.date.fromisoformat, default='2023-12-30')
parser.add_argument(
    '--tick-len', help="A day is divided to TICKS (in minutes)",
    type=int, choices=[15, 20, 30], default=20)


def time_to_minute(row, fmt='%Y-%m-%d %H:%M:%S'):
    dt = datetime.datetime.strptime(row[0], fmt)
    return dt.hour * 60 + dt.minute


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    num_ticks = 24 * 60 // args.tick_len
    hit_cnt = HitCounter(args.tick_len)
    with sqlite3.connect(f"file:{args.db_file}?mode=ro",  uri=True) as conn:
        cursor = conn.cursor()
        query = """
            SELECT pee_time, strftime('%Y-%m-%d', pee_time) as pee_day
            FROM pee_log
            WHERE pee_day = ?
        """
        cursor.execute(query, (args.date.strftime('%Y-%m-%d'),))
        rows = cursor.fetchall()
        mins_list = [time_to_minute(row) for row in rows]
        print(f'{len(mins_list) = }')
        hit_cnt.count(mins_list)
        x, y = zip(*[(tick_no, hum_hits)
                     for tick_no, hum_hits in hit_cnt.hits.items()])
        plt.bar(x, y, color='blue', alpha=0.7)
        plt.xlabel(f'{args.tick_len} mins')
        plt.ylabel('Pees')
        plt.title(f'{args.date} ({len(x)})')
        plt.show()
