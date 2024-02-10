#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Parse multilog file, e.g., file with many log records like
*** 12/26 ***
0205
0409
...
(the pee_log.txt file).

>>> parse_multilog(pee_sample)
[('12/26', '0205'), ('12/26', '0409'),\
 ('01/09', '0008'), ('01/09', '0158'), ('01/09', '0454'),\
 ('01/14', '0407'), ('01/14', '0726'), ('01/14', '0921')]
"""
import re

pee_sample = """
*** 12/26 ***
0205
0409
*** 01/09 ***
0008
0158
0454
*** 01/14 ***
0407
0726
0921
"""
time_re = re.compile(r'(:?\d{4}.?)')

log_re = re.compile(
    r'\*{3} (\d{2}/\d{2} \*{3}).' + time_re.pattern + r'+',
    re.DOTALL | re.MULTILINE)
date_times_re = re.compile(
    r'\*{3} (?P<date>\d{2}/\d{2}) \*{3}.(?P<times>.+).',
    re.DOTALL | re.MULTILINE)


def parse_multilog(log_str):
    logs = log_re.finditer(log_str)
    result = []
    for log in logs:
        one_log_txt = log.group()
        m = date_times_re.match(one_log_txt)
        log_date, log_times = m.group('date'), m.group('times')
        for log_time in time_re.findall(log_times):
            result.append((log_date, log_time))
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
