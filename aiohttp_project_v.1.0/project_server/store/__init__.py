from aiohttp import web


class Store:

    def __init__(self, app: web.Application):
        from store.pg import PgAccessor
        from store.gino import GinoAccessor

        self.pg = PgAccessor(app)
        self.gino = GinoAccessor(app)

        from apps.admin_user.accessor import AdminAccessor, SessionAccessor
        from apps.bot_user.accessor import UserAccessor

        self.admin = AdminAccessor(app)
        self.session = SessionAccessor(app)
        self.bot_user = UserAccessor(app)

        from store.bot import BotAccessor
        from store.telegramm import TelegrammAccessor
        self.telegramm = TelegrammAccessor(app)
        self.bot = BotAccessor(app)

    def setup(self, ):
        self.pg.setup()
        self.gino.setup()
        self.bot.setup()
