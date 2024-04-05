#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import os
import glob
import argparse
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

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    for logname in sorted(glob.glob(os.path.join(args.logdir, '*.txt'))):
        for rec in logrecords_generator(logname):
            if rec.has_tags:
                print(f'{logname}')
                break
