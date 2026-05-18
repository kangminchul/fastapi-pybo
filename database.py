#import contextlib

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

# 비동기 디비
#from sqlalchemy.ext.asyncio import create_async_engine, async_session, AsyncSession

config =  Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

#SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

#동기 디비
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
naming_convention = {
    "ix" : 'ix_%(column_0_labl)s',
    "uq" : "uq_%(table_name)s_%(column_0_name)s",
    "ck" : "ck_%(table_name)s_%(column_0_name)s",
    "fk" : "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk" : "pk_%(table_name)s",
}
Base.metadata = MetaData(naming_convention=naming_convention)


# @contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
         yield db
    finally:
        db.close()


#비동기 디비
# async_engine = create_async_engine("sqlite+aiosqlite:///./myapi.db")
# async def get_async_db():
#     db = AsyncSession(bind=async_engine)
#     try:
#         yield db
#     finally:
#         await db.close()
