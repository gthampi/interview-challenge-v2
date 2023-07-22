from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.models import Business, Symptom, Diagnosis


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_diagnoses_by_params(business_id, diagnostic, db: AsyncSession):
    pass


async def update_db(data, db: AsyncSession):
    # TODO: should we use pandas here?
    csv_business_ids, csv_symptom_codes = set(), set()
    for row in data:
        csv_business_ids.add(int(row['Business ID']))
        csv_symptom_codes.add(row['Symptom Code'])

    business_mappings = await get_business_id_mapping(csv_business_ids, db)
    symptom_mappings = await get_symptom_code_mapping(csv_symptom_codes, db)

    diagnoses_to_insert = []
    for row in data:

        business_id = int(row['Business ID'])
        if business_id not in business_mappings:
            business = Business(business_id=business_id, name=row['Business Name'])
            db.add(business)
            await db.flush()
            business_mappings[business_id] = business.id

        if row['Symptom Code'] not in symptom_mappings:
            symptom = Symptom(code=row['Symptom Code'], name=row['Symptom Name'])
            db.add(symptom)
            await db.flush()
            symptom_mappings[row['Symptom Code']] = symptom.id

        diagnosis = Diagnosis(is_diagnosed=parse_is_diagnosed(row['Symptom Diagnostic']),
                              business_id=business_mappings[business_id],
                              symptom_id=symptom_mappings[row['Symptom Code']])
        diagnoses_to_insert.append(diagnosis)

    # using add_all (orm) instead of the Legacy API (core) for bulk insert mappings
    # https://github.com/sqlalchemy/sqlalchemy/discussions/6935#discussioncomment-1233465
    db.add_all(diagnoses_to_insert)

    # Commit the changes to the database
    await db.commit()

    # Close the session
    await db.close()


async def get_business_id_mapping(ids_from_csv: set, db: AsyncSession):
    existing_businesses_statement = select(Business).filter(Business.business_id.in_(ids_from_csv))
    existing_businesses = await db.execute(existing_businesses_statement)
    existing_businesses_dict = {business.business_id: business.id for business in existing_businesses.scalars().all()}
    return existing_businesses_dict


async def get_symptom_code_mapping(codes_from_csv: set, db: AsyncSession):
    existing_symptoms_statement = select(Symptom).filter(Symptom.code.in_(codes_from_csv))
    existing_symptoms = await db.execute(existing_symptoms_statement)
    existing_symptoms_dict = {symptom.code: symptom.id for symptom in existing_symptoms.scalars().all()}
    return existing_symptoms_dict


def parse_is_diagnosed(value: str):
    value_lower = value.lower()
    if value_lower == "true" or value_lower == "yes":
        return True
    elif value_lower == "false" or value_lower == "no":
        return False
    raise ValueError("Invalid bool-like string for Symptom Diagnostic")
