#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, \
    create_engine, select, func  # noqa
from sqlalchemy.orm import declarative_base, relationship, \
    sessionmaker, Session       # noqa
import argparse
import argcomplete
Base = declarative_base()


sample_tag = Table(
    'sample_tag', Base.metadata,
    Column('sample_id', Integer, ForeignKey('sample.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Sample(Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    time = Column(String)
    volume = Column(Integer)
    text = Column(String)
    tags = relationship('Tag', secondary=sample_tag, back_populates='samples',
                        cascade='all, delete')

    def __repr__(self) -> str:
        return (f'Samples(id={self.id!r}, time={self.time!r}, '
                f'volume={self.volume!r}, text={self.text!r}) '
                f'tags={self.tags!r}')


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    samples = relationship('Sample', secondary=sample_tag,
                           back_populates='tags')

    def __repr__(self) -> str:
        return f'Tag(id={self.id!r}, text=={self.text!r})'


def _test():
    print('TEST')


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
parser_init = subparsers.add_parser('init', help='Initialize DB')
parser_test = subparsers.add_parser(
    'test', help='Test consistency of log file(s)')
parser_test.add_argument(
    'logfile', nargs='+',
    help='The .txt file (e.g., LOG_DIARY/2024-03-15.txt)')
parser_test.set_defaults(func=_test)
parser_add = subparsers.add_parser('add', help='Add logfile(s) to the DB')
parser_add.add_argument(
    'logfile', nargs='+',
    help='The .txt file (e.g., LOG_DIARY/2024-03-15.txt)')
parser_print = subparsers.add_parser(
    'print', help='Print the "sample" table of the DB')
parser_print.add_argument(
    '--day', help='Print all log records of the day', default=datetime.now())


def initialize(engine):
    Base.metadata.create_all(engine)
    pee = Tag(text='pee')
    stool = Tag(text='stool')
    creatine = Tag(text='creatine')
    s1 = Sample(time='2024-03-28 19:00:15', volume=123)
    s2 = Sample(time='2024-03-29 20:00:20', volume=456)
    s3 = Sample(time='2024-03-31 18:15:00', volume=789)
    s1.tags.extend((pee, creatine))
    s2.tags.append(stool)
    s3.tags.append(pee)
    Session = sessionmaker(engine)  # noqa
    with Session() as session:
        session.add_all((s1, s2))
        session.commit()


def print_tables(engine):
    Session = sessionmaker(engine)  # noqa
    with Session() as session:
        for sample in session.scalars(select(Sample)):
            print(sample)


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print(f'{args = }')
    exit(0)
    engine = create_engine('sqlite:///sampletag.db', echo=args.echo)
    if args.command == 'init':
        initialize(engine)
    elif args.command == 'print':
        print_tables(engine)
    else:
        pass
