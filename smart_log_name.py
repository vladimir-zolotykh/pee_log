#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
from datetime import datetime


def is_log_date(date_str):
    '''
    >>> is_log_date("2024-01-26")
    True
    >>> is_log_date("24/01/26")
    False
    '''
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_log_file(filename):
    '''
    >>> is_log_file("LOG_DIARY/240126.txt")
    True
    '''
    with open(filename) as fd:
        date_str = fd.readlines()[0].strip()
        try:
            datetime.strptime(date_str, "%y/%m/%d")
            return True
        except ValueError:
            return False


def date_to_filename(date_str):
    '''
    >>> date_to_filename("2024-01-26")
    'LOG_DIARY/240126.txt'
    '''
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return os.path.join("LOG_DIARY", date.strftime("%y%m%d") + ".txt")


def smart_log_name(log_str):
    '''
    Returns a standardized log file name based on the input log string.

    Parameters:
    - log_str (str): A string representing a potential log file name
      or date.

    Returns:
    str: The standardized log file name. If no conversion is
    successful, returns the original input.

    - If the input log_str represents an existing file path, it is
      returned unchanged.

    - If the input log_str does not represent an existing file path,
      it is prefixed with "LOG_DIARY/".

    - If the resulting log_name exists and is a valid log file, it is
      returned.

    - If the input log_str represents a valid log date, it is
      converted to a filename, and the resulting log_name is checked.

    >>> smart_log_name("2024-01-24")
    'LOG_DIARY/240124.txt'
    >>> smart_log_name("240124.txt")
    'LOG_DIARY/240124.txt'
    >>> smart_log_name("LOG_DIARY/240126.txt")
    'LOG_DIARY/240126.txt'
    '''

    if os.path.exists(log_str):
        return log_str
    log_name = os.path.join("LOG_DIARY", log_str)
    if os.path.exists(log_name):
        return log_name
    if is_log_date(log_str):
        log_name = date_to_filename(log_str)
        if os.path.exists(log_name) and is_log_file(log_name):
            return log_name
    return log_str          # all convertions fail


if __name__ == '__main__':
    import doctest
    doctest.testmod()
