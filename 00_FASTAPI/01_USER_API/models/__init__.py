from sqlmodel import Field, SQLModel, TIMESTAMP, Column, text
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, unique=True, nullable=False)
    firstName: str = Field(nullable=False, min_length=3, max_length=15)
    lastName: str = Field(nullable=False, min_length=3, max_length=15)
    password: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    username: str = Field(nullable=False, unique=True)
    avatar: str = Field(nullable=True, default='http://127.0.0.1:8000/storage/default.png')
    verified: bool = Field(nullable=False, default=False)
    loggedIn: bool = Field(nullable=False, default=False)
    
    # verification
    verificationToken: str = Field(nullable=False, default='000000')
    verificationTokenCreateTimestamp: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))

    # timestamps
    createdAt: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updatedAt: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))


