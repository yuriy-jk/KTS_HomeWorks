from aiohttp import web

from store import Store


class Accessor:
    def __init__(self, app: web.Application):
        self.app = app

    @property
    def store(self) -> Store:
        return self.app["store"]

    def setup(self):
        self.app.on_startup.append(self._on_connect)
        self.app.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, _):
        pass

    async def _on_disconnect(self, _) -> None:
        pass
