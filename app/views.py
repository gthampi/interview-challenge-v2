import csv

from fastapi.params import Depends
from sqlalchemy.orm import Session

import controller
import pandas as pd

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from typing import Optional


router = APIRouter()


@router.get('/diagnosis')
async def get(business_id: Optional[int], diagnostic: Optional[bool]):  # do we need default ?
    try:
        return {"Health OK"}

    except Exception as e:
        return {'Error: ' + str(e)}


@router.post("/import_csv")  # make this put
async def post(file: UploadFile = File(...), db: Session = Depends(controller.get_db)):
    # TODO: can do some kind of chunking or use shutil for memory buffer
    try:
        # Check if the file extension is allowed
        if file.content_type != 'text/csv':     # 'application/csv'
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        contents = await file.read()
        # df = pd.DataFrame.from_records(contents)
        data = list(csv.DictReader(contents.decode('utf-8').splitlines()))

        controller.update_db(data, db)

    except IOError:
        return JSONResponse(status_code=500, content={"message": "There was an error reading the file"})

    finally:
        await file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
    # with open(f"{file.filename}", "wb") as f:
    #     f.write(await file.read())
    #
    # with open(f"{file.filename}", newline="") as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     items = [Item(name=row["name"]) for row in reader]
    #
    # # Delete the uploaded CSV file after processing
    # os.remove(f"{file.filename}")
    #
    # # Insert items into the database
    # db = SessionLocal()
    # db.add_all(items)
    # db.commit()
    # db.close()
    #
    # return {"message": f"{len(items)} items imported successfully!"}
