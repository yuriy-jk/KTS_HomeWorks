import asyncio
import os

from aiogram import Bot, Dispatcher
from aiohttp import web

from store.accessor import Accessor

API_TOKEN = os.environ['BOT_KEY']
# API_TOKEN = "1857420338:AAGJF00Eq57_4cQiFqQO55zAm_r_YFBr8EE"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


class BotAccessor(Accessor):
    def __init__(self, app: web.Application):
        super().__init__(app)
        self.bot_start_task = None

    async def _on_connect(self, _):
        self.bot_start_task = asyncio.create_task(dp.start_polling(dp))

    async def _on_disconnect(self, _) -> None:
        dp.stop_polling()
        self.bot_start_task.cancel()
