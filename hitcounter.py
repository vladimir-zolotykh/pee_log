#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import math
TICK_LEN = 20
hits = {}                       # num of logs per TICK interval
# LOGS - logs[0] == 121 means that at the minute 121 (0-based) there's
# a log record in the DB
logs = [                        # in minutes
    121, 312, 396, 460, 562, 655, 713, 765, 790, 814, 844, 859, 874,
    886, 901, 915, 943, 965, 995, 1052, 1128, 1183, 1277, 1347, 1433
]


def time_to_tick_no(hour, minute, tick_len=TICK_LEN):
    """Convert HOUR, MINUTE to TICK number"""

    return (hour * 60 + minute) // tick_len


def minute_to_tick(minute, tick_len=TICK_LEN):
    """Convert MINUTE to TICK number"""

    return minute // tick_len


def initialize_hits(tick_len=TICK_LEN):
    for tick_no in range(math.ceil(24 * 60 / tick_len)):
        hits[tick_no] = 0


def count_hits():
    for s in logs:
        hits[minute_to_tick(s)] += 1
