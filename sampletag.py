#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy import Column, Integer, String, ForeignKey, Table, \
    create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
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


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    samples = relationship('Sample', secondary=sample_tag,
                           back_populates='tags')


if __name__ == '__main__':
    engine = create_engine('sqlite:///sampletag.db', echo=True)
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
