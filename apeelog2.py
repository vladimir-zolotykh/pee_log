#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
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


class Logged(Base):             # former "User"
    __tablename__ = "log_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[str]
    volume: Mapped[Optional[int]]
    note: Mapped[Optional[str]] = mapped_column(default='')

    events: Mapped[List["Event"]] = relationship(
        back_populates="logged", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (f"Logged(id={self.id!r}, time={self.time!r}, "
                f"volume={self.volume!r}, note={self.note!r})")


class Event(Base):              # former "Address"
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(unique=True)
    logged_id: Mapped[int] = mapped_column(ForeignKey("log_records.id"))
    logged: Mapped["Logged"] = relationship(back_populates="events")

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, text={self.text!r})"


if __name__ == '__main__':
    engine = create_engine("sqlite://", echo=True)
    # engine = create_engine('sqlite:///pee_diary_al.db', echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        pee, creatine = Event(text='pee'), Event(text='Creatine')
        r1 = Logged(time='2024-01-26 12:24:00', volume=357)
        r1.events.append(pee)
        r2 = Logged(time='2024-01-26 13:00:00', volume=439)
        r2.events.extend([pee, creatine])
        # r2.events.append(pee)
        # r2.events.append(creatine)
        r3 = Logged()
        r3 = Logged(time='2024-01-26 23:50:00', volume=0)
        r3.events.append(pee)
        session.add_all([r1, r2, r3])
        session.commit()
        session.close()
