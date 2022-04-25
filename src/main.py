from fastapi import FastAPI
from src.db.database import Base, engine

app = FastAPI()

Base.metadata.create_all(engine)
