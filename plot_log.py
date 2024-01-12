#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import sqlite3
import datetime
import matplotlib.pyplot as plt
from hitcounter import HitCounter
bar_index = 0


class Formatter:
    def __init__(self, ax, tick_len=None):
        self.tick_len = tick_len if tick_len else 20  # mins
        self.ax = ax

    def format_coord(self, x, y):
        """Convert X to HH:MM"""
        global bar_index
        x2 = bar_index if bar_index else 0
        hour, minute = divmod(int(x2) * self.tick_len, 60)
        return f'x={x:.2f} x2={x2:.2f} ({hour:02d}:{minute:02d})'


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
        bars = ax.bar(x, y, color='blue', alpha=0.7)

        def hover(event):
            global bar_index
            bar_index = None
            for bar in bars:
                contains, _ = bar.contains(event)
                if contains:
                    bar_index = bars.index(bar)
                    # print(f'Hovered over Bar {bar_index + 1}')

        formatter = Formatter(ax, tick_len=args.tick_len)
        ax.format_coord = formatter.format_coord
        plt.xlabel(f'{args.tick_len} min interval')
        plt.ylabel('Pees')
        plt.title(f'{args.date} ({len(x)})')
        fig.canvas.mpl_connect('motion_notify_event', hover)
        plt.show()
