import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .api.api import api

app = FastAPI()

app.include_router(api, prefix='/api')


def openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title='Api', version='0.0.1', routes=app.routes)
    return schema


app.openapi = openapi


