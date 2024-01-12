#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import sqlite3
import datetime
import matplotlib.pyplot as plt
from hitcounter import HitCounter


class Formatter:
    def __init__(self, ax):
        self.ax = ax

    def format_coord(self, x, y):
        return f'Custom X: {x:.2f}, Custom Y: {y:.2f}'


parser = argparse.ArgumentParser(
    description='Plot log samples',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--db-file', help='Db file', default='pee_log.db')
parser.add_argument(
    '--date', help='Plot samples of that date',
    type=datetime.date.fromisoformat, default='2023-12-30')
parser.add_argument(
    '--tick-len', help="A day is divided to TICKS (in minutes)",
    type=int, choices=[5, 10, 15, 20, 30, 60], default=20)


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
        hit_cnt.count(mins_list)
        x, y = zip(*[(tick_no, hum_hits)
                     for tick_no, hum_hits in hit_cnt.hits.items()])
        fig, ax = plt.subplots()
        ax.bar(x, y, color='blue', alpha=0.7)
        formatter = Formatter(ax)
        ax.format_coord = formatter.format_coord
        plt.xlabel(f'{args.tick_len} min interval')
        plt.ylabel('Pees')
        plt.title(f'{args.date} ({len(x)})')
        plt.show()
