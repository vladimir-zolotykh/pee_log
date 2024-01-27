#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Calls print_diary() or add_logs()
"""
import argparse
import argcomplete
import sqlite3                  # noqa
import parse_log_re             # noqa
import add_logs
import print_diary


parser = argparse.ArgumentParser(
    description="Manage pee logs",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--log-db', default='./pee_diary.db',
                    help='Log database file')
parser.add_argument('--verbose', '-v', action='count', default=0)
subparsers = parser.add_subparsers(dest='command', required=True,
                                   help='Choose a command')
parser_add = subparsers.add_parser('add', help="LOG_FILE Add new logs")
parser_add.add_argument("log_file", help="Path to the log file", type=str)
subparsers.add_parser("print", help="Print already added logs")

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.command == "print":
        print_diary.print_diary(args.log_db)
    else:
        add_logs.add_logs(args.log_file)
