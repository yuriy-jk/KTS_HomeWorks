from gino import Gino

from settings import config
from store.accessor import Accessor
from store.pg import PostgresConfig

db = Gino()


class GinoAccessor(Accessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = PostgresConfig(**config["postgres"])

    async def _on_connect(self, _):
        await db.set_bind(self.config.dsn)

    async def _on_disconnect(self, _) -> None:
        await db.pop_bind().close()
