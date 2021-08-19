import datetime
from typing import Dict, Optional

from web.exceptions import AlreadyExists, NotFound
from apps.bot_user.models import User, Subscriptions


class UserAccessor:

    @staticmethod
    async def add_user(username: str, password: str, first_name: str, last_name: str,
                       subscriptions: Optional[Dict[str, datetime.datetime]]) -> User:
        is_user = await User.query.where(User.username == username).gino.first()
        if is_user is not None:
            raise AlreadyExists
        created = datetime.datetime.now()
        user = await User.create(username=username, password=password, first_name=first_name,
                                 last_name=last_name, created=created, is_banned='False')
        user_id = user.id
        if subscriptions:
            for k, v in subscriptions.items():
                await Subscriptions.create(user_id=user_id, tag=k.lower(), schedule=v)
        else:
            pass
        return user

    @staticmethod
    async def list(data) -> list:
        limit = None
        if 'limit' in data.keys():
            limit = data['limit'][0]
        if 'q' in data.keys():
            users = await User.query.where(
                User.first_name == data['q'][0] or
                User.last_name == data['q'][0]).limit(limit).gino.all()
        else:
            users = await User.query.limit(limit).gino.all()
        return users

    @staticmethod
    async def get(id: int) -> User:
        user = await User.query.where(User.id == id).gino.first()
        subs = await Subscriptions.select('tag', 'schedule').where(Subscriptions.user_id == id).gino.all()
        subs = {i[0]: i[1] for i in subs}
        await user.update_subscriptions(subs)
        if user is None:
            raise NotFound
        return user

    @staticmethod
    async def post(data) -> User:
        user = await User.query.where(User.id == int(data.id)).gino.first()
        if user is None:
            raise NotFound
        if data.is_banned:
            await user.update(is_banned=data.is_banned).apply()
        if data.subscriptions:
            user_subs = await Subscriptions.select('tag').where(Subscriptions.user_id == user.id).gino.all()
            user_subs = [i[0] for i in user_subs]
            for k, v in data.subscriptions.items():
                if k.lower() in user_subs:
                    sub = await Subscriptions.query.where(Subscriptions.user_id == user.id and
                                                          Subscriptions.tag == k.lower()).gino.first()
                    await sub.update(schedule=v).apply()
                else:
                    await Subscriptions.create(user_id=user.id, tag=k.lower(), schedule=v)
        subs = await Subscriptions.select('tag', 'schedule').where(Subscriptions.user_id == user.id).gino.all()
        subs = {i[0]: i[1] for i in subs}
        await user.update_subscriptions(subs)
        return user
