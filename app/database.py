from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from settings import DB_URL

engine = create_async_engine(DB_URL, echo=True)  # we need some async driver other than psycopg2 for this?
# , connect_args={"check_same_thread": False}
# engine = create_engine(DB_URL, echo=True)  # make this async

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
# SessionLocal = sessionmaker(bind=engine)


# Base = declarative_base()
class Base(DeclarativeBase):
    pass
