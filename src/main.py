from fastapi import FastAPI
from src.orm import database


def init_api():
    app = FastAPI()
    database.Base.metadata.create_all(database.engine)
    return app


app: FastAPI = init_api()
