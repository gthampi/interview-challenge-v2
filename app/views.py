import csv
from http import HTTPStatus

from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

import controller

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from typing import Optional


router = APIRouter()


@router.get('/diagnoses', status_code=HTTPStatus.OK)
async def get(db: AsyncSession = Depends(controller.get_db),
              business_id: Optional[int] = Query(None, alias="business_id"),
              is_diagnosed: Optional[bool] = Query(None, alias="is_diagnosed")):
    try:
        diagnoses_data = await controller.get_diagnoses_by_params(db, business_id, is_diagnosed)
        return diagnoses_data

    except Exception as e:
        return {'Error': str(e)}


@router.post("/import_csv", status_code=HTTPStatus.CREATED)
async def post(file: UploadFile = File(...), db: AsyncSession = Depends(controller.get_db)):
    try:
        if file.content_type != 'text/csv':
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        # can do some kind of chunking/buffer if needed
        contents = await file.read()
        data = list(csv.DictReader(contents.decode('utf-8').splitlines()))

        await controller.update_db(data, db)

    except IOError:
        return JSONResponse(status_code=500, content={"message": "There was an error reading the file"})

    finally:
        await file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

