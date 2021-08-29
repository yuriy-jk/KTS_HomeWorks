import asyncio
from datetime import datetime as dt
import datetime
from apps.bot_user.models import Subscriptions, User
from store.accessor import Accessor

import pytz

tzmoscow = pytz.timezone('Europe/Moscow')


class SchedulerAccessor(Accessor):

    async def task(self, sub: Subscriptions):
        user = await User.query.where(User.id == sub.user_id).gino.first()
        chat_id = user.chat_id

        if sub.last_update is None:
            last_update = dt.now(tzmoscow) - datetime.timedelta(days=2)
            await sub.update(last_update=last_update.replace(tzinfo=None)).apply()
        links = await self.store.crawler.run(sub.tag, sub.last_update)

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
            subs = await Subscriptions.query.gino.all()
            now_time = (dt.now(tzmoscow).hour, dt.now(tzmoscow).minute)
            for sub in subs:
                sub_time = (sub.schedule.hour, sub.schedule.minute)
                if now_time == sub_time:
                    asyncio.create_task(self.task(sub))

            await asyncio.sleep(60)
