from contextlib import contextmanager

from fastapi import Depends
from sqlalchemy.orm import Session

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy_utils import create_database, database_exists

from app.database import SessionLocal
from app.models import Business, Symptom, Diagnosis


# from settings import DB_URL


# engine = create_engine(DB_URL, echo=True)
# SessionLocal = sessionmaker(engine)
#
# # Create a new session
# session = SessionLocal()


# Dependency to get the database session # TODO: check this
# @contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def update_db(data, db: Session = Depends(get_db)):
def update_db(data, db: Session):
    # TODO: should we use pandas here?
    csv_business_ids, csv_symptom_codes = set(), set()
    for row in data:
        csv_business_ids.add(row['Business ID'])
        csv_symptom_codes.add(row['Symptom Code'])

    existing_businesses = db.query(Business).filter(Business.business_id.in_(csv_business_ids)).all()
    existing_businesses_dict = {business.business_id: business.id for business in existing_businesses}

    existing_symptoms = db.query(Symptom).filter(Symptom.code.in_(csv_symptom_codes)).all()
    existing_symptoms_dict = {symptom.code: symptom.id for symptom in existing_symptoms}

    diagnoses_to_insert = []
    for row in data:

        business_id = int(row['Business ID'])
        if business_id not in existing_businesses_dict:
            business = Business(business_id=business_id, name=row['Business Name'])
            db.add(business)
            db.flush()
            # update dict with new record
            existing_businesses_dict[business_id] = business.id

        if row['Symptom Code'] not in existing_symptoms_dict:
            symptom = Symptom(code=row['Symptom Code'], name=row['Symptom Name'])
            db.add(symptom)
            db.flush()
            existing_symptoms_dict[row['Symptom Code']] = symptom.id

        # TODO: write logic to save is_diagnosed
        diagnosis = Diagnosis(is_diagnosed=True,
                              business_id=existing_businesses_dict[business_id],
                              symptom_id=existing_symptoms_dict[row['Symptom Code']])
        diagnoses_to_insert.append(diagnosis)

    db.bulk_save_objects(diagnoses_to_insert)
    # TODO: bulk_save_object when no relationships (simple insert) otherwise use add_all

    # for row in data:
    # Check if the Business already exists in the database, or create a new one
    # business = session.query(Business).filter_by(business_id=row['Business ID']).first()
    # if not business:
    #     business = Business(business_id=row['Business ID'], name=row['Business Name'])
    #     session.add(business)
    #
    # # Check if the Symptom already exists in the database, or create a new one
    #     symptom = session.query(Symptom).filter_by(code=row['Symptom Code']).first()
    #     if not symptom:
    #         symptom = Symptom(code=row['Symptom Code'], name=row['Symptom Name'])
    #         session.add(symptom)
    #
    # # Create a new Diagnosis entry
    # diagnosis = Diagnosis(business_id=row['Business ID'], symptom_id=symptom.id,       # TODO: convert code to ID
    #                       is_diagnosed=row['Symptom Diagnostic'])  # TODO: convert text to bool
    # session.add(diagnosis)

    # Commit the changes to the database
    db.commit()

    # Close the session
    db.close()
