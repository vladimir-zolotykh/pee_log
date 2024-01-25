#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Read one day log records.
The file format:
YY/MM/DD
HHMM
HHMM
...

Example usage:
$ python test_log.py LOG_DIARY/240124.txt
LOG_DIARY/240124.txt                    : 23
parse_log_re                            : 23
"""
import argparse
import argcomplete
import parse_log_re

parser = argparse.ArgumentParser(
    description='Testify the input file is a log file',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input_file', help='Log file (.txt) to test')

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    with open(args.input_file) as log_file:
        log_str = log_file.read()
        lines = log_str.count('\n')
        # lines = sum(1 for char in log_str if char == '\n')
        parse_res = parse_log_re.parse_log_re(log_str)
    print(f'{args.input_file:40s}: {lines:2d}\n'
          f'{"parse_log_re":40s}: {1 + len(parse_res[0][1]):2d}')
