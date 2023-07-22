from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Business, Symptom, Diagnosis


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_diagnoses_by_params(business_id, diagnostic, db: Session):
    pass


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
            # update dict with new record
            existing_symptoms_dict[row['Symptom Code']] = symptom.id

        # TODO: write logic to save is_diagnosed
        diagnosis = Diagnosis(is_diagnosed=True,
                              business_id=existing_businesses_dict[business_id],
                              symptom_id=existing_symptoms_dict[row['Symptom Code']])
        diagnoses_to_insert.append(diagnosis)

    db.bulk_save_objects(diagnoses_to_insert)  # seems to be more efficient than add_all

    # Commit the changes to the database
    db.commit()

    # Close the session
    db.close()
