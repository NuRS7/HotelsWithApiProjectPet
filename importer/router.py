import codecs
import csv
from typing import Literal

from fastapi import APIRouter, Depends, UploadFile

from exceptions import CannotAddDataToDatabase, CannotProcessCSV
from importer.utils import TABLE_MODEL_MAP, convert_csv_to_postgres_format
from users.dependencies import get_current_user

router = APIRouter(
    prefix="/import",
    tags=["Импорт данных в БД"],
)


@router.post(
    "/{table_name}",
    status_code=201,
    dependencies=[Depends(get_current_user)],
)
async def import_data_to_table(
    file: UploadFile,
    table_name: Literal["hotels", "rooms", "bookings"],
):
    ModelDAO = TABLE_MODEL_MAP[table_name]

    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'), delimiter=";")
    data = convert_csv_to_postgres_format(csvReader)
    file.file.close()
    if not data:
        raise CannotProcessCSV
    added_data = await ModelDAO.add_bulk(data)
    if not added_data:
        raise CannotAddDataToDatabase
