import asyncio
from datetime import datetime as dt
from apps.bot_user.models import Subscriptions, User
from store.accessor import Accessor


class SchedulerAccessor(Accessor):
    async def task(self, sub, now_time):
        sub_time = (sub.schedule.hour, sub.schedule.minute)
        if now_time == sub_time:
            user = await User.query.where(User.id == sub.user_id).gino.first()
            chat_id = user.chat_id
            links = await self.store.crawler.run(sub.tag)
            if len(links) != 0:
                await self.store.telegram.send_links(chat_id, links)

    async def check_subscribes(self):
        while True:
            await asyncio.sleep(0.5)
            subs = await Subscriptions.query.gino.all()
            now_time = (dt.now().hour, dt.now().minute)

            for sub in subs:
                asyncio.create_task(self.task(sub, now_time))

            await asyncio.sleep(60)
