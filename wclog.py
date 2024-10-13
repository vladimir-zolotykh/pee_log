#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.exc import SQLAlchemyError
import argparse
import argcomplete
import test_log
from sampletag_re import logrecords_generator
import database as db
import models as md
from log_diary_config import read_config


def add_logfile_records(
        logfile: str, engine, pee_optional: bool = False,
        check_duplicates: bool = False,
        verbose: bool = False
) -> None:
    """Add LOGFILE records to DB (all records or none)

    Read the record, make the Sample from it, add the Sample to the DB."""

    line_no: int
    num_skipped: int = 0
    with db.session_scope(engine) as session:
        try:
            for line_no, rec in enumerate(logrecords_generator(logfile), 1):
                if check_duplicates:
                    rec_stamp = rec.stamp.strftime("%Y-%m-%d %H:%M:%S")
                    if session.scalar(
                            select(md.Sample)
                            .where(md.Sample.time == rec_stamp)):
                        if verbose:
                            w1 = f'{os.path.basename(logfile)}:{line_no}'
                            print(f'{w1:17s} skipped, '
                                  f'"{rec.stamp}" exists in '
                                  f'{engine.url.database}')
                        num_skipped += 1
                        continue
                tags = session.add_missing_tag(
                    session._get_logrecord_tags(rec),
                    missing_tag_text='pee',
                    pee_optional=pee_optional)
                kwds = {'time': rec.stamp, 'volume': rec.volume,
                        'text': rec.note}
                sample = md.Sample(**kwds)
                session.add(sample)
                sample.tags.extend(tags)
        except ValueError:
            session.rollback()
            raise
    if num_skipped and verbose and check_duplicates:
        print(f'Total {num_skipped} lines was skipped')


parser = argparse.ArgumentParser(
    prog='wclog.py',
    description='Manage wclog.db',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--echo', action='store_true', help='Print emitted SQL commands')
parser.add_argument('--db', default='wclog.db', help='Database file (DB)')
parser.add_argument(
    '--verbose', '-v', action='count', default=0, help='''
Provide some feedback. E.g., add_logfile_records prints its
`pee_optional` parameter if args.verbose > 0
''')
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
# Orignally the log record "1030" added PEE tag to the db
# implicitly. Similarly, "1140 IMET" added to the db two tags, PEE and
# IMET.  If --pee-orignal is specified, "1030" still adds PEE tag,
# while "1140 IMET" adds only IMET tag
parser_add.add_argument(
    '--pee-optional', action='store_true', help='''
Orignally the log file line "1030" added PEE tag to the db
implicitly. Similarly, "1140 IMET" added two tags, PEE and IMET.  If
--pee-optional is specified, "1030" still adds PEE tag, while
"1140 IMET" adds only IMET tag''')
parser_add.set_defaults(func=add_logfile_records)

parser_update = subparsers.add_parser('update', help="""
Update logfile in the DB. Use when a few records are missing in the
logfile when it was added. Read the file and add only the missing
records.
""")
parser_update.add_argument(
    'logfile', help='The .txt file (e.g., LOG_DIARY/2024-03-15.txt)')

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
    if not os.path.exists(args.db):
        print(f"""\
{args.db} is missing. Have you started wclog.py from the right
directory (shall be ~/Documents/pee_log)? Otherwise set --db option\
        """)
        exit(1)
    engine = create_engine(f'sqlite:///{args.db}', echo=args.echo)
    try:
        engine.connect()
    except SQLAlchemyError as err:
        print(f'{err = }')
    if args.command in ('init', 'initialize'):
        args.func('', engine)
    elif args.command == 'del':
        args.func('', engine)   # func = empty_tables
    elif args.command == 'print':
        args.func(args.day, engine)
    elif args.command == 'test':
        for log in args.logfile:
            args.func(log, engine)
    elif args.command == 'update':
        add_logfile_records(args.logfile, engine,
                            verbose=True, check_duplicates=True)
    else:                       # args.command = `add`
        pee_optional_dict = read_config()
        for log in args.logfile:
            _m = ''
            if (args.pee_optional or (os.path.basename(log) in
                                      pee_optional_dict)):
                pee_optional_flag = True
                _m = '(with pee_optional=True)'
            else:
                pee_optional_flag = False
            try:
                # args.func is `add_logfile_records`
                args.func(log, engine, pee_optional=pee_optional_flag,
                          verbose=args.verbose)
                print(f'"{log}" added successfully {_m}')
            except SQLAlchemyError as err:
                print(f'"{log}": {err}')
            finally:
                sys.stdout.flush()
