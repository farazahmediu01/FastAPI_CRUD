from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
from models import Book

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


session_dependency = Annotated[Session, Depends(get_session)]


# from typing import AsyncGenerator
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# async def get_async_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session

# # async_session_dependency = Annotated[AsyncSession, Depends(get_async_session)]


# async def async_init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
