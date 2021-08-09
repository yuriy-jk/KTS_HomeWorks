import asyncio
import time
from asyncio import Queue

import aiohttp
from bs4 import BeautifulSoup

from async_lastnpages_links_from_habr import LastNPages

domen = 'https://habr.com'

links = LastNPages.run(5)  # все статьи с последних n страниц
print('Количество статей для поиска тегов', len(links))

tags = ['microsoft', 'kts', 'python', 'data science', 'java', 'design']

finded_links = []


class FindLinks:
    @staticmethod
    async def download(link: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    soup = BeautifulSoup(text, 'lxml')
                    for tag in soup.find_all(attrs={'class': "tm-article-body__tags-item"}):
                        if tag.text.lower() in tags:
                            finded_links.append(link)
                else:
                    pass

            await session.close()


class WorkerPool:
    def __init__(self, queue: Queue):
        self._queue = queue

    async def run(self):
        while self._queue:
            obj = await self._queue.get()
            name = obj.__qualname__
            if name == 'FindLinks.download':  # здесь можно проверять тип таска и рейт лимит?
                await obj
                self._queue.task_done()


async def main():
    queue = asyncio.Queue()
    for link in links:
        await queue.put(FindLinks.download(domen + link))
    tasks = []
    for i in range(15):
        task = asyncio.create_task(WorkerPool(queue).run())
        tasks.append(task)
    await queue.join()
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)


started_at = time.monotonic()

asyncio.run(main())

print(f'finded links - {finded_links}')

print('total time', time.monotonic() - started_at)
