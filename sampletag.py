#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, ForeignKey, Table, \
    create_engine, select, func  # noqa
from sqlalchemy.orm import declarative_base, relationship, \
    sessionmaker, Session       # noqa
from sqlalchemy.exc import SQLAlchemyError  # noqa
import argparse
import argcomplete
import test_log
from sampletag_re import logrecords_generator
Base = declarative_base()


sample_tag = Table(
    'sample_tag', Base.metadata,
    Column('sample_id', Integer, ForeignKey('sample.id', ondelete='CASCADE')),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete='CASCADE'))
)


class Sample(Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    time = Column(String)
    volume = Column(Integer)
    text = Column(String)
    tags = relationship(
        'Tag', secondary=sample_tag, back_populates='samples',
        # cascade="all, delete-orphan"
        cascade='all, delete')

    def __repr__(self) -> str:
        return (f'Samples(id={self.id!r}, time={self.time!r}, '
                f'volume={self.volume!r}, text={self.text!r}) '
                f'tags={self.tags!r}')


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    samples = relationship(
        'Sample', secondary=sample_tag,
        back_populates='tags', passive_deletes=True)

    def __repr__(self) -> str:
        return f'Tag(id={self.id!r}, text=={self.text!r})'


def add_logfile_records(logfile: str, engine) -> None:
    for rec in logrecords_generator(logfile):
        tag1 = Tag(text=rec.label1)
        s1 = Sample(time=rec.stamp, volume=rec.volume)
        s1.tags.append(tag1)
        Session = sessionmaker(engine)  # noqa
        with Session() as session:
            session.add(s1)
            session.commit()


@contextmanager
def session_scope(engine):
    """Provide a transactional scope around a series of operations"""

    session = Session(engine)
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


parser = argparse.ArgumentParser(
    prog='sampletag.py',
    description='Manage sampletag.db',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--echo', action='store_true', help='Print emitted SQL commands')
parser.add_argument('--db', default='sampletag.db', help='Database file (DB)')
subparsers = parser.add_subparsers(
    description='Manage logging database DB',
    dest='command', title=f'{sys.argv[0]} commands')
parser_init = subparsers.add_parser(
    'init', help='Initialize DB. Make empty tables')
parser_del = subparsers.add_parser('del', help='Delete table contents')
# set_defaults func signature: (logfile: str, engine: Engine)
parser_del.set_defaults(func=lambda ingnore, engine: empty_tables(engine))
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


def empty_tables(engine):
    '''Empty all tables (sample, tag, sample_tag)'''

    Base.metadata.reflect(engine)
    tables = reversed(Base.metadata.sorted_tables)
    # table_names = (t.__tablename__ for t in tables)
    table_names = ('sample_tag', 'tag', 'sample')
    ans = input(f'The content of the tables {", ".join(table_names)} '
                f'will be deleted. Are you sure? ')
    if ans.upper().startswith('Y'):
        Session = sessionmaker(engine)  # noqa
        with Session() as session:
            for table in tables:
                session.execute(table.delete())
            session.commit()


def initialize(engine):
    Base.metadata.create_all(engine)
    # pee = Tag(text='pee')
    # stool = Tag(text='stool')
    # creatine = Tag(text='creatine')
    # s1 = Sample(time='2024-03-28 19:00:15', volume=123)
    # s2 = Sample(time='2024-03-29 20:00:20', volume=456)
    # s3 = Sample(time='2024-03-31 18:15:00', volume=789)
    # s1.tags.extend((pee, creatine))
    # s2.tags.append(stool)
    # s3.tags.append(pee)
    # Session = sessionmaker(engine)  # noqa
    # with Session() as session:
    #     session.add_all((s1, s2))
    #     session.commit()


def print_tables(engine):
    Session = sessionmaker(engine)  # noqa
    with Session() as session:
        for sample in session.scalars(select(Sample)):
            print(sample)


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    engine = create_engine(f'sqlite:///{args.db}', echo=args.echo)
    if args.command == 'del':
        args.func('', engine)
    else:
        for log in args.logfile:
            args.func(log, engine)
