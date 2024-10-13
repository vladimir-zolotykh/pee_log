#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import io
from typing import Dict
import csv
LOG_DIARY_DIR = './LOG_DIARY'
CONFIG_FILENAME = 'log_diary.csv'
# Example of the config date.
# If the file is present in the CONFIG_DATA, e.g., 2024-05-24.txt, it
# shall be added to the db with the command:
# $ python wclog.py add --pee-optional 2024-05-24.txt

CONFIG_DATA = [
    ['2024-05-21.txt', '--pee-optional'],
    ['2024-05-24.txt', '--pee-optional'],
    ['2024-05-25.txt', '--pee-optional'],
    ['2024-05-26.txt', '--pee-optional']]


def write_config(config_filename=CONFIG_FILENAME):
    """Write the LOG_DIARY config.csv

    A line example:
    2024-05-21.txt --pee-optional
    """

    with open(os.path.join(LOG_DIARY_DIR, config_filename),
              mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        writer.writerows(CONFIG_DATA)


def read_config(config_filename=CONFIG_FILENAME) -> Dict[str, str]:
    """Read the LOG_DIARY config.csv

    Return it as a dict. The dict item example:
    '2024-05-21.txt': '--pee-optional'
    """

    open_kwargs: dict[str, str] = {'newline': ''}
    fd: io.TextIOBase
    try:
        fd = open(os.path.join(LOG_DIARY_DIR, config_filename), **open_kwargs)
    except FileNotFoundError:
        fd = open(config_filename, **open_kwargs)
    with fd as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        config_dict: Dict[str, str] = {}
        for row in reader:
            config_dict[row[0]] = row[1]
        return config_dict
