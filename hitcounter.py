#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> cnt = HitCounter(tick_len=20)
>>> len(cnt.hits)
72
>>> cnt.minute_to_tick(19)
0
>>> cnt.minute_to_tick(20)
1
>>> cnt.time_to_tick_no(0, 19)
0
>>> cnt.time_to_tick_no(0, 20)
1
>>> cnt.time_to_tick_no(1, 20)
4
>>> sample_logs = [                        # in minutes
...     121, 312, 396, 460, 562, 655, 713, 765, 790, 814, 844, 859, 874,
...     886, 901, 915, 943, 965, 995, 1052, 1128, 1183, 1277, 1347, 1433
... ]
>>> cnt.count(sample_logs)
>>> import pprint
>>> pprint.pprint(cnt.hits)
{0: 0,
 1: 0,
 2: 0,
 3: 0,
 4: 0,
 5: 0,
 6: 1,
 7: 0,
 8: 0,
 9: 0,
 10: 0,
 11: 0,
 12: 0,
 13: 0,
 14: 0,
 15: 1,
 16: 0,
 17: 0,
 18: 0,
 19: 1,
 20: 0,
 21: 0,
 22: 0,
 23: 1,
 24: 0,
 25: 0,
 26: 0,
 27: 0,
 28: 1,
 29: 0,
 30: 0,
 31: 0,
 32: 1,
 33: 0,
 34: 0,
 35: 1,
 36: 0,
 37: 0,
 38: 1,
 39: 1,
 40: 1,
 41: 0,
 42: 2,
 43: 1,
 44: 1,
 45: 2,
 46: 0,
 47: 1,
 48: 1,
 49: 1,
 50: 0,
 51: 0,
 52: 1,
 53: 0,
 54: 0,
 55: 0,
 56: 1,
 57: 0,
 58: 0,
 59: 1,
 60: 0,
 61: 0,
 62: 0,
 63: 1,
 64: 0,
 65: 0,
 66: 0,
 67: 1,
 68: 0,
 69: 0,
 70: 0,
 71: 1}
>>> list_cnt_expected = [
...    0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0,
...    0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 2, 1,
...    1, 2, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0,
...    0, 1, 0, 0, 0, 1
... ]
>>> assert list(cnt) == list_cnt_expected
"""

import math
TICK_LEN = 20
sample_logs = [                        # in minutes
    121, 312, 396, 460, 562, 655, 713, 765, 790, 814, 844, 859, 874,
    886, 901, 915, 943, 965, 995, 1052, 1128, 1183, 1277, 1347, 1433
]


class HitCounter:
    tick_len = TICK_LEN

    def __init__(self, tick_len=TICK_LEN):
        """Initialize self.hits"""

        self.hits = {self.minute_to_tick(minute): 0
                     for minute in range(24 * 60)}

    def __iter__(self):
        for tick_no in self.hits:
            yield self.hits[tick_no]

    def minute_to_tick(self, minute):
        """Convert MINUTE to TICK number"""

        return minute // self.tick_len

    def count(self, logs):
        for minute in logs:
            self.hits[self.minute_to_tick(minute)] += 1

    def time_to_tick_no(self, hour, minute):
        """Convert HOUR, MINUTE to TICK number"""

        return (hour * 60 + minute) // self.tick_len


if __name__ == '__main__':
    import doctest
    doctest.testmod()
