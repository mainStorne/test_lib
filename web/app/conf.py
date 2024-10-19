from web.settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

settings = Settings()
SECRET = 'SECRET'

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={'target_session_attrs': "read-write"})
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
