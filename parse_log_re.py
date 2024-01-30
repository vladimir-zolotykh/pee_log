#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> input_string = '24/01/23\\n0232\\n0840\\n1044 224\\n1132 308\\n1725\\n1840'
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
    ... 1725
    ... 1840'''
    >>> parse_log_re(input_string)
    [('24/01/23', ['0232', '0840', '1044 224', '1132 308', '1725', '1840'])]

    """

    full_log_re = re.compile(r'^(\d{2}/\d{2}/\d{2})\s*(.*)$',
                             re.DOTALL | re.MULTILINE)
    timestamp_re = re.compile(r'^\d{4}(?:[ \t]\d+)?(?:[ \t]\w+)?$',
                              re.MULTILINE)
    matches = full_log_re.finditer(log_str)
    result = []
    for match in matches:
        date, rest = match.groups()
        timestamps = timestamp_re.findall(rest)
        result.append((date, timestamps))
    return result


def log_to_timestamps(date_str, *time_vol_list):
    """

    Example:
    >>> input_string = '''24/01/23
    ... 0232
    ... 0840
    ... 1044 224
    ... 1132 308
    ... 1725
    ... 1840'''
    >>> parse_res = parse_log_re(input_string)
    >>> parse_res
    [('24/01/23', ['0232', '0840', '1044 224', '1132 308', '1725', '1840'])]
    >>> log_to_timestamps(parse_res[0][0], *parse_res[0][1])
    [(datetime.datetime(2024, 1, 23, 2, 32), (0, '')),
     (datetime.datetime(2024, 1, 23, 8, 40), (0, '')),
     (datetime.datetime(2024, 1, 23, 10, 44), (224, '')),
     (datetime.datetime(2024, 1, 23, 11, 32), (308, '')),
     (datetime.datetime(2024, 1, 23, 17, 25), (0, '')),
     (datetime.datetime(2024, 1, 23, 18, 40), (0, ''))]
    >>> input_string = '''24/01/27
    ... 0730
    ... 0919 207 Creatine
    ... 1016 Piracetam'''
    >>> parse_res = parse_log_re(input_string)
    >>> parse_res
    [('24/01/27', ['0730', '0919 207 Creatine', '1016 Piracetam'])]
    >>> log_to_timestamps(parse_res[0][0], *parse_res[0][1])
    [(datetime.datetime(2024, 1, 27, 7, 30), (0, '')),
     (datetime.datetime(2024, 1, 27, 9, 19), (207, 'Creatine')),
     (datetime.datetime(2024, 1, 27, 10, 16), (0, 'Piracetam'))]
    """

    date = datetime.datetime.strptime(date_str, '%y/%m/%d')
    result = []
    for time_vol in time_vol_list:
        time_str, vol_str = (time_vol.split(maxsplit=1)
                             if len(time_vol.split()) > 1 else (time_vol, ''))
        time = datetime.datetime.strptime(time_str, '%H%M')
        timestamp = datetime.datetime.combine(date.date(), time.time())

        def get_vol_note(vol_str):
            vol, note = 0, ''
            for s in vol_str.split(maxsplit=1):
                if s.isdecimal():
                    vol = int(s)
                else:
                    note = s
            return vol, note

        result.append((timestamp, get_vol_note(vol_str)))
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
