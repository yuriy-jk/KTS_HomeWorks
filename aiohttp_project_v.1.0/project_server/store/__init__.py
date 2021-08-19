from aiohttp import web


class Store:

    def __init__(self, app: web.Application):
        from store.pg import PgAccessor
        from store.gino import GinoAccessor

        self.pg = PgAccessor(app)
        self.gino = GinoAccessor(app)

        from apps.admin_user.accessor import AdminAccessor, SessionAccessor
        from apps.bot_user.accessor import UserAccessor

        self.admin = AdminAccessor()
        self.session = SessionAccessor()
        self.bot_user = UserAccessor()

    def setup(self, ):
        self.pg.setup()
        self.gino.setup()
