import asyncio
from asyncio import Queue

import aiohttp
from bs4 import BeautifulSoup
import requests
import pprint
import time

"""берем список ссылок на последние статьи"""

main_link = 'https://habr.com/ru/all/page'
links = []


class Last_n_pages:

    @staticmethod
    async def get_links(link: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    #
                    soup = BeautifulSoup(text, 'lxml')
                    for link in soup.find_all(attrs={'class': 'tm-article-snippet__title-link'}):
                        links.append(link.get('href'))
                else:
                    pass

    @staticmethod
    async def worker(n: int, queue: Queue):
        while queue:
            obj = await queue.get()
            # print(f'worker{n}, received, {obj}')
            await Last_n_pages.get_links(obj)
            # print(f'worker{n}, processed, {obj}')
            queue.task_done()

    @staticmethod
    async def main(number: int):
        queue = asyncio.Queue()

        pages = [main_link + str(i) for i in range(1, number)]

        for page in pages:
            await queue.put(page)

        tasks = []

        for i in range(4):
            task = asyncio.create_task(Last_n_pages.worker(i + 1, queue))
            tasks.append(task)

        await queue.join()

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

    @staticmethod
    def run(n: int):
        asyncio.run(Last_n_pages.main(n))
        return links


