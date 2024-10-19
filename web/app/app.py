from fastapi import FastAPI

from .api.api import api

app = FastAPI()

app.include_router(api, prefix='/api')
