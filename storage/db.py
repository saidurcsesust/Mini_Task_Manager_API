import os
from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="todo")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    due_date = Column(Date, nullable=True)


def get_database_url():
    return os.getenv("DATABASE_URL", "sqlite:///data/tasks.db")


def init_engine():
    return create_engine(get_database_url(), future=True)


def init_db(engine):
    Base.metadata.create_all(engine)


def make_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
