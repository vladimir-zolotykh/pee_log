#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> input_string = '''
... 24/01/23
... 0232
... 0840
... 1044 224
... 1132 308
... 1725
... 1840'''
>>> parse_log_re(input_string)
[('24/01/23', ['0232', '0840', '1044 224', '1132 308', '1725', '1840'])]
"""
import re
import datetime

def parse_log_re(log_str):
    """
    Parse log (all timestamps of one day) file

    Example:
    >>> input_string = '''24/01/23
    ... 0232
    ... 0840
    ... 1044 224
    ... 1132 308
    ... 1725'''
    >>> parse_log_re(input_string)
    [('24/01/23', ['0232', '0840', '1044 224', '1132 308', '1725'])]

    """

    full_log_re = re.compile(r'^(\d{2}/\d{2}/\d{2})\s*(.*)$',
                             re.DOTALL | re.MULTILINE)
    timestamp_re = re.compile(r'^\d{4}(?:[ \t]\d+)?$', re.MULTILINE)
    matches = full_log_re.finditer(log_str)
    result = []
    for match in matches:
        date, rest_of_log = match.groups()
        timestamps = timestamp_re.findall(rest_of_log)
        result.append((date, timestamps))
    return result


def log_to_timestamps(date_str, *time_vol_list):
    date = datetime.datetime.strptime(date_str, '%y/%m/%d')
    result = []
    for time_vol in time_vol_list:
        time_str, vol_str = (time_vol.split(maxsplit=1)
                             if len(time_vol.split()) > 1 else (time_vol, ''))
        time = datetime.strptime(time_str, '%H%M')
        timestamp = datetime.combine(date.date(), time.time())
        result.append((timestamp, int(vol_str) if vol_str else ''))
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
