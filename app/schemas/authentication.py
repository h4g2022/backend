from enum import Enum
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserType(str, Enum):
    patient = 'patient'
    employer = 'employer'
    admin = 'admin'


class UserSchema(BaseModel):
    email: EmailStr
    password: str
    type: UserType


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserDataSchema(BaseModel):
    email: EmailStr
    type: UserType
