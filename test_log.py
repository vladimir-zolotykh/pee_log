#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Read one day log records.
The file format:
YY/MM/DD
HHMM [VOLUME] [NOTE]
...

Example usage:
$ for f in LOG_DIARY/*.txt; do diary.py test $f; done
"""
import argparse
import argcomplete
import parse_log_re
from validate_sample import validate
from time_format import to24H


def test_log(input_file: str) -> bool:
    """Return True to continue scanning

    False to abort scanning
    """
    with open(input_file) as fd:
        log_str = fd.read()
        num_lines = log_str.count('\n')
        # parse_res = parse_log_re.parse_log_re(log_str)
        parse_res = parse_log_re.parse_log_re24h(log_str)
        times0 = parse_res[0][1]
        print(f'{times0 = }')
        times24H = to24H(times0)
        # print(f'{times_24H = }')
        # in the next line `input_file' is needed for error messages

        # if not validate(parse_res[0][1], input_file, verbose=False):
        if not validate(times24H, input_file, verbose=False):
            return True
    if num_lines == 1 + len(parse_res[0][1]):
        print(f'"{input_file}" OK')
        return True
    else:
        print(f'{input_file:40s}: {num_lines:2d}\n'
              f'{"parse_log_re":40s}: {1 + len(parse_res[0][1]):2d}\n'
              f'Likely {input_file} has empty lines(s) in the end')
        return False


parser = argparse.ArgumentParser(
    description='Testify the input file is a log file',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input_file', nargs='+', help='Log file (.txt) to test')

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    for log_file in args.input_file:
        test_log(log_file)
