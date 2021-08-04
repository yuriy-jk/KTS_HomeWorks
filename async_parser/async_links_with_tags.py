import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup

from async_lastNpages_links_from_Habr import Last_n_pages

domen = 'https://habr.com'

links = Last_n_pages.run(4)  # все статьи с последних n страниц
# print('Количество статей для поиска тегов', len(links))

tags = ['microsoft', 'kts', 'python', 'data science', 'java', 'design']

finded_links = []


async def download(link: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            # print(f'session get {link}')
            if resp.status == 200:
                # print(f'{resp.status} - {link}')
                # print('status ok')
                text = await resp.text()
                # print('await resp')
                soup = BeautifulSoup(text, 'lxml')

                for tag in soup.find_all(attrs={'class': "tm-article-body__tags-item"}):
                    if tag.text.lower() in tags:
                        # print(tag.text.lower())
                        finded_links.append(link)
                        # print('link append')
            else:
                pass
                # print('link error')

        await session.close()
        # print('session closed')


async def worker(n, queue):
    while queue:
        obj = await queue.get()
        # print(f'worker{n}, received, {obj}')
        await download(obj)
        # print(f'worker{n}, processed, {obj}')
        queue.task_done()


async def main():
    queue = asyncio.Queue()

    for link in links:
        await queue.put(domen + link)

    tasks = []
    for i in range(8):
        task = asyncio.create_task(worker(i + 1, queue))
        tasks.append(task)

    await queue.join()

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)


started_at = time.monotonic()

asyncio.run(main())

print(f'finded links - {finded_links}')

print('total time', time.monotonic() - started_at)
