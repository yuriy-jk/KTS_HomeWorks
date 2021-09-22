from aiohttp import web


class Store:
    def __init__(self, app: web.Application):
        from store.pg import PgAccessor
        from store.gino import GinoAccessor
        from store.bot import BotAccessor
        from store.scheduler import SchedulerStartAccessor

        self.pg = PgAccessor(app)
        self.gino = GinoAccessor(app)
        self.bot = BotAccessor(app)
        self.scheduler_start = SchedulerStartAccessor(app)

        from apps.admin_user.accessor import AdminAccessor, SessionAccessor
        from apps.bot_user.accessor import UserAccessor
        from apps.telegram.accessor import TelegramAccessor
        from apps.scheduler.accessor import SchedulerAccessor
        from apps.crawler.accessor import CrawlerAccessor

        self.admin = AdminAccessor(app)
        self.session = SessionAccessor(app)
        self.bot_user = UserAccessor(app)
        self.telegram = TelegramAccessor(app)
        self.scheduler = SchedulerAccessor(app)
        self.crawler = CrawlerAccessor(app)

    def setup(
        self,
    ):
        self.pg.setup()
        self.gino.setup()
        self.bot.setup()
        self.scheduler_start.setup()
