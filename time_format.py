#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> to24H(['125', '411', '538', '710', '804', '931', '1050', '1141',\
           '1244', '102', '129', '200', '223', '242', '300', '331',\
           '351', '437', '520', '643', '752', '952'])
['0125', '0411', '0538', '0710', '0804', '0931', '1050', '1141',\
 '1244', '1302', '1329', '1400', '1423', '1442', '1500', '1531',\
 '1551', '1637', '1720', '1843', '1952', '2152'])
"""
from datetime import datetime


def to24H(times: list[str]) -> list[str]:
    times_12_hour: list[str] = times
    times_24_hour: list[str] = []

    for time_str in times_12_hour:
        if len(time_str) <= 3:
            time_str = time_str.zfill(4)
        hour_minute_format = '%I%M'  # %I for 12-hour format hour
        dt = datetime.strptime(time_str, hour_minute_format)
        # Determine if it is AM or PM based on time order in the day
        if (dt.hour < 12 and len(times_24_hour) > 0 and
                int(times_24_hour[-1][:2]) >= 12):
            # Convert to PM if it's after 12:00 PM (since the hour
            # rolls over)
            print(f'{dt = }, {dt.hour = }')
            dt = dt.replace(hour=dt.hour + 12)

        times_24_hour.append(dt.strftime('%H%M'))
    return times_24_hour


def convert_12_to_24_hour_format(
        file_path: str
) -> list[str]:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    date_line = lines[0].strip()
    print(f"Date: {date_line}")

    times_12_hour: list[str] = [line.strip() for line in lines[1:]]
    times_24_hour = list[str] = []

    for time_str in times_12_hour:
        # Ensure time string is 4 digits by padding hour if necessary
        if len(time_str) <= 3:
            # Adds leading zero to make hour always 2 digits (e.g.,
            # '125' -> '0125')
            time_str = time_str.zfill(4)
        hour_minute_format = '%I%M'  # %I for 12-hour format hour
        dt = datetime.strptime(time_str, hour_minute_format)
        # Determine if it is AM or PM based on time order in the day
        if (dt.hour < 12 and len(times_24_hour) > 0 and
                int(times_24_hour[-1][:2]) >= 12):
            # Convert to PM if it's after 12:00 PM (since the hour
            # rolls over)
            dt = dt.replace(hour=dt.hour + 12)

        times_24_hour.append(dt.strftime('%H%M'))
    for time_24 in times_24_hour:
        print(time_24)
    return times_24_hour


if __name__ == '__main__':
    # convert_12_to_24_hour_format("LOG_DIARY/2024-01-18.txt")
    import doctest
    doctest.testmod()
