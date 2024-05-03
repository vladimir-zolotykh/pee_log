#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
from datetime import datetime
from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
import argparse
import argcomplete
import test_log
from sampletag_re import logrecords_generator
import database as db
# from database import session_scope, initialize, empty_tables, print_tables
import models as md
# Base = declarative_base()


def add_logfile_records(logfile: str, engine) -> None:
    """Add LOGFILE records to DB (all records or none)

    Read the record, make the Sample from it, add the Sample to the DB."""

    for rec in logrecords_generator(logfile):
        with db.session_scope(engine) as session:
            tags = session.add_missing_tag(session._get_logrecord_tags(rec),
                                           missing_tag_text='pee')
            kwds = {'time': rec.stamp, 'volume': rec.volume, 'text': rec.note}
            sample = md.Sample(**kwds)
            session.add(sample)
            sample.tags.extend(tags)


parser = argparse.ArgumentParser(
    prog='wclog.py',
    description='Manage wclog.db',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--echo', action='store_true', help='Print emitted SQL commands')
parser.add_argument('--db', default='wclog.db', help='Database file (DB)')
subparsers = parser.add_subparsers(
    description='Manage logging database DB',
    dest='command', title=f'{sys.argv[0]} commands')
parser_init = subparsers.add_parser(
    'init', help='Initialize DB. Make empty tables',
    aliases=['initialize'])
parser_init.set_defaults(func=lambda _, engine: db.initialize(engine))
parser_del = subparsers.add_parser(
    'del', help='Delete table contents', aliases=['empty'])
# set_defaults func signature: (logfile: str, engine: Engine)
parser_del.set_defaults(func=lambda ingnore, engine: db.empty_tables(engine))
parser_test = subparsers.add_parser(
    'test', help='Test consistency of log file(s)')
parser_test.add_argument(
    'logfile', nargs='+',
    help='The .txt file (e.g., LOG_DIARY/2024-03-15.txt)')
# parser_test.set_defaults(func=test_logfile)
parser_test.set_defaults(func=lambda file, ignore: test_log.test_log(file))
parser_add = subparsers.add_parser('add', help='Add logfile(s) to the DB')
parser_add.add_argument(
    'logfile', nargs='+',
    help='The .txt file (e.g., LOG_DIARY/2024-03-15.txt)')
parser_add.set_defaults(func=add_logfile_records)
parser_print = subparsers.add_parser(
    'print', help='Print the "sample" table of the DB')
parser_print.add_argument(
    '--day', help='Print all log records of the day', default=datetime.now())
# print_tables is define later. Withot lambda I'll get
# NameError: name 'print_tables' is not defined
parser_print.set_defaults(
    func=lambda day, engine: db.print_tables(day, engine))


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    engine = create_engine(f'sqlite:///{args.db}', echo=args.echo)
    if args.command in ('init', 'initialize'):
        args.func('', engine)
    elif args.command == 'del':
        args.func('', engine)   # func = empty_tables
    elif args.command == 'print':
        args.func(args.day, engine)
    else:
        for log in args.logfile:
            # func: test_log or add_logfile_records
            try:
                args.func(log, engine)
                print(f'"{log}" added successfully')
            except SQLAlchemyError as err:
                print(f'"{log}": {err}')
            finally:
                sys.stdout.flush()