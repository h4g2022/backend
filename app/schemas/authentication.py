from enum import Enum
from pydantic import BaseModel


class UserType(str, Enum):
    patient = 'patient'
    employer = 'employer'
    admin = 'admin'


class UserSchema(BaseModel):
    email: str
    password: str
    type: UserType


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserDataSchema(BaseModel):
    email: str
    type: UserType
