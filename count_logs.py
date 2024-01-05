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


def print_hits(len=20):
    for k, g in itertools.groupby(mins, lambda min: tick(min, len=len)):
        # print(f'{k}: {len(list(g))}')
        print('{:3d}: {:3d}'.format(k, sum(1 for h in g)))
