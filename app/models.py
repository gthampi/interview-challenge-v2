import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy_utils import generic_repr, Timestamp
from sqlalchemy.orm import mapped_column, relationship, Mapped
from app.database import Base
from settings import DB_USER


# TODO: Will we need event listeners for created_by, updated_by? from where to get user context? - env vars
# Define the Diagnosis table
@generic_repr
class Diagnosis(Base):  # Timestamp
    __tablename__ = 'diagnosis'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    symptom_id: Mapped[int] = mapped_column(ForeignKey("symptom.id"))
    is_diagnosed: Mapped[bool] = mapped_column(nullable=False)

    # metadata
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                          nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_onupdate=func.now(),
                                                          nullable=True)
    created_by: Mapped[str] = mapped_column(default=DB_USER, nullable=False)
    updated_by: Mapped[str] = mapped_column(onupdate=DB_USER, nullable=True)
    # id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    # business_id = Column(Integer, ForeignKey('business.id'), nullable=False)
    # symptom_id = Column(Integer, ForeignKey('symptom.id'), nullable=False)
    # is_diagnosed = Column(Boolean, nullable=False)


@generic_repr
class Business(Base):   # Timestamp
    __tablename__ = "business"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    business_id: Mapped[int] = mapped_column(nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    # metadata
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                          nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_onupdate=func.now(),
                                                          nullable=True)
    created_by: Mapped[str] = mapped_column(default=DB_USER, nullable=False)
    updated_by: Mapped[str] = mapped_column(onupdate=DB_USER, nullable=True)
    # id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    # business_id = Column(Integer, nullable=False, unique=True, index=True)
    # name = Column(String(100), nullable=False)

    # Define the relationship between Diagnosis and Business
    diagnoses: Mapped[List[Diagnosis]] = relationship(backref="business")   # , lazy='selectin'
    # diagnoses = relationship("Diagnosis", backref="business")


@generic_repr
class Symptom(Base):    # Timestamp
    __tablename__ = "symptom"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    code: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    # metadata
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                          nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_onupdate=func.now(),
                                                          nullable=True)
    created_by: Mapped[str] = mapped_column(default=DB_USER, nullable=False)
    updated_by: Mapped[str] = mapped_column(onupdate=DB_USER, nullable=True)
    # id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    # code = Column(String(9), nullable=False, unique=True, index=True)  # put validation for 'SYMPT' prefix
    # name = Column(String(100), nullable=False)


    # Define the relationship between Diagnosis and Symptom
    diagnoses: Mapped[List[Diagnosis]] = relationship(backref="symptom")    # , lazy='selectin'
    # diagnoses = relationship("Diagnosis", backref="symptom")
#
# @generic_repr
# class Business(Base, Timestamp):   # Timestamp
#     __tablename__ = "business"
#
#     id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
#     business_id = Column(Integer, nullable=False, unique=True, index=True)
#     name = Column(String(100), nullable=False)
#
#     # metadata
#     created_by = Column(String(50), default=DB_USER)
#     updated_by = Column(String(50), onupdate=DB_USER)
#
#     # Define the relationship between Diagnosis and Business
#     diagnoses = relationship("Diagnosis", backref="business")
#
#
# @generic_repr
# class Symptom(Base, Timestamp):    # Timestamp
#     __tablename__ = "symptom"
#
#     id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
#     code = Column(String(9), nullable=False, unique=True, index=True)    # put validation for 'SYMPT' prefix
#     name = Column(String(100), nullable=False)
#
#     # metadata
#     created_by = Column(String(50), default=DB_USER)
#     updated_by = Column(String(50), onupdate=DB_USER)
#
#     # Define the relationship between Diagnosis and Symptom
#     diagnoses = relationship("Diagnosis", backref="symptom")
#
#
# # Define the Diagnosis table
# @generic_repr
# class Diagnosis(Base, Timestamp):  # Timestamp
#     __tablename__ = 'diagnosis'
#
#     id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
#     business_id = Column(Integer, ForeignKey('business.id'), nullable=False)
#     symptom_id = Column(Integer, ForeignKey('symptom.id'), nullable=False)
#     is_diagnosed = Column(Boolean, nullable=False)
#
#     # metadata
#     created_by = Column(String(50), default=DB_USER)
#     updated_by = Column(String(50), onupdate=DB_USER)

