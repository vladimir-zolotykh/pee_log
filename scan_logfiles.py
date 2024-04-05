#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import re
import glob
import argparse
import shutil
from datetime import datetime
import argcomplete
from sampletag_re import logrecords_generator

parser = argparse.ArgumentParser(
    prog='scan_logfiles.py',
    description='''Print logfiles "properties", e.g., has_tags, \
has_note, has_volume''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--logdir', default='./LOG_DIARY',
    help='The directory with YYYY-MM-DD.txt logfiles')


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

    def get_time4(index: int) -> datetime:
        m = re.match(r'^(?P<stamp>\d{4}).*$', lines[index])
        if m:
            return datetime.strptime(m.group('stamp'), '%H%M')
        else:
            raise ValueError(f'{line[index]}: Invalide sample')

    lines2 = []
    for line_no, line in enumerate(lines):
        if line[:4] == '2400':
            t1 = get_time4(line_no - 1)
            t2 = get_time4(line_no + 1)
            mid = (t2 - t1) / 2
            line = datetime.strftime(t1 + mid, '%H%M') + line[4:]
        lines2.append(line)

    with open(logfile, 'w') as f:
        f.writelines(lines2)


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    for logname in sorted(glob.glob(os.path.join(args.logdir, '*.txt'))):
        if has_2400(logname):
            replace_2400(logname, backup_ext='bak')
        for rec in logrecords_generator(logname):
            if rec.has_tags:
                print(f'{logname}')
                break