import asyncio
from datetime import datetime as dt
import datetime
from itertools import product

from apps.bot_user.models import Subscriptions, User
from store.accessor import Accessor

import pytz

tzmoscow = pytz.timezone('Europe/Moscow')

BASE_URL = [
    "https://habr.com/ru/all/page1",
    # "https://habr.com/ru/all/page2",
    # 'https://habr.com/ru/all/page3'
]


class SchedulerAccessor(Accessor):

    async def set_last_update(self, sub):
        if sub.last_update is None:
            last_update = dt.now(tzmoscow) - datetime.timedelta(days=2)
            await sub.update(last_update=last_update.replace(tzinfo=None)).apply()
        else:
            pass

    async def get_user_chat_id(self, sub):
        user = await User.query.where(User.id == sub.user_id).gino.first()
        chat_id = user.chat_id
        return chat_id

    async def check_and_send_task(self, articles: list):
        while True:
            now_time = (dt.now(tzmoscow).hour, dt.now(tzmoscow).minute)
            subs = await Subscriptions.query.gino.all()

            for sub in subs:
                links = []
                await self.set_last_update(sub)
                sub_time = (sub.schedule.hour, sub.schedule.minute)
                if now_time == sub_time:
                    for article in articles:
                        if (sub.tag in article.tags) and (sub.last_update < article.date):
                            links.append(article.url)
                    chat_id = await self.get_user_chat_id(sub)
                    if len(links) != 0:
                        date = dt.now(tzmoscow)
                        db_date = date.replace(tzinfo=None)
                        await sub.update(last_update=db_date).apply()
                        await self.store.telegram.send_links(chat_id, sub.tag, links)
                    else:
                        await self.store.telegram.send_empty_links(chat_id, sub.tag)

    async def check_subscribes(self):
        while True:
            await asyncio.sleep(0.5)
            """запуск парсинг Хабра, получаем список статей articles с параметрами Task.url, Task.tag, Task.date"""
            articles = await self.store.crawler.run()

            """используем список статей для подписок юзеров"""
            asyncio.create_task(self.check_and_send_task(articles))

            await asyncio.sleep(60)
