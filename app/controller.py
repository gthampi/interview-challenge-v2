from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Business, Symptom, Diagnosis
from app.util import (
    parse_is_diagnosed,
    get_symptom_code_mapping,
    get_business_id_mapping,
)


async def get_diagnoses_by_params(
    db: AsyncSession,
    business_id: Optional[int] = None,
    is_diagnosed: Optional[bool] = None,
):
    diagnoses_query = select(Diagnosis)
    if is_diagnosed is not None:
        diagnoses_query = diagnoses_query.filter(Diagnosis.is_diagnosed == is_diagnosed)
    if business_id is not None:
        diagnoses_query = diagnoses_query.join(Business).filter(
            Business.business_id == business_id
        )
    diagnoses_query.join(Symptom)

    results = await db.execute(diagnoses_query)
    diagnoses = results.scalars().all()

    # move to a separate file and obj later
    return {"data": diagnoses}


async def update_db(data, db: AsyncSession):
    # TODO: should we use pandas here?
    csv_business_ids, csv_symptom_codes = set(), set()
    for row in data:
        csv_business_ids.add(int(row["Business ID"]))
        csv_symptom_codes.add(row["Symptom Code"])

    business_mappings = await get_business_id_mapping(csv_business_ids, db)
    symptom_mappings = await get_symptom_code_mapping(csv_symptom_codes, db)

    diagnoses_to_insert = []
    for row in data:
        business_id = int(row["Business ID"])
        if business_id not in business_mappings:
            business = Business(business_id=business_id, name=row["Business Name"])
            db.add(business)
            await db.flush()
            business_mappings[business_id] = business.id

        if row["Symptom Code"] not in symptom_mappings:
            symptom = Symptom(code=row["Symptom Code"], name=row["Symptom Name"])
            db.add(symptom)
            await db.flush()
            symptom_mappings[row["Symptom Code"]] = symptom.id

        diagnosis = Diagnosis(
            is_diagnosed=parse_is_diagnosed(row["Symptom Diagnostic"]),
            business_id=business_mappings[business_id],
            symptom_id=symptom_mappings[row["Symptom Code"]],
        )
        diagnoses_to_insert.append(diagnosis)

    # using add_all (orm) instead of the Legacy API (core) for bulk insert mappings
    # https://github.com/sqlalchemy/sqlalchemy/discussions/6935#discussioncomment-1233465
    db.add_all(diagnoses_to_insert)

    # Commit the changes to the database
    await db.commit()

    # Close the session
    await db.close()
