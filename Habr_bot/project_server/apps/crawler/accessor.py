import asyncio
import datetime
from asyncio import Queue
from dataclasses import dataclass
from typing import List, Optional

import aiohttp
import pytz
from bs4 import BeautifulSoup
from dateutil import parser
from yarl import URL

from store.accessor import Accessor
from apps.scheduler.models import Article

domen = "https://habr.com"

tzmoscow = pytz.timezone('Europe/Moscow')


@dataclass
class Task:
    url: URL
    date: Optional[datetime.datetime] = None
    tags: Optional[List[str]] = None

    def link_parser(self, data: str):
        soup = BeautifulSoup(data, "lxml")
        res = []
        for elem in soup.find_all(attrs={'class': 'tm-article-snippet'}):
            url = URL(elem.contents[1].contents[0].get('href'))
            date = parser.isoparse(elem.next.contents[0].contents[1].contents[0].get('datetime'))
            date_tz = date.astimezone(tzmoscow).replace(tzinfo=None)
            res.append(Task(url=url, date=date_tz))
        return res

    def tag_parser(self, data: str):
        soup = BeautifulSoup(data, "lxml")
        self.tags = []
        _items = soup.find_all(attrs={"class": "tm-article-body__tags-links"})
        _tags = _items[0].contents
        for i in range(1, len(_tags)):
            self.tags.append(_tags[i].text.lower())
        return self

    async def perform(self, pool: "Pool"):
        if self.url.host is None:
            self.url = URL(f"{domen}{self.url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                data = await resp.text()
                if "https://habr.com/ru/all/page" in str(self.url):
                    res = await asyncio.get_running_loop().run_in_executor(
                        None, self.link_parser, data
                    )
                    for task in res:
                        await pool.put(task)
                else:
                    task = await asyncio.get_running_loop().run_in_executor(
                        None, self.tag_parser, data
                    )
                    article = await Article.query.where(Article.url == str(task.url)).gino.first()
                    if article is None:
                        await Article.create(url=str(task.url),
                                             date=task.date,
                                             tag=task.tags)


class Pool:
    def __init__(self, max_rate: int, interval: int, queue: Queue):
        self._queue = queue
        self._scheduler_task = None
        self._concurrent_workers = 0
        self._stop_event = asyncio.Event()
        self._sem = asyncio.Semaphore(8)
        self.is_running = False
        self.max_rate = max_rate
        self.interval = interval

    async def _scheduler(self):
        while self.is_running:
            for _ in range(self.max_rate):
                async with self._sem:
                    task: Task = await self._queue.get()
                    asyncio.create_task(self._worker(task))
            await asyncio.sleep(self.interval)

    async def _worker(self, task: Task):
        self._concurrent_workers += 1
        async with self._sem:
            await task.perform(self)
            self._queue.task_done()
        self._concurrent_workers -= 1
        if not self.is_running and self._concurrent_workers == 0:
            self._stop_event.set()

    def start(self):
        self.is_running = True
        self._scheduler_task = asyncio.create_task(self._scheduler())

    async def put(self, task: Task):
        await self._queue.put(task)

    async def join(self):
        await self._queue.join()


BASE_URL = [
    "https://habr.com/ru/all/page1",
    # "https://habr.com/ru/all/page2",
    # 'https://habr.com/ru/all/page3'
]


class CrawlerAccessor(Accessor):

    async def prepare(self):

        queue = asyncio.Queue()
        pool = Pool(15, 1, queue)
        pool.start()
        for link in BASE_URL:
            await pool.put(Task(URL(link)))
        await queue.join()

    async def run(self):
        await self.prepare()

