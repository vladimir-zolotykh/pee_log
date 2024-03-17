#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    records: Mapped[List["Record"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (f"Event(id={self.id!r}, text={self.text!r})")


class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(primary_key=True)
    stamp: Mapped[str]
    volume: Mapped[Optional[int]]
    note: Mapped[Optional[str]]
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    event: Mapped["Event"] = relationship(back_populates="records")

    def __repr__(self) -> str:
        return (f"Record(id={self.id!r}, stamp={self.stamp!r}, "
                f"volume={self.volume!r}, note={self.note!r})")


engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)
