import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src import config


user = config.DATABASE_USER
password = config.DATABASE_PASSWORD
host = config.DATABASE_HOST
port = config.DATABASE_PORT
database = config.DATABASE_NAME
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(
	SQLALCHEMY_DATABASE_URL,
	pool_size=250,
	max_overflow=500,
	pool_pre_ping=True,
	pool_recycle=3600,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
