from hashlib import md5

from project_server.apps.admin_user.accessor import AdminUserAccessor, SessionAccessor
from project_server.apps.bot_user.accessor import BotUserAccessor


class Store:

    def __init__(self):

        self.admin = AdminUserAccessor()
        self.session = SessionAccessor()
        self.bot_user = BotUserAccessor()

