import datetime

from marshmallow_dataclass import dataclass

from web.schema import BaseSchema


@dataclass
class Session(BaseSchema):
    id: str
    username: str


@dataclass
class LoginSchema(BaseSchema):
    username: str
    password: str


@dataclass
class ResponseSchema(BaseSchema):
    username: str
    first_name: str
    last_name: str
    created: datetime.datetime


@dataclass
class RequestSchema(BaseSchema):
    username: str
    password: str
    first_name: str
    last_name: str
