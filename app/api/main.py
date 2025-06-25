# This is the point of entry to my api

from fastapi import FastAPI
from api.routes import router

api = FastAPI()

app.include_router(router)

