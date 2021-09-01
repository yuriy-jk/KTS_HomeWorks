import asyncio
import datetime
from aiohttp import web
from store.accessor import Accessor


async def name():
    time = datetime.datetime.now().time()
    return print(time)


class SchedulerStartAccessor(Accessor):
    def __init__(self, app: web.Application):
        super().__init__(app)
        self.scheduler_task = None

    async def _on_connect(self, _):
        self.scheduler_task = asyncio.create_task(
            self.store.scheduler.check_subscribes()
        )

    async def _on_disconnect(self, _) -> None:
        self.scheduler_task.cancel()
