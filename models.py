#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Table, Integer
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


sample_tag = Table(
    'sample_tag',
    Base.metadata,
    Column('sample_id', Integer, ForeignKey('sample.id', ondelete='CASCADE')),
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete='CASCADE')))


class Sample(Base):
    __tablename__ = 'sample'
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[str]
    volume: Mapped[Optional[int]]
    text: Mapped[Optional[str]]
    tags: Mapped[List["Tag"]] = relationship(
        'Tag', secondary='sample_tag', back_populates='samples',
        cascade='all, delete')

    def __repr__(self) -> str:
        return (f'Sample(id={self.id!r}, time={self.time!r}, '
                f'volume={self.volume!r}, '
                f'tags={self.tags!r}, '
                f'text={self.text!r})')

    def __str__(self) -> str:
        """Return str(sample) suitable for log (.txt) file"""

        _t = datetime.strptime(self.time, '%Y-%m-%d %H:%M:%S')
        values = [f'{_t.strftime("%H%M")}']
        if self.volume:
            values.append(str(self.volume))
        for tag in self.tags:
            values.append(tag.text)
        if self.text:
            values.append(self.text)
        return ' '.join(values)


class Tag(Base):
    __tablename__ = 'tag'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    samples: Mapped[List["Sample"]] = relationship(
        'Sample', secondary='sample_tag',
        back_populates='tags', passive_deletes=True)

    def __repr__(self) -> str:
        return f'Tag(id={self.id!r}, text={self.text!r})'

    def __str__(self) -> str:
        return str(self.text)
