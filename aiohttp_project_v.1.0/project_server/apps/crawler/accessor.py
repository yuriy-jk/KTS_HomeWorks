import asyncio
from asyncio import Queue
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup
from yarl import URL

from store.accessor import Accessor

domen = "https://habr.com"
tags = None
finded_links = []


@dataclass
class Task:
    url: URL

    def link_parser(self, data):
        soup = BeautifulSoup(data, "lxml")
        res = []
        for link in soup.find_all(attrs={"class": "tm-article-snippet__title-link"}):
            url = URL(link.get("href"))
            res.append(Task(url))
        return res

    def tag_parser(self, data, url):
        soup = BeautifulSoup(data, "lxml")
        for tag in soup.find_all(attrs={"class": "tm-article-body__tags-item"}):
            if tag.text.lower() in tags:
                # print(url)
                finded_links.append(url)
                return True

    async def perform(self, pool: "Pool"):
        if self.url.host is None:
            self.url = URL(f"{domen}{self.url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                # print(self.url, resp.status)
                data = await resp.text()
                if "https://habr.com/ru/all/page" in str(self.url):
                    res = await asyncio.get_running_loop().run_in_executor(
                        None, self.link_parser, data
                    )
                    for task in res:
                        await pool.put(task)
                else:
                    await asyncio.get_running_loop().run_in_executor(
                        None, self.tag_parser, data, self.url
                    )


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
    "https://habr.com/ru/all/page2",
    # 'https://habr.com/ru/all/page3'
]


class CrawlerAccessor(Accessor):
    async def prepare(self, user_tags):
        global tags
        tags = user_tags
        global finded_links
        finded_links = []

        queue = asyncio.Queue()
        pool = Pool(15, 1, queue)
        pool.start()
        for link in BASE_URL:
            await pool.put(Task(URL(link)))
        await queue.join()

    async def run(self, user_tags):
        await self.prepare(user_tags)
        return finded_links


# user_tags = ['microsoft', 'kts', 'python', 'data science', 'java', 'design']
# crawler = CrawlerAccessor()
# result = crawler.run(user_tags)
# print(result)
