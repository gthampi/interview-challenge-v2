from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DB_URL


# engine = create_async_engine(DB_URL, echo=True)  # we need some async driver other than psycopg2 for this?
engine = create_engine(DB_URL, echo=True)  # make this async

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
