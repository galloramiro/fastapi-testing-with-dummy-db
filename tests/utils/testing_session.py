import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import config
from src.repositories.interface import DatabaseSessionInterface


user = config.DATABASE_USER
password = config.DATABASE_PASSWORD
host = config.TEST_DATABASE_HOST
port = config.DATABASE_PORT
database_name = config.TEST_DATABASE_NAME
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=250,
    max_overflow=500,
    pool_pre_ping=True,
    pool_recycle=3600,
)


class DatabaseTestingSession(DatabaseSessionInterface):
    """Manage the local session"""

    def __init__(self) -> None:
        testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = testing_session()
