from sqlalchemy import Column, DateTime, Integer, String, func

from src.orm.database import Base


class Crop(Base):
    __tablename__ = "crops"

    id = Column(name="id", type_=Integer, primary_key=True)
    name = Column(name="name", type_=String(255), nullable=False)
    type = Column(name="type", type_=String(255), nullable=False)
    created_at = Column(
        name="created_at",
        type_=DateTime(timezone=False),
        server_default=func.now(),
        default=func.now(),
        nullable=False,
    )
    updated_at = Column(name="updated_at", type_=DateTime(timezone=False), onupdate=func.now())
