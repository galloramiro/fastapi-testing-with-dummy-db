from sqlalchemy.orm import Session

from src.orm.models import Crop
from src.schemas import CropRequest


class CropRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, crop: CropRequest):
        """We strongly recomend to use this function with the
        DatabaseSession.get_session() context manager.
        Because this function will change the db.
        """
        crop = Crop(**crop.dict())
        self.session.add(crop)
        self.session.commit()
        self.session.refresh(crop)

        return crop

    def get_all(self):
        return self.session.query(Crop).all()
