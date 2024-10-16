#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re


def is_valid_time2(time_str: str) -> bool:
    """
    Validate the time string format (HHMM) and ensure it's within 0000-2359.
    """
    m: re.Match = re.match(r'^(?P<hh>\d{2})(?P<mm>\d{2})$', time_str)
    if m:
        hour: int = int(m[1])
        minute: int = int(m[2])
        return 0 <= hour < 24 and 0 <= minute < 60
    return False


def is_valid_time(time_str: str) -> bool:
    """
    Validate the time string format (HHMM) and ensure it's within 0000-2359.
    """
    if re.match(r'^\d{4}$', time_str):
        hour = int(time_str[:2])
        minute = int(time_str[2:])
        return 0 <= hour < 24 and 0 <= minute < 60
    return False


def check_ascending_order2(times: list) -> bool:
    pass


def check_ascending_order(times: list) -> bool:
    """
    Check if times are in strictly ascending order.
    """
    return all(times[i] < times[i + 1] for i in range(len(times) - 1))


def main(file_path: str):
    """
    Read the times from the file and perform validation and ordering checks.
    """
    with open(file_path, 'r') as file:
        times = [line.strip() for line in file if line.strip()]
    times = times[1:]

    # Validate times
    invalid_times = [time for time in times if not is_valid_time(time)]
    if invalid_times:
        print(f"Invalid times found: {invalid_times}")
        return

    # Check if times are in strictly ascending order
    if check_ascending_order(times):
        print("All times are valid and in strictly ascending order.")
    else:
        print("Times are not in strictly ascending order.")


if __name__ == '__main__':
    file_path = 'LOG_DIARY/2024-09-21.txt'
    main(file_path)
