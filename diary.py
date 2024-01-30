#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
Manage pee logs
"""
import argparse
import argcomplete
import sqlite3                  # noqa
import parse_log_re             # noqa
import add_diary
import print_diary
import test_log

LOG_DB_DEFAULT = "./pee_diary.db"
parser = argparse.ArgumentParser(
    description="Manage pee logs",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--log-db', default=LOG_DB_DEFAULT,
                    help='Log database file')
parser.add_argument('--verbose', '-v', action='count', default=0)
subparsers = parser.add_subparsers(dest='command', required=True,
                                   help='Choose a command')
parser_add = subparsers.add_parser('add', help="Add new logs")
parser_add.add_argument("log_file", help="Path to the log file", type=str)
parser_test = subparsers.add_parser('test', help="Check the log file")
parser_test.add_argument("log_file", help="Path to the log file", type=str)
subparsers.add_parser("print", help="Print already added logs")

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.command == "print":
        print_diary.print_diary(args.log_db)
    elif args.command == "test":
        test_log.test_log(args.log_file)
    else:
        add_diary.add_diary(args.log_file, log_db=args.log_db)
