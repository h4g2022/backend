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
    registered: bool
    user_type: UserType
    access_token: str
    token_type: str


class StatusEnum(str, Enum):
    success = "success"
    failure = "failure"


class LogoutResponseSchema(BaseModel):
    status: StatusEnum
