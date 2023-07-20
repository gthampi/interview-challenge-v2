from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import generic_repr, Timestamp
from sqlalchemy.orm import relationship

Base = declarative_base()


@generic_repr
class Business(Base, Timestamp):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(100), nullable=False)

    # Define the relationship between Diagnosis and Business
    diagnosis = relationship("Diagnosis", backref="business")


@generic_repr
class Symptom(Base, Timestamp):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    code = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)

    # Define the relationship between Diagnosis and Symptom
    diagnosis = relationship("Diagnosis", backref="symptom")


# Define the Diagnosis table
@generic_repr
class Diagnosis(Base, Timestamp):
    __tablename__ = 'diagnoses'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    symptom_id = Column(Integer, ForeignKey('symptoms.id'), nullable=False)
    is_diagnosed = Column(Boolean, nullable=False)

    # Define the relationship between Diagnosis and Business
    business = relationship("Business", backref="diagnoses")

    # Define the relationship between Diagnosis and Symptom
    symptom = relationship("Symptom", backref="diagnoses")
