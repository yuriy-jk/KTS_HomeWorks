from typing import Optional

from aiohttp import web

from apps.admin_user.accessor import Session
from store import Store
from web.exceptions import NotAuthorized


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
