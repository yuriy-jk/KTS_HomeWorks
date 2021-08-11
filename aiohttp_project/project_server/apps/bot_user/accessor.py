from dataclasses import dataclass
from hashlib import md5
import datetime
from typing import Optional, List, Dict

from project_server.apps.admin_user.accessor import BaseUser
from project_server.web.exceptions import AlreadyExists, InvalidCredentials, NotFound


@dataclass
class BotUser(BaseUser):
    id: int
    is_banned: bool
    subscriptions: Dict[str, datetime.time]


bot_user_database = {}
id = 0


class BotUserAccessor:

    @staticmethod
    def add_user(username: str, password: str, first_name: str, last_name: str,
                 subscriptions: Dict[str, datetime.time]) -> BotUser:
        if username in bot_user_database:
            raise AlreadyExists
        created = datetime.datetime.now()
        global id
        id += 1
        bot_user_database[username] = BotUser(username, md5(password.encode()).hexdigest(), first_name, last_name,
                                              created, subscriptions=subscriptions, id=id, is_banned=False)
        bot_user_database[int(id)] = username
        return bot_user_database[username]

    def list(self):
        pass

    @staticmethod
    def get(id: int):
        try:
            username = bot_user_database[id]
        except "NotFoundError":
            raise NotFound
        return bot_user_database[username]

    @staticmethod
    def post(**kwargs):
        data = kwargs
        try:
            username = bot_user_database[data['id']]
        except "NotFoundError":
            raise NotFound
        user = bot_user_database[username]
        if 'is_banned' in data:
            user.is_banned = data['is_banned']
        if 'subscriptions' in data:
            for k, v in data['subscriptions'].items():
                if k in user.subscriptions:
                    user.subscriptions[k] = v
                else:
                    user.subscriptions[k] = v

        return bot_user_database[username]
