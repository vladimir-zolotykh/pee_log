#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Parse multilog file, e.g., file with many log records like
*** 12/26 ***
0205
0409
...
(the pee_log.txt file).

>>> parse_multilog(pee_sample)
[('12/26', '0205'), ('12/26', '0409'),\
 ('01/09', '0008'), ('01/09', '0158'), ('01/09', '0454'),\
 ('01/14', '0407'), ('01/14', '0726'), ('01/14', '0921')]
"""
import re

pee_sample = """*** 12/26 ***
0205
0409
*** 01/09 ***
0008
0158
0454
*** 01/14 ***
0407
0726
0921"""

time_re = re.compile(r'(:?\d{4}.?)')
log_re = re.compile(
    r'\*{3} (\d{2}/\d{2} \*{3}).' + time_re.pattern + r'+',
    re.DOTALL | re.MULTILINE)
date_times_re = re.compile(
    r'\*{3} (?P<date>\d{2}/\d{2}) \*{3}.(?P<times>.+)',
    re.DOTALL | re.MULTILINE)


def parse_multilog(log_str):
    logs = log_re.finditer(log_str)
    result = []
    for log in logs:
        one_log_txt = log.group()
        m = date_times_re.match(one_log_txt)
        log_date, log_times = m.group('date'), m.group('times')
        for log_time in time_re.findall(log_times):
            result.append((log_date, log_time))
    return result


# date_re example "01/27"
date_re = re.compile(r'''
    \*{3}\s+
    (?:(?P<year>\d{2,4})[/-])?  # 2024 or 24
    (?P<month>\d{2})[/-]
    (?P<date>\d{2})
    \s+\*{3}
''', re.VERBOSE)
# log_re example "1234 121 Creatine"
log_re = re.compile(r'''
    ((?P<time>\d{3,4})          # 0214 or 214 (2:14 AM)
    (?:\s+(?P<volume>\d+))?
    (?:\s+(?P<note>\w+))?)
    |(?P<label>\w+)             # standalone label, e.g., "stool"
''', re.VERBOSE)


class LogState:
    EVENTS = ('date', 'log', 'eof')
    STATES = {
        'idle': {'date': 'collect', 'eof': 'idle'},
        'collect': {'log': 'collect', 'date': 'write', 'eof': 'write'},
        'write': {'date': 'collect', 'eof': 'terminate'},
        'terminate': None}

    def __init__(self, init_state='idle'):
        self.state = init_state

    def transition(self, event):
        if event in self.EVENTS:
            new_state = self.STATES[self.state][event]
            if new_state == self.state:
                return
            self.state = new_state


def convert_to_diary(log_file):
    log_state = LogState()
    log_data = []               # collected logs (tuples)
    log_date = None

    def set_date(*args):
        print(f'*** set_date {args = }')

    def save_log(data):
        print(f'*** save_log {data = }')

    def clear_log():
        nonlocal log_data, log_date
        log_data = []
        log_date = None

    with open(log_file) as log_fd:
        for line_no, line_str in enumerate(log_fd.readlines(), start=1):
            date_match = date_re.match(line_str)
            if date_match:
                if log_state.state == 'collect':
                    save_log(log_data)
                    clear_log()
                    log_state.transition('idle')
                else:
                    log_state.transition('collect')
                    set_date(date_match.groups())
                continue
            log_match = log_re.match(line_str)
            if log_match:
                log_data.append((log_date, *log_match.groups()))
                continue
        if log_data:
            save_log(log_data)
            clear_log()
            log_state.transition('idle')


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
    convert_to_diary('pee_log.txt')
