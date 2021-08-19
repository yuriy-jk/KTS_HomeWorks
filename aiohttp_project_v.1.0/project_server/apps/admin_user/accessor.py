import datetime
import uuid
from hashlib import md5
from typing import Optional

from apps.admin_user.models import Admin, Session
from web.exceptions import AlreadyExists, InvalidCredentials, NotAuthorized


class AdminAccessor:

    @staticmethod
    async def add_user(username: str, password: str, first_name: str, last_name: str) -> Admin:
        admin = await Admin.query.where(Admin.username == username).gino.first()
        if admin is not None:
            raise AlreadyExists
        created = datetime.datetime.now()
        return await Admin.create(username=username, password=md5(password.encode()).hexdigest(), first_name=first_name,
                                  last_name=last_name, created=created)

    @staticmethod
    async def login(username: str, password: str) -> Admin:
        admin = await Admin.query.where(Admin.username == username).gino.first()
        if not admin:
            raise InvalidCredentials
        if admin.password != md5(password.encode()).hexdigest():
            raise InvalidCredentials
        return admin


class SessionAccessor:

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
