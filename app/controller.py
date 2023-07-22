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

    # existing_businesses = await asyncio.gather(db.query(Business).filter(Business.business_id.in_(csv_business_ids)).all())
    # use ensure future instead of create task when we don't need to implement custom event loop

    # get_existing_business_mappings_task = asyncio.ensure_future(get_business_id_mapping(csv_business_ids, db))
    # get_existing_symptoms_mappings_task = asyncio.ensure_future(get_symptom_code_mapping(csv_symptom_codes, db))
    #
    diagnoses_to_insert = []
    # -- causes cold start, looking into sharing the session during concurrency
    # business_mappings = await get_existing_business_mappings_task
    # symptom_mappings = await get_existing_symptoms_mappings_task

    business_mappings = await get_business_id_mapping(csv_business_ids, db)
    symptom_mappings = await get_symptom_code_mapping(csv_symptom_codes, db)

    for row in data:

        business_id = int(row['Business ID'])
        if business_id not in existing_businesses_dict:
            business = Business(business_id=business_id, name=row['Business Name'])
            db.add(business)
            db.flush()
            # update dict with new record
            business_mappings[business_id] = business.id

        if row['Symptom Code'] not in existing_symptoms_dict:
            symptom = Symptom(code=row['Symptom Code'], name=row['Symptom Name'])
            db.add(symptom)
            db.flush()
            # update dict with new record
            symptom_mappings[row['Symptom Code']] = symptom.id

        # TODO: write logic to save is_diagnosed
        diagnosis = Diagnosis(is_diagnosed=True,
                              business_id=business_mappings[business_id],
                              symptom_id=symptom_mappings[row['Symptom Code']])
        diagnoses_to_insert.append(diagnosis)

    # using add_all instead of the Legacy API for bulk insert mappings
    # https://github.com/sqlalchemy/sqlalchemy/discussions/6935#discussioncomment-1233465
    db.add_all(diagnoses_to_insert)

    # Commit the changes to the database
    db.commit()

    # Close the session
    db.close()
