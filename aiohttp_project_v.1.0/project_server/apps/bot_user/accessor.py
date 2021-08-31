from typing import List
from apps.bot_user.models import User, Subscriptions
from apps.bot_user.schema import ListBotUserSchemaRequest
from web.exceptions import NotFound
from store.accessor import Accessor


async def user_with_subs(user: User, subs: List[Subscriptions]):
    for sub in subs:
        user.subscriptions[sub.tag] = sub.schedule
    return user


class UserAccessor(Accessor):
    @staticmethod
    async def list(data: ListBotUserSchemaRequest) -> list:
        if data.q is not None:
            users = (
                await User.query.where(
                    User.first_name == data.q or User.last_name == data.q
                )
                    .limit(data.limit)
                    .gino.all()
            )
        else:
            users = await User.query.limit(data.limit).gino.all()
        return users

    @staticmethod
    async def get(id: int) -> User:
        user = await User.query.where(User.id == id).gino.first()
        if user is None:
            raise NotFound
        user_subs = (
            await Subscriptions.query.where(Subscriptions.user_id == user.id)
                .gino.load(Subscriptions)
                .all()
        )
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
            user_subs = (
                await Subscriptions.select("tag")
                    .where(Subscriptions.user_id == user.id)
                    .gino.all()
            )
            tags = [sub.tag for sub in user_subs]
            for new_tag, schedule in data.subscriptions.items():
                if new_tag.lower() in tags:
                    sub = (
                        await Subscriptions.query.where(
                            Subscriptions.user_id == user.id
                        )
                            .where(Subscriptions.tag == new_tag.lower())
                            .gino.first()
                    )
                    await sub.update(schedule=schedule).apply()
                else:
                    await Subscriptions.create(
                        user_id=user.id, tag=new_tag.lower(), schedule=schedule
                    )
        user_subs = (
            await Subscriptions.query.where(Subscriptions.user_id == user.id)
                .gino.load(Subscriptions)
                .all()
        )
        user = await user_with_subs(user, user_subs)
        return user

    # @staticmethod
    # async def add_user(
    #         username: str,
    #         password: str,
    #         first_name: str,
    #         last_name: str,
    #         subscriptions: Optional[Dict[str, datetime.time]],
    # ) -> User:
    #     is_user = await User.query.where(User.username == username).gino.first()
    #     if is_user is not None:
    #         raise AlreadyExists
    #     created = datetime.datetime.now()
    #
    #     async with db.transaction():
    #         try:
    #             user = await User.create(
    #                 username=username,
    #                 password=password,
    #                 first_name=first_name,
    #                 last_name=last_name,
    #                 created=created,
    #                 is_banned="False",
    #             )
    #             if subscriptions:
    #                 for tag, schedule in subscriptions.items():
    #                     await Subscriptions.create(
    #                         user_id=user.id, tag=tag.lower(), schedule=schedule
    #                     )
    #             else:
    #                 pass
    #         except Exception:
    #             raise Error
    #     return user
