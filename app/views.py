import csv
from http import HTTPStatus

from fastapi.params import Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

import controller
import pandas as pd

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from typing import Optional


router = APIRouter()


@router.get('/diagnoses')
async def get(business_id: Optional[int] = Query(None, alias="business_id"),
              diagnostic: Optional[bool] = Query(None, alias="diagnostic"),
              db: AsyncSession = Depends(controller.get_db)):
    try:
        # Call the function to get the data from the database based on the provided parameters
        diagnoses_data = controller.get_diagnoses_by_params(business_id, diagnostic, db)
        return diagnoses_data

    except Exception as e:
        return {'Error': str(e)}


@router.post("/import_csv", status_code=HTTPStatus.CREATED)  # make this put
async def post(file: UploadFile = File(...), db: AsyncSession = Depends(controller.get_db)):
    # TODO: can do some kind of chunking or use shutil for memory buffer
    try:
        if file.content_type != 'text/csv':
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        contents = await file.read()
        # df = pd.DataFrame.from_records(contents)
        data = list(csv.DictReader(contents.decode('utf-8').splitlines()))

        await controller.update_db(data, db)

    except IOError:
        return JSONResponse(status_code=500, content={"message": "There was an error reading the file"})

    finally:
        await file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

