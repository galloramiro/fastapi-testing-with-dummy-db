from typing import List

from fastapi import APIRouter, Depends

from src.repositories import DatabaseSession, DatabaseSessionInterface
from src.repositories.crop import CropRepository
from src.schemas import CropRequest, CropResponse

CROP_TAG = "crop"
crop_router = APIRouter(tags=[CROP_TAG], prefix=f"/{CROP_TAG}")


@crop_router.post("", response_model=CropResponse)
async def save_crop(crop: CropRequest, database: DatabaseSessionInterface = Depends(DatabaseSession)):
    with database.get_session() as session:
        repository = CropRepository(session=session)
        saved_crop = repository.save(crop=crop)
        saved_crop = CropResponse.from_orm(saved_crop)
    return saved_crop


@crop_router.get("", response_model=List[CropResponse])
async def get_all(database: DatabaseSessionInterface = Depends(DatabaseSession)):
    repository = CropRepository(session=database.session)
    return repository.get_all()
