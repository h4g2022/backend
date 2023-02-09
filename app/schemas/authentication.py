from enum import Enum
from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserType(str, Enum):
    patient = "patient"
    employer = "employer"


class UserBaseSchema(BaseModel):
    email: EmailStr


class UserLoginSchema(UserBaseSchema):
    password: str


class UserSchema(UserLoginSchema):
    type: UserType


class UserCreateResponseSchema(UserBaseSchema):
    status: str


class UserDataSchema(UserBaseSchema):
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
