from dataclasses import dataclass
from typing import Optional

import asyncpg

from settings import config
from store.accessor import Accessor


@dataclass
class PostgresConfig:
    host: str
    port: int
    database: str
    username: str
    password: str

    @property
    def dsn(self):
        return (
            f'postgres://{self.username}:{self.password}@'
            f'{self.host}:{self.port}/{self.database}'
        )


class PgAccessor(Accessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = PostgresConfig(**config["postgres"])
        self.conn: Optional[asyncpg.Connection] = None

    async def _on_connect(self, _):
        self.conn = await asyncpg.connect(self.config.dsn)

    async def _on_disconnect(self, _) -> None:
        await self.conn.close()
