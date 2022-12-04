import random
from asyncio import Semaphore
from unittest.mock import ANY, AsyncMock, MagicMock, call

import pytest

from files_downloader.downloader import Downloader
from files_downloader.exception import RetryableException
from files_downloader.schema import Failed, Success


@pytest.mark.asyncio
async def test_download_one_happy_path():
    # GIVEN
    display, reader, writer = AsyncMock(), AsyncMock(), AsyncMock()
    location = "/path"
    writer.save.return_value = location
    downloader = Downloader(display, reader, writer)

    client = MagicMock()
    client.get.return_value.__aenter__.return_value.status = 200
    client.get.return_value.__aenter__.return_value.read.return_value = b"data"

    semaphore, url = Semaphore(1), "https://text.com/"
    # WHEN
    result = await downloader.download_one(1, url, client, semaphore)
    # THEN
    assert result == Success(index=1, url=url, location=location)
    assert client.get.return_value.__aenter__.return_value.read.called
    assert writer.save.call_args == call(1, ANY, b"data")


@pytest.mark.parametrize(
    "retryable_status_codes",
    [[429], [408, 429, 500, 502, 503]],
)
@pytest.mark.asyncio
async def test_download_raise_retryable(retryable_status_codes):
    # GIVEN
    display, reader, writer = AsyncMock(), AsyncMock(), AsyncMock()
    downloader = Downloader(display, reader, writer)
    downloader.retryable_status_codes = retryable_status_codes

    client = MagicMock()
    client.get.return_value.__aenter__.return_value.status = random.choice(
        retryable_status_codes
    )

    semaphore, url = Semaphore(1), "https://text.com/"
    # WHEN & THEN
    with pytest.raises(RetryableException):
        await downloader.download_one(1, url, client, semaphore)


@pytest.mark.parametrize(
    "status_code",
    [400, 404],
)
@pytest.mark.asyncio
async def test_download_error_status_code(status_code):
    # GIVEN
    display, reader, writer = AsyncMock(), AsyncMock(), AsyncMock()
    location = "/path"
    writer.save.return_value = location
    downloader = Downloader(display, reader, writer)

    client = MagicMock()
    client.get.return_value.__aenter__.return_value.status = status_code
    client.get.return_value.__aenter__.return_value.read.return_value = b""

    semaphore, url = Semaphore(1), "https://text.com/"
    # WHEN
    result = await downloader.download_one(1, url, client, semaphore)
    # THEN
    assert result == Failed(
        index=1,
        url=url,
        message=f"Downloading file from {url} failed with status code {status_code}",
    )
    assert client.get.return_value.__aenter__.return_value.read.called


@pytest.mark.asyncio
async def test_download_empty_content():
    # GIVEN
    display, reader, writer = AsyncMock(), AsyncMock(), AsyncMock()
    location = "/path"
    writer.save.return_value = location
    downloader = Downloader(display, reader, writer)

    client = MagicMock()
    client.get.return_value.__aenter__.return_value.status = 200
    client.get.return_value.__aenter__.return_value.read.return_value = b""

    semaphore, url = Semaphore(1), "https://text.com/"
    # WHEN
    result = await downloader.download_one(1, url, client, semaphore)
    # THEN
    assert result == Failed(
        index=1, url=url, message=f"Downloading file from {url} failed. Empty Content"
    )
    assert client.get.return_value.__aenter__.return_value.read.called
