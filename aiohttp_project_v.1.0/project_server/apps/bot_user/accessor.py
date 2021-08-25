
from typing import List

from apps.bot_user.models import User, Subscriptions
from web.exceptions import NotFound
from store.accessor import Accessor


async def user_with_subs(user: User, subs: List[Subscriptions]):
    for sub in subs:
        user.subscriptions[sub.tag] = sub.schedule
    return user


class UserAccessor(Accessor):

    @staticmethod
    async def list(params: dict) -> list:
        limit = None
        if 'limit' in params.keys():
            limit = params['limit']
        if 'q' in params.keys():
            users = await User.query.where(
                User.first_name == params['q'] or
                User.last_name == params['q']).limit(limit).gino.all()
        else:
            users = await User.query.limit(limit).gino.all()
        return users

    @staticmethod
    async def get(id: int) -> User:
        user = await User.query.where(User.id == id).gino.first()
        if user is None:
            raise NotFound
        user_subs = await Subscriptions.query.where(Subscriptions.user_id == user.id).gino.load(Subscriptions).all()
        user = await user_with_subs(user, user_subs)
        return user

    @staticmethod
    async def post(data) -> User:
        user = await User.query.where(User.id == int(data.id)).gino.first()
        if user is None:
            raise NotFound
        if data.is_banned:
            await user.update(is_banned=data.is_banned).apply()
        if data.subscriptions:
            user_subs = await Subscriptions.query.where(Subscriptions.user_id == user.id).gino.load(Subscriptions).all()
            tags = [sub.tag for sub in user_subs]
            for tag, schedule in data.subscriptions.items():
                if tag.lower() in tags:
                    sub = await Subscriptions.query.where(Subscriptions.user_id == user.id and
                                                          Subscriptions.tag == tag.lower()).gino.first()
                    await sub.update(schedule=schedule).apply()
                else:
                    await Subscriptions.create(user_id=user.id, tag=tag.lower(), schedule=schedule)
        user_subs = await Subscriptions.query.where(Subscriptions.user_id == user.id).gino.load(Subscriptions).all()
        user = await user_with_subs(user, user_subs)
        return user

    # @staticmethod
    # async def add_user(username: str, password: str, first_name: str, last_name: str,
    #                    subscriptions: Optional[Dict[str, datetime.datetime]]) -> User:
    #     is_user = await User.query.where(User.username == username).gino.first()
    #     if is_user is not None:
    #         raise AlreadyExists
    #     created = datetime.datetime.now()
    #
    #     async with db.transaction():
    #         try:
    #             user = await User.create(username=username, password=password, first_name=first_name,
    #                                      last_name=last_name, created=created, is_banned='False')
    #             if subscriptions:
    #                 for tag, schedule in subscriptions.items():
    #                     await Subscriptions.create(user_id=user.id, tag=tag.lower(), schedule=schedule)
    #             else:
    #                 pass
    #         except Exception:
    #             raise Error
    #     return user
