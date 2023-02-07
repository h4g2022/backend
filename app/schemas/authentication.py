from enum import Enum
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserType(str, Enum):
    patient = "patient"
    employer = "employer"


class UserSchema(BaseModel):
    email: EmailStr
    password: str
    type: UserType


class UserCreateResponseSchema(BaseModel):
    email: EmailStr
    status: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserDataSchema(BaseModel):
    email: EmailStr
    type: UserType


class UserLoginResponseSchema(BaseModel):
    data: UserDataSchema
    access_token: str
    refresh_token: str
    token_type: str


class UserRefreshSchema(BaseModel):
    refresh_token: str


class UserRefreshResponseSchema(BaseModel):
    access_token: str
    token_type: str
