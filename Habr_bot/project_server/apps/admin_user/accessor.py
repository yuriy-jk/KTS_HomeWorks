import datetime
import uuid
from hashlib import md5
from typing import Optional
from apps.admin_user.models import Admin, Session
from web.exceptions import AlreadyExists, InvalidCredentials, NotAuthorized
from store.accessor import Accessor
import pytz

tzmoscow = pytz.timezone('Europe/Moscow')


class AdminAccessor(Accessor):
    @staticmethod
    async def add_user(
            username: str, password: str, first_name: str, last_name: str
    ) -> Admin:
        admin = await Admin.query.where(Admin.username == username).gino.first()
        if admin is not None:
            raise AlreadyExists
        date = datetime.datetime.now(tzmoscow)
        db_date = date.replace(tzinfo=None)
        return await Admin.create(
            username=username,
            password=md5(password.encode()).hexdigest(),
            first_name=first_name,
            last_name=last_name,
            created=db_date,
        )

    @staticmethod
    async def login(username: str, password: str) -> Admin:
        admin = await Admin.query.where(Admin.username == username).gino.first()
        if not admin:
            raise InvalidCredentials
        if admin.password != md5(password.encode()).hexdigest():
            raise InvalidCredentials
        return admin


class SessionAccessor(Accessor):
    @staticmethod
    async def generate_session(username: str) -> Session:
        session_id = uuid.uuid4().hex
        row = await Session.create(id=session_id, username=username)
        return row

    async def get_by_id(self, session_id) -> Optional[Session]:
        row = await Session.query.where(Session.id == session_id).gino.first()
        if not row:
            raise NotAuthorized
        return row
