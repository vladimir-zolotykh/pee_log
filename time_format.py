#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> to24H(['125', '411', '538', '710', '804', '931', '1050', '1141',\
           '1244', '102', '129', '200', '223', '242', '300', '331',\
           '351', '437', '520', '643', '752', '952'])
['0125', '0411', '0538', '0710', '0804', '0931', '1050', '1141',\
 '1244', '1302', '1329', '1400', '1423', '1442', '1500', '1531',\
 '1551', '1637', '1720', '1843', '1952', '2152']
"""
from datetime import datetime


def to24H(times: list[str]) -> list[str]:
    times24H: list[str] = []
    sfx = 'AM'
    dt: datetime = datetime.strptime('1200am', '%I%M%p')
    _times: list[str] = []
    for time_str in times:
        # make times str 4 digits lenght
        if len(time_str) <= 3:
            time_str = time_str.zfill(4)
        _times.append(time_str)
    times = _times
    for time_str in times:
        # if len(time_str) <= 3:
        #     time_str = time_str.zfill(4)
        time_str += sfx
        format = '%I%M%p'
        dt_prev: datetime = dt
        try:
            dt = datetime.strptime(time_str, format)
        except ValueError:
            # Already in 24H format?
            return times
        if dt.hour < dt_prev.hour:
            sfx = 'PM'
            time_str = time_str[:-2] + sfx
            dt = datetime.strptime(time_str, format)
        times24H.append(dt.strftime('%H%M'))
    return times24H


if __name__ == '__main__':
    import doctest
    doctest.testmod()
