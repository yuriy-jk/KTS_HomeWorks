from typing import Optional

from aiohttp import web

from project_server.apps.admin_user.accessor import Session
from project_server.store import Store
from project_server.web.exceptions import NotAuthorized


class BaseView(web.View):
    @property
    def store(self) -> Store:
        return self.request.app["store"]

    @property
    def session(self) -> Optional[Session]:
        return self.request.get("session")


def require_auth(func):
    async def wrapper(self, *args, **kwargs):
        if not self.session:
            raise NotAuthorized
        return await func(self, *args, **kwargs)

    return wrapper
