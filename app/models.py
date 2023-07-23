from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy_utils import generic_repr
from sqlalchemy.orm import mapped_column, relationship, Mapped
from app.database import Base
from settings import DB_USER


# Define the Diagnosis table
@generic_repr
class Diagnosis(Base):
    __tablename__ = "diagnosis"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    symptom_id: Mapped[int] = mapped_column(ForeignKey("symptom.id"))
    is_diagnosed: Mapped[bool] = mapped_column(nullable=False)

    # metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_onupdate=func.now(), nullable=True
    )
    created_by: Mapped[str] = mapped_column(default=DB_USER, nullable=False)
    updated_by: Mapped[str] = mapped_column(onupdate=DB_USER, nullable=True)


@generic_repr
class Business(Base):  # Timestamp
    __tablename__ = "business"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    business_id: Mapped[int] = mapped_column(nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    # metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_onupdate=func.now(), nullable=True
    )
    created_by: Mapped[str] = mapped_column(default=DB_USER, nullable=False)
    updated_by: Mapped[str] = mapped_column(onupdate=DB_USER, nullable=True)

    # Define the relationship between Diagnosis and Business
    diagnoses: Mapped[List[Diagnosis]] = relationship(backref="business")


@generic_repr
class Symptom(Base):  # Timestamp
    __tablename__ = "symptom"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    code: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    # metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_onupdate=func.now(), nullable=True
    )
    created_by: Mapped[str] = mapped_column(default=DB_USER, nullable=False)
    updated_by: Mapped[str] = mapped_column(onupdate=DB_USER, nullable=True)

    # Define the relationship between Diagnosis and Symptom
    diagnoses: Mapped[List[Diagnosis]] = relationship(backref="symptom")
