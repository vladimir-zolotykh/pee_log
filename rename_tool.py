#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
'''
Was much simpler for me to generate simple .sh files that repeated
"sed -i.bak..." and "git mv " commands than to create and debug the
corresponding Python functions.
'''
import os
from contextlib import contextmanager
from glob import glob
import re
import subprocess
DIARY_DIR = 'LOG_DIARY'
old_filename_re = re.compile(r'^(\d{2})(\d{2})(\d{2})\.txt$')
new_filename_re = re.compile(r'^(\d{4})-(\d{2})-(\d{2})\.txt$')
filename_re = old_filename_re.pattern + new_filename_re.pattern


@contextmanager
def pushd(new_dir):
    old_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        yield old_dir
    finally:
        os.chdir(old_dir)


# #!/bin/bash

# # Loop through each .txt file in the current directory
# for file in *.txt; do
#     # Execute the sed command for each file
#     sed -i.bak
#         '1s/\([0-9]\{2\}\)\/\([0-9]\{2\}\)\/\([0-9]\{2\}\)/20\1-\2-\3/'
#          "$file"
# done


def sed_date_line(log_file, show_script=True, backup=False):
    '''Change the date format of the 1st line

    yy/mm/dd -> yyyy-mm-dd'''

    cmd = [
        'sed', '-i'
        r'1s/\([0-9]\{2\}\)\/\([0-9]\{2\}\)\/\([0-9]\{2\}\)/20\1-\2-\3/']

    subprocess.run(cmd, log_file)

    # 24/02/01 or 2024-02-01
    pass


def change_header_date(log_file, show_script=1, backup=True):
    """Change date format of the 1st line

    yymmdd -> YYYY-MM-DD, e.g, 240114 -> 2024-01-14"""
    for log_file in sorted(glob('*.txt')):
        match_old = old_filename_re.match(log_file)
        match_new = new_filename_re.match(log_file)
        sed_cmd = r'sed -i "s/^24\/01\/24$/2024-01-24/g" filename.txt'
        if match_old:
            yy, mm, dd = match_old.groups()
        elif match_new:
            yyyy, mm, dd = match_new.groups()
        else:
            pass
        if show_script:
            print(sed_cmd)
        else:
            pass


def rename_files(diary_dir=DIARY_DIR, show_script=1):
    """Rename YYMMDD.txt files of DIARY_DIR to YYYY-MM-DD.txt"""

    with pushd(diary_dir):
        for log_file in sorted(glob('*.txt')):
            match = old_filename_re.match(log_file)
            if match:
                yy, mm, dd = match.groups()
                cmd = ['mv', '--no-clobber', log_file, f'20{yy}-{mm}-{dd}.txt']
                if show_script:
                    print(' '.join(cmd))
                else:
                    subprocess.run(cmd, check=True)
            else:
                pass
