#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy import Column, Integer, String, ForeignKey, Table, \
    create_engine, select
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
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
    tags = relationship('Tag', secondary=sample_tag, back_populates='samples')

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


parser = argparse.ArgumentParser(
    description='Initialize/print sampletag.db',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('command', type=str, choices=('init', 'print'))


def initialize(engine):
    Base.metadata.create_all(engine)
    pee = Tag(text='pee')
    stool = Tag(text='stool')
    creatine = Tag(text='creatine')
    s1 = Sample(time='2024-03-28 19:00:15', volume=123)
    s2 = Sample(time='2024-03-29 20:00:20', volume=456)
    s1.tags.extend((pee, creatine))
    s2.tags.append(stool)
    Session = sessionmaker(engine)
    with Session() as session:
        session.add_all(s1, s2)
        session.commit()


def print_tables(engine):
    Session = sessionmaker(engine)
    with Session() as session:
        for sample in session.scalars(select(Sample)):
            print(sample)


if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    engine = create_engine('sqlite:///sampletag.db', echo=False)
    if args.command == 'init':
        initialize(engine)
    elif args.command == 'print':
        print_tables(engine)
    else:
        pass
