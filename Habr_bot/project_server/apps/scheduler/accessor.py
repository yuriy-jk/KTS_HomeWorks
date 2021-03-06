import asyncio
from datetime import datetime as dt
import datetime

from apps.bot_user.models import Subscriptions, User
from apps.scheduler.models import Article
from store.accessor import Accessor
import pytz

tzmoscow = pytz.timezone('Europe/Moscow')

BASE_URL = [
    "https://habr.com/ru/all/page1",
    # "https://habr.com/ru/all/page2",
    # 'https://habr.com/ru/all/page3'
]


class SchedulerAccessor(Accessor):

    async def set_last_update(self, sub: Subscriptions):
        if sub.last_update is None:
            last_update = dt.now(tzmoscow) - datetime.timedelta(days=2)
            await sub.update(last_update=last_update.replace(tzinfo=None)).apply()
        else:
            pass

    async def get_user_chat_id(self, sub: Subscriptions):
        user = await User.query.where(User.id == sub.user_id).gino.first()
        chat_id = user.chat_id
        return chat_id

    async def check_and_send_task(self):
        for i in range(60):
            now_time = dt.now(tzmoscow)
            time = datetime.time(now_time.hour, now_time.minute)
            subs = await Subscriptions.query.where(Subscriptions.schedule == time).gino.all()
            # subs = await Subscriptions.query.gino.all()
            if len(subs) > 0:
                for sub in subs:
                    links = []
                    await self.set_last_update(sub)
                    articles = await Article.query.where(
                        Article.tag.any(sub.tag)).where(
                        Article.date > sub.last_update).gino.all()
                    for article in articles:
                        date = dt.now(tzmoscow)
                        db_date = date.replace(tzinfo=None)
                        await sub.update(last_update=db_date).apply()
                        links.append(article.url)
                    chat_id = await self.get_user_chat_id(sub)
                    if len(links) != 0:
                        await self.store.telegram.send_links(chat_id, sub.tag, links)
                    else:
                        await self.store.telegram.send_empty_links(chat_id, sub.tag)
            await asyncio.sleep(60)

    async def check_subscribes(self):
        while True:
            await asyncio.sleep(0.5)
            """???????????? ?????????????? ??????????"""
            await self.store.crawler.run()

            """???????????????????? ???????????? ???????????? ?????? ???????????????? ????????????"""
            await self.check_and_send_task()



