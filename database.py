#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from itertools import groupby
from operator import attrgetter
from typing import Generator
from contextlib import contextmanager
from sqlalchemy import select, func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from datetime import datetime
import models
from logrecord import LogRecord
from summary_box import SummaryBox
import models as md
from summary_view import SummaryData
# Base = declarative_base()


class Transaction(Session):
    def get_or_make_tag(self, tag_text: str) -> md.Tag:
        """Return the existing or create a new Tag"""

        tag = self.scalar(select(md.Tag).where(
            md.Tag.text == tag_text))
        if not tag:
            tag = md.Tag(text=tag_text)
            self.add(tag)
        return tag

    def _get_logrecord_tags(self, rec: LogRecord) -> List[md.Tag]:
        """For a given LogRecord "rec" return the list of Tags"""

        tags = []
        for label_caption in (f'label{n}' for n in range(1, 4)):
            tag_text = getattr(rec, label_caption)
            if tag_text:
                tags.append(self.get_or_make_tag(tag_text))
        return tags

    def add_sample(self, sample: md.Sample, rec: LogRecord) -> None:
        """Make a new Sample, add it to the "sample" table

        without session.commit() the changes will remain only in
        memory. Regularly, called within session_scope"""

        tags = self._get_logrecord_tags(rec)
        sample.tags.extend(tags)
        self.add(sample)

    def update_sample(self, sample: md.Sample, rec: LogRecord) -> None:
        """Update existing sample

        The function updates Sample in memory. Need session.commit() to
        "flush" data into the persistent db"""

        sample.time = datetime.strftime(rec.stamp, '%Y-%m-%d %H:%M:%S')
        sample.volume = rec.volume
        sample.text = rec.note
        tags = self._get_logrecord_tags(rec)
        sample.tags = tags

    def add_missing_tag(
            self, tags: List[md.Tag],
            missing_tag_text: str = 'pee'
    ) -> List[md.Tag]:
        """Add Tag(text=missing_tag_text) to the TAGS if missing

        return the TAGS"""

        for tag in tags:
            if tag.text == missing_tag_text:
                return tags
        new_tag = self.get_or_make_tag(missing_tag_text)
        if new_tag:
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

    md.Base.metadata.reflect(engine)
    tables = reversed(md.Base.metadata.sorted_tables)
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
    """Initialize sample_tag, tag, and sample tables"""

    with Session(engine) as session:
        md.Base.metadata.create_all(engine)
        session.commit()
        session.close()


def print_tables(day, engine):
    Session = sessionmaker(engine)  # noqa
    with Session() as session:
        for sample in session.scalars(select(md.Sample)):
            print(sample)


def update_summary_box(
        engine: Engine, summary_box: SummaryBox, date: datetime
) -> None:
    date_str = date.strftime('%Y-%m-%d')
    summary_box.date = date_str
    with Session(engine) as session:
        query = select(md.Sample).where(func.DATE(md.Sample.time) == date_str)
        tags = set()
        notes = []
        count = 0
        for sample in session.scalars(query):
            count += 1
            for tag in sample.tags:
                tags.add(tag.text)
            if sample.text:
                notes.append(sample.text)
        summary_box.count = str(count)
        summary_box.tag = list(tags)
        summary_box.note = notes


def generate_summary_data(
        engine: Engine
) -> Generator[SummaryData, None, None]:
    with Session(engine) as session:
        query = select(md.Sample)
        samples = session.scalars(query)

        def sample_date(sample: md.Sample) -> str:
            return datetime.strptime(sample.time, '%Y-%m-%d  %H:%M:%S').date()

        samples = sorted(samples, key=sample_date)
        grouped_samples = groupby(samples, key=sample_date)
        for date, group in grouped_samples:
            tags = set()
            notes = []
            count = 0
            volume = 0
            for sample in group:
                count += 1
                if isinstance(sample.volume, int):
                    volume += int(sample.volume)
                for tag in sample.tags:
                    tags.add(tag.text)
                if sample.text:
                    notes.append(sample.text)
            yield SummaryData(sample.time, count, volume,
                              ', '.join(tags), notes)
