#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import csv
CONFIG_FILENAME = 'log_diary.csv'
CONFIG_DATA = [
    {'log_filename': '2024-05-21.txt', 'options': '--pee-optional'},
    {'log_filename': '2024-05-24.txt', 'options': '--pee-optional'},
    {'log_filename': '2024-05-25.txt', 'options': '--pee-optional'},
    {'log_filename': '2024-05-26.txt', 'options': '--pee-optional'}
]


def write_config():
    with open(CONFIG_FILENAME, mode='w', newline='') as csvfile:
        fieldnames = ['log_filename', 'options']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(CONFIG_DATA)


def read_config():
    with open(CONFIG_FILENAME, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        print(list(reader))
        # for row in reader:
        #     print(row['log_filename'], row['options'])
