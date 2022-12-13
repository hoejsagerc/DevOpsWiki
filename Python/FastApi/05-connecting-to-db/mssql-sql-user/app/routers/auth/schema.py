# Importing standard python libs
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    first_name: str
    last_name: str
    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None