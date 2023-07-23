from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.models import Business, Symptom


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_business_id_mapping(ids_from_csv: set, db: AsyncSession):
    existing_businesses_statement = select(Business).filter(
        Business.business_id.in_(ids_from_csv)
    )
    existing_businesses = await db.execute(existing_businesses_statement)
    existing_businesses_dict = {
        business.business_id: business.id
        for business in existing_businesses.scalars().all()
    }
    return existing_businesses_dict


async def get_symptom_code_mapping(codes_from_csv: set, db: AsyncSession):
    existing_symptoms_statement = select(Symptom).filter(
        Symptom.code.in_(codes_from_csv)
    )
    existing_symptoms = await db.execute(existing_symptoms_statement)
    existing_symptoms_dict = {
        symptom.code: symptom.id for symptom in existing_symptoms.scalars().all()
    }
    return existing_symptoms_dict


def parse_is_diagnosed(value: str):
    value_lower = value.lower()
    if value_lower == "true" or value_lower == "yes":
        return True
    elif value_lower == "false" or value_lower == "no":
        return False
    raise ValueError("Invalid bool-like string for Symptom Diagnostic")
