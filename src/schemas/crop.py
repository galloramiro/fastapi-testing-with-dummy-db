from datetime import datetime

from pydantic import BaseModel


class CropResponse(BaseModel):
    id: int
    name: str
    type: str
    created_at: datetime
    updated_at: str

    class Config:
        orm_mode = True


class CropRequest(BaseModel):
    name: str
    type: str
