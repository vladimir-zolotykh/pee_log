#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import re


def parse_log_re(input_string):
    """
    Parse log (all timestamps of one day) file
    """

    full_pattern = re.compile(r'^(\d{2}/\d{2}/\d{2})\s*(.*)$',
                              re.DOTALL | re.MULTILINE)
    second_pattern = re.compile(r'^\d{4}(?:[ \t]\d+)?$', re.MULTILINE)
    matches = full_pattern.finditer(input_string)
    result = []
    for match in matches:
        date, rest_of_line = match.groups()
        second_matches = second_pattern.findall(rest_of_line)
        result.append((date, second_matches))
    return result


# Example usage
input_string = """
24/01/23
0232
0840
1044 224
1132 308
1725
1840"""

result = parse_log_re(input_string)
print(result)
