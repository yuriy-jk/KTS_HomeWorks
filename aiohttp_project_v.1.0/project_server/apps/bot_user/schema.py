import datetime
from typing import Dict, Optional

from marshmallow_dataclass import dataclass

from web.schema import BaseSchema


@dataclass
class RequestBotUserSchema(BaseSchema):
    username: str
    password: str
    first_name: str
    last_name: str
    subscriptions: Optional[Dict[str, datetime.time]]


@dataclass
class ResponseBotUserSchema(BaseSchema):
    username: str
    first_name: str
    last_name: str
    created: datetime.datetime
    is_banned: str
    subscriptions: Dict[str, datetime.time]


@dataclass
class SubscriptionsSchema(BaseSchema):
    user_id: str
    tag: str
    schedule: datetime.time


@dataclass
class UpdateBotUserSchema(BaseSchema):
    id: int
    is_banned: Optional[str]
    subscriptions: Optional[Dict[str, datetime.time]]


@dataclass
class GetBotUserSchema(BaseSchema):
    id: int


@dataclass
class ListBotUserSchemaResponse(BaseSchema):
    id: int
    username: str
    first_name: str
    last_name: str
    created: datetime.datetime


@dataclass
class ListBotUserSchemaRequest(BaseSchema):
    limit: int
    q: str
