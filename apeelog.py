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
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    records: Mapped[List["Record"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (f"Event(id={self.id!r}, name={self.name!r}, "
                f"fullname={self.fullname!r})")


class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    event: Mapped["Event"] = relationship(back_populates="records")

    def __repr__(self) -> str:
        return f"Record(id={self.id!r}, email_address={self.email_address!r})"


engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)
