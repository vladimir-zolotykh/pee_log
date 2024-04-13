#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import sys
import re
import glob
import argparse
import shutil
from datetime import datetime
import argcomplete
from sampletag_re import logrecords_generator

parser = argparse.ArgumentParser(
    prog='scan_logfiles.py',
    description='Scan/operate on logfiles',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--logdir', default='./LOG_DIARY',
    help='The directory with YYYY-MM-DD.txt logfiles')
subparsers = parser.add_subparsers(
    # description='Operate on LOG_DIARY dir',
    dest='command', title=f'{sys.argv[0]} commands')
parser_2400 = subparsers.add_parser(
    'fix2400', help='Replace 2400 with the valid time stamp')
parser_2400.add_argument(
    'logfiles', nargs='+',
    help='The .txt file (e.g., LOG_DIARY/2024-03-15.txt)')
parser_scan = subparsers.add_parser(
    'scan',
    help='Scan LOG_DIARY; print the requested properties')
parser_scan.add_argument(
    'property', nargs='+',
    choices=['has_tags', 'tags_count', 'has_volume', 'has_note'],
    help="""
Usage: scan_logfiles scan has_volume Print the log file names that
has records with volume field > 0""")
parser_scan.add_argument(
    '--count', type=int, default=1,
    help="""
Usage: scan_logfiles scan has_tags --count 2 Print log file names that
has records with two tag fields or more""")


def has_2400(logfile: str, prefix: str = '2400') -> bool:
    with open(logfile) as f:
        for line in (line.strip() for line in f.readlines()):
            if line.startswith(prefix):
                return True
        return False


def replace_2400(logfile, backup_ext='.bak'):
    if backup_ext:
        shutil.copyfile(logfile, logfile + backup_ext)
    with open(logfile) as f:
        lines = f.readlines()

    def ptime4(hhmm: str) -> datetime:
        return datetime.strptime(hhmm, '%H%M')

    def get_time4(index: int) -> datetime:
        m = re.match(r'^(?P<stamp>\d{4}).*$', lines[index])
        if m:
            return datetime.strptime(m.group('stamp'), '%H%M')
        else:
            raise ValueError(f'{line[index]}: Invalide sample')

    lines2 = []
    num_lines_changed = 0
    for line_no, line in enumerate(lines):
        if line[:4] == '2400':
            try:
                t1 = get_time4(line_no - 1)
            except IndexError:
                t1 = ptime4('0000')
            try:
                t2 = get_time4(line_no + 1)
            except IndexError:
                t2 = ptime4('2359')
            mid = (t2 - t1) / 2
            line = datetime.strftime(t1 + mid, '%H%M') + line[4:]
            num_lines_changed += 1
        lines2.append(line)

    if 0 < num_lines_changed:
        print(f'"{logfile}" modified, .bak file created')
        with open(logfile, 'w') as f:
            f.writelines(lines2)


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.command == 'fix2400':
        # for logname in sorted(glob.glob(os.path.join(args.logdir, '*.txt'))):
        for logname in args.logfiles:
            if has_2400(logname):
                replace_2400(logname, backup_ext='.bak')
    elif args.command == 'scan':
        for logname in sorted(glob.glob(os.path.join(args.logdir, '*.txt'))):
            
            def print_if_found(logname):
                '''Iterate over logfile properties'''

                for rec in logrecords_generator(logname):  # rec_loop
                    for prop in args.property:             # prop_loop
                        prop_val = getattr(rec, prop)
                        if prop == 'tags_count':
                            if args.count <= prop_val:
                                print(f'{logname}: tags_count = {prop_val}')
                                return  # break rec_loop
                        else:
                            if prop_val:
                                print(f'{logname}: {prop}')
                                return  # break rec_loop
            print_if_found(logname)
