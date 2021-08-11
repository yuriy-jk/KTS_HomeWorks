import uuid
from dataclasses import dataclass
from hashlib import md5
import datetime
from typing import Optional

from project_server.web.exceptions import AlreadyExists, InvalidCredentials


@dataclass
class BaseUser:
    username: str
    password: str
    first_name: str
    last_name: str
    created: datetime.datetime


@dataclass
class Session:
    id: str
    username: str


@dataclass
class AdminUser(BaseUser):
    pass


password = 'first'
database = {'first': AdminUser(username='first', password=md5(password.encode()).hexdigest(), first_name='first',
                               last_name='first', created=datetime.datetime(2021, 8, 8, 17, 12, 0, 423512))}


class AdminUserAccessor:

    @staticmethod
    def add_user(username: str, password: str, first_name: str, last_name: str) -> AdminUser:
        if username in database:
            raise AlreadyExists
        created = datetime.datetime.now()
        database[username] = AdminUser(username, md5(password.encode()).hexdigest(), first_name, last_name, created)
        return database[username]

    @staticmethod
    def login(username: str, password: str) -> AdminUser:
        if username in database:
            admin_user = database[username]
            if admin_user.password == md5(password.encode()).hexdigest():
                return admin_user
        raise InvalidCredentials


class SessionAccessor:
    def __init__(self):
        self.database = {}

    def generate_session(self, username: str) -> Session:
        session_id = uuid.uuid4().hex
        session = Session(session_id, username)
        self.database[session_id] = session
        return session

    def get_by_id(self, session_id) -> Optional[Session]:
        return self.database.get(session_id)
