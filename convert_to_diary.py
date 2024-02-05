#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Convert old pee log file (with *** 01/14 *** dates ; no volume or note
fields) to LOG_DIARY .txt file)

>>> times = ["300", "502", "631", "711", "818", "1054", "1243", \
    "1259", "116", "141", "209", "231", "249", "313", "344", "416", \
    "520", "714", "906", "1112", "1150"]
>>> convert_to_24h(times)
['0300AM', '0502AM', '0631AM', '0711AM', '0818AM', '1054AM', '1243AM',
'1259AM', '0116PM', '0141PM', '0209PM', '0231PM', '0249PM', '0313PM',
'0344PM', '0416PM', '0520PM', '0714PM', '0906PM', '1112PM', '1150PM']
"""
from datetime import datetime
import parse_date


def convert_to_24h(time_strs):
    def add_leading0(time_strs):
        return [f"{t:0>4s}" for t in time_strs]

    def find_midday_index(time_strs):
        t1 = datetime.strptime(time_strs[0], "%H%M")
        for i, t in enumerate(time_strs):
            t2 = datetime.strptime(t, "%H%M")
            if t2 < t1:
                return i
            t1 = t2

    def convert_to_12h(time_strs, midday_index):
        # [t + ("AM" if i < midday_index else "PM")
        #  for i, t in enumerate(time_strs)]

        res = []
        for i, t in enumerate(time_strs):
            res.append(t + ("AM" if i < midday_index else "PM"))
        return res

    time_strs = add_leading0(time_strs)
    mdi = find_midday_index(time_strs)
    time_strs = convert_to_12h(time_strs, mdi)
    # return [datetime.strptime(t, "%I%M%p") for t in time_strs]
    return time_strs


def convert_to_diary(old_log):
    with open(old_log) as fd:
        lines = convert_to_24h(fd.readlines())
        for line_no, log_line in enumerate(lines):
            line = log_line.rstrip()
            if not line:
                continue
            if log_line.startswith('***'):
                hour24 = 0
                year, month, day = parse_date.parse_date(line)
            else:
                if len(line) < 4:
                    line = '0' + line
                hour, minute = int(line[:2]), int(line[2:])
                if hour < hour24:
                    hour += 12
                hour24 = hour
                pee_time = datetime.datetime(year, month, day,
                                             hour24, minute)
                print(pee_time)

        pass


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
