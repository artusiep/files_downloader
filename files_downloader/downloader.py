import asyncio
import functools
from asyncio import Semaphore, Task
from typing import Awaitable, Callable, Iterable, Type

import aiohttp
from aiohttp import ClientSession

from files_downloader.display import Display
from files_downloader.exception import RetryableException
from files_downloader.reader.abstract import Reader
from files_downloader.schema import Failed, Success
from files_downloader.writer.abstract import Writer


class Downloader:
    retryable_status_codes = [408, 429, 500, 502, 503, 503]

    def __init__(self, display: Display, reader: Reader, writer: Writer):
        self.display = display
        self.reader = reader
        self.writer = writer

    async def retry(
        self,
        coro: Callable[[], Awaitable],
        max_retries: int,
        timeout: float,
        retry_interval: float,
        custom_exc: Iterable[Type[BaseException]] = (Exception,),
    ):  # pylint: disable=R0913
        """
        Implementation of exponential backoff would behave better in case receiving 429
        """
        index = coro.keywords["index"]  # type: ignore
        url = coro.keywords["url"]  # type: ignore
        for retry_num in range(0, max_retries):
            try:
                return await asyncio.wait_for(coro(), timeout=timeout)
            except (*custom_exc, RetryableException) as exception:  # type: ignore
                self.display.retry_info(retry_num, index, url, exception)
                await asyncio.sleep(retry_interval)
        return Failed(
            index=index,
            url=url,
            message=f"Exceed max retry num: {max_retries} times failed",
        )

    def get_tasks(self, client: ClientSession, sem: Semaphore, urls) -> list[Task]:
        return [
            asyncio.create_task(
                self.retry(
                    functools.partial(
                        self.download_one, index=i, url=url, client=client, sem=sem
                    ),
                    max_retries=5,
                    timeout=1,
                    retry_interval=5,
                    custom_exc=(
                        aiohttp.ClientConnectionError,
                        asyncio.exceptions.TimeoutError,
                    ),
                )
            )
            for i, url in urls
        ]

    async def download(self, source, limit):
        results = []
        successes = 0
        fails = 0
        sem = Semaphore(limit)
        urls = await self.reader.read(source)
        async with ClientSession() as client:
            pending = self.get_tasks(client, sem, urls)
            self.display.start(len(pending))
            while pending:
                self.display.progress(len(pending), successes, fails)

                done, pending = await asyncio.wait(
                    pending, return_when=asyncio.FIRST_COMPLETED
                )
                for done_task in done:

                    result = await done_task
                    results.append(result)
                    if isinstance(result, Success):
                        successes += 1
                    else:
                        fails += 1

        self.display.progress(len(pending), successes, fails)
        return results

    async def download_one(self, index, url, client: ClientSession, sem: Semaphore):
        async with sem, client.get(url) as response:
            data = await response.read()
        if response.status in self.retryable_status_codes:
            raise RetryableException()

        if response.status != 200:
            message = (
                f"Downloading file from {url} failed with "
                f"status code {response.status}"
            )
            self.display.error(message)
            return Failed(index=index, url=url, message=message)

        if index == 5:
            return Failed(index=index, url=url, message="BLAH")

        if data == b"":
            message = f"Downloading file from {url} failed. Empty Content"
            self.display.error(message)
            return Failed(index=index, url=url, message=message)

        location = await self.writer.save(index, response, data)
        return Success(index=index, url=url, location=location)
