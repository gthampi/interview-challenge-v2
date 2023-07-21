from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean
from sqlalchemy_utils import generic_repr, Timestamp
from sqlalchemy.orm import relationship
from app.database import Base
from settings import DB_USER


# TODO: Will we need event listeners for created_by, updated_by? from where to get user context? - env vars
@generic_repr
class Business(Base):   # Timestamp
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    business_id = Column(Integer, nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)

    # Define the relationship between Diagnosis and Business
    diagnoses = relationship("Diagnosis", backref="business")


@generic_repr
class Symptom(Base):    # Timestamp
    __tablename__ = "symptom"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    code = Column(String(9), nullable=False, unique=True, index=True)    # put validation for 'SYMPT' prefix
    name = Column(String(100), nullable=False)

    # Define the relationship between Diagnosis and Symptom
    diagnoses = relationship("Diagnosis", backref="symptom")


# Define the Diagnosis table
@generic_repr
class Diagnosis(Base):  # Timestamp
    __tablename__ = 'diagnosis'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    business_id = Column(Integer, ForeignKey('business.id'), nullable=False)
    symptom_id = Column(Integer, ForeignKey('symptom.id'), nullable=False)
    is_diagnosed = Column(Boolean, nullable=False)

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

