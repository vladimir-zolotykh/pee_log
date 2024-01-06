#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import functools                # noqa
import itertools
import operator                 # noqa


mins = list(range(24 * 60))


def tick(min, len=20):
    """Return TICK number

    One tick has LEN minuntes. A day has 24 * 60 // LEN TICKS"""

    return min // len


def groupby_hits(mins, len=20):
    """Returns a dict {tick: hits, ...}

    Where TICK is the tick (of an hour) number, HITS - how many logs
    was recorderd within this TICK"""

    return {k: sum(1 for h in g) for k, g
            in itertools.groupby(mins, lambda min: tick(min, len=len))}


def print_hits(mins, len=20):
    for tick_no, num_hits in groupby_hits(mins, len=len).items():
        print('{:3d}: {:3d}'.format(tick_no, num_hits))
