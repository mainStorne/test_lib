from fastapi import Depends, FastAPI, Request
from .db.setup import create_db_and_tables
from .api.api import api
from .conf import engine



{% if cookiecutter.is_local %}
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables(engine)
    yield
app = FastAPI(lifespan=lifespan)
{% else %}
app = FastAPI()
{% endif %}

app.include_router(api, prefix='/api')

