from fastapi import FastAPI
from src.orm import database
from src.routes import crop_router


def init_api():
    app = FastAPI()
    app.include_router(crop_router)
    return app


app: FastAPI = init_api()
