from fastapi import Depends, FastAPI, Request
from .db.setup import create_db_and_tables
from .api.api import api
from .conf import engine




app = FastAPI()


app.include_router(api, prefix='/api')

