#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()


sample_tag = Table(
    'sample_tag', Base.metadata,
    Column('sample_id', Integer, ForeignKey('sample.id', ondelete='CASCADE')),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete='CASCADE'))
)


class Sample(Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    time = Column(String, unique=True)
    volume = Column(Integer)
    text = Column(String)
    tags = relationship(
        'Tag', secondary=sample_tag, back_populates='samples',
        # cascade="all, delete-orphan"
        cascade='all, delete')
    # __table_args__ = (
    #     UniqueConstraint('time', name='unique_time_constraint'),
    # )

    def __repr__(self) -> str:
        return (f'Sample(id={self.id!r}, time={self.time!r}, '
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
