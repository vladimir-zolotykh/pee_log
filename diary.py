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
parser_add = subparsers.add_parser('add', help="Add logs")
parser_add.add_argument("log_file", help="Path to the log file", type=str)
parser_test = subparsers.add_parser('test', help="Check the log file")
parser_test.add_argument("log_file", help="Path to the log file", type=str)
parser_print = subparsers.add_parser("print", help="Print logs")
parser_print.add_argument(
    "--req-date", help="Print the date logs", type=print_diary.date_type)
parser_delete = subparsers.add_parser("delete", help="Delete logs")
parser_delete.add_argument(
    "--req-date", help="Delete all REQ_DATE logs from database",
    type=print_diary.date_type)

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if args.command == "delete":
        print_diary.delete_diary(args.req_date, args.log_db)
    elif args.command == "print":
        print_diary.print_diary(args.req_date, args.log_db)
    elif args.command == "test":
        test_log.test_log(args.log_file)
    else:
        add_diary.add_diary(args.log_file, log_db=args.log_db)
