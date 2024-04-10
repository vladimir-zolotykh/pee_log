#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import List, Optional
import sampletag as SA
from logrecord import LogRecord


def get_logrecord_tags(
        session: SA.Session, rec: LogRecord
) -> List[SA.Tag]:
    def get_or_make_tag(
            session: SA.Session, tag_text: str
    ) -> Optional[SA.Tag]:
        """Return the existing or create new Tag"""

        if tag_text:
            tag = session.scalar(SA.select(SA.Tag).where(
                SA.Tag.text == tag_text))
            if not tag:
                tag = SA.Tag(text=tag_text)
                session.add(tag)
            return tag
        else:
            return None

    tags = []
    for label_caption in (f'label{n}' for n in range(1, 4)):
        tag_text = getattr(rec, label_caption)
        if tag_text:
            tags.append(get_or_make_tag(session, tag_text))
    return tags


def add_sample(
        session: SA.Session, sample: SA.Sample, rec: LogRecord
) -> None:
    """Make a new Sample, add it to the sample table"""

    tags = get_logrecord_tags(session, rec)
    sample.tags.extend(tags)
    session.add(sample)


def update_sample(session, sample: SA.Sample, rec: LogRecord) -> None:
    """Update existing sample"""

    sample.time = rec.stamp
    sample.volume = rec.volume
    sample.text = rec.note
    tags = get_logrecord_tags(session, rec)
    sample.tags = tags
