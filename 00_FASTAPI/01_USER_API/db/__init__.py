from fastapi import Depends
from typing import Annotated
from sqlmodel import create_engine, Session


sqlite_url = "sqlite:///users.db"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
