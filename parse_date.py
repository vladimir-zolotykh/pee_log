#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re


class ParseError(Exception):
    pass


def parse_date(date_str, year=2023):
    """
>>> parse_date('*** 12/30 ***')
(2023, 12, 30)
>>> parse_date('*** 23/12/30 ***')
(2023, 12, 30)
>>>
    """
    m = re.match(
        r'^\*{3}\s+(?:(?P<year>[\d]+)/)?'
        r'(?P<month>[\d]+)/(?P<day>[\d]+)\s+\*{3}$', date_str)
    if not m:
        raise ParseError(f"{date_str}: Invalid date")
    _year = m.group('year')
    if _year:
        if not _year.startswith('20'):
            _year = '20' + _year
        year = _year
    return tuple(map(int, (year, m.group('month'), m.group('day'))))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
