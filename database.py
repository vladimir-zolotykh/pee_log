#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from contextlib import contextmanager
from sqlalchemy import select
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from models import Sample, Tag
from logrecord import LogRecord

Base = declarative_base()


class Transaction(Session):
    def get_or_make_tag(self, tag_text: str) -> Optional[Tag]:
        """Return the existing or create a new Tag"""

        if tag_text:
            tag = self.scalar(select(Tag).where(
                Tag.text == tag_text))
            if not tag:
                tag = Tag(text=tag_text)
                self.add(tag)
            return tag
        else:
            return None

    def _get_logrecord_tags(self, rec: LogRecord) -> List[Tag]:
        """For a given LogRecord "rec" return the list of Tags"""

        tags = []
        for label_caption in (f'label{n}' for n in range(1, 4)):
            tag_text = getattr(rec, label_caption)
            if tag_text:
                tags.append(self.get_or_make_tag(tag_text))
        return tags

    def add_sample(self, sample: Sample, rec: LogRecord) -> None:
        """Make a new Sample, add it to the "sample" table

        without session.commit() the changes will remain only in
        memory. Regularly, called within session_scope"""

        tags = self._get_logrecord_tags(self, rec)
        sample.tags.extend(tags)
        self.add(sample)

    def update_sample(self, sample: Sample, rec: LogRecord) -> None:
        """Update existing sample

        The function updates Sample in memory. Need session.commit() to
        "flush" data into the persistent db"""

        sample.time = rec.stamp
        sample.volume = rec.volume
        sample.text = rec.note
        tags = self._get_logrecord_tags(rec)
        sample.tags = tags

    def add_missing_tag(
            self, tags: List[Tag],
            missing_tag_text: str = 'pee'
    ) -> List[Tag]:
        """Add Tag(text=missing_tag_text) to the TAGS if missing

        return the TAGS"""

        for tag in tags:
            if tag.text == missing_tag_text:
                return tags
        new_tag = self.get_or_make_tag(missing_tag_text)
        tags.insert(0, new_tag)
        return tags


@contextmanager
def session_scope(engine):
    """Provide a transactional scope around a series of operations"""

    Session = sessionmaker(engine, class_=Transaction)
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def empty_tables(engine):
    '''Empty all tables (sample, tag, sample_tag)'''

    Base.metadata.reflect(engine)
    tables = reversed(Base.metadata.sorted_tables)
    # table_names = (t.__tablename__ for t in tables)
    table_names = ('sample_tag', 'tag', 'sample')
    ans = input(f'The content of the tables {", ".join(table_names)} '
                f'will be deleted. Are you sure? ')
    if ans.upper().startswith('Y'):
        Session = sessionmaker(engine)
        print('Deleting...', end='')
        with Session() as session:
            for table in tables:
                session.execute(table.delete())
            session.commit()
        print('done')
    else:
        print('Not confirmed, exiting...')


def initialize(engine):
    """Initialize only sample_tag, tag, sample tables

    Do not put any inital content in them."""

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


def print_tables(day, engine):
    Session = sessionmaker(engine)  # noqa
    with Session() as session:
        for sample in session.scalars(select(Sample)):
            print(sample)
