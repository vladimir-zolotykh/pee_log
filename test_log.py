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


def test_log(input_file):
    with open(input_file) as fd:
        log_str = fd.read()
        lines = log_str.count('\n')
        parse_res = parse_log_re.parse_log_re(log_str)
    # print(f'{input_file:40s}: {lines:2d}\n'
    #       f'{"parse_log_re":40s}: {1 + len(parse_res[0][1]):2d}')
    assert lines == 1 + len(parse_res[0][1])


parser = argparse.ArgumentParser(
    description='Testify the input file is a log file',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input_file', help='Log file (.txt) to test')

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    test_log(args.input_file)
