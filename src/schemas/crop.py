from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CropResponse(BaseModel):
    id: int
    name: str
    type: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class CropRequest(BaseModel):
    name: str
    type: str
