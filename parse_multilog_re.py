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
import argparse
import argcomplete
from datetime import datetime
from typing import NamedTuple, Optional

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


class LogEntry(NamedTuple):
    time: Optional[datetime.time] = None
    volume: Optional[int] = None
    note: Optional[str] = None
    label: Optional[str] = None


class InvalidEventError(Exception):
    pass


class LogState:
    EVENTS = ('date_event', 'log_event')
    STATES = {
        'idle_state': {
            'date_event': 'collect_state'},
        'collect_state': {
            'date_event': 'collect_state', 'log_event': 'collect_state'}}

    def __init__(self, init_state='idle_state'):
        assert init_state in self.STATES
        self.state = init_state

    def transition(self, event):
        assert event in self.EVENTS
        try:
            new_state = self.STATES[self.state][event]
        except KeyError as e:
            print(f'*** transition {self.state = }, {event = }, {e = }')
            raise
        if new_state == self.state:
            return
        self.state = new_state


def convert_to_diary(log_file):
    log_state = LogState()
    log_data = []               # collected logs (tuples)
    log_day = None

    # def set_date(*args):
    #     print(f'*** set_date {args = }')

    def get_log_day(date_match: re.Match) -> datetime.date:
        year, month, day = date_match.groups()
        if not year:
            year = datetime.now().year
        return datetime(*map(int, (year, month, day))).date()

    def save_log(data):
        print(f'*** save_log {data = }')

    def clear_log():
        nonlocal log_data, log_day
        log_data = []
        log_day = None

    with open(log_file) as log_fd:
        log_state = LogState(init_state='idle_state')
        for line_no, line_str in enumerate(log_fd.readlines(), start=1):
            date_match = date_re.match(line_str)
            log_match = log_re.match(line_str)
            if date_match:
                # year, month, day = date_match.groups()
                log_day = get_log_day(date_match)
                if log_state.state == 'collect_state':
                    save_log(log_data)
                    log_data = []
                    # 'collect_state' remains active
                elif log_state.state == 'idle_state':
                    log_state.transition('date_event')  # -> 'collect_state'
            elif log_match:
                time, *rest = log_match.groups()[1:]
                if time:
                    time = datetime.strptime(time, '%H%M')
                log_entry = LogEntry(time, *rest)
                log_data.append((log_day, log_entry))
                # 'collect_state' remains active
            else:
                raise InvalidEventError(line_str)
        if log_data:
            save_log(log_data)
            log_data = []


parser = argparse.ArgumentParser(
    description='''
parse_multilog_re: run doctest, dbg, or parse log file(s)''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--pdb', help='Call pdb.set_trace() first', action='store_true')
parser.add_argument(
    '--testmod', help='''\
Call doctest.testmod(), --pdb option and log files if supplied are ignored''',
    action='store_true')
parser.add_argument(
    'log_files', help='Log files to parse', nargs='*')


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.testmod:
        import doctest
        doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
    else:
        if args.pdb:
            import pdb
            pdb.set_trace()
        convert_to_diary(args.log_files[0])
