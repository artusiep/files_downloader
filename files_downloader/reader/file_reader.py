from pathlib import Path

import asyncstdlib
from aiofile import AIOFile, LineReader

from files_downloader.reader.abstract import Reader


class FileReader(Reader):  # pylint: disable=R0903
    async def read(  # pylint: disable=W0221
        self, input_file_path: Path, *args, **kwargs
    ) -> list[tuple[int, str]]:
        async with AIOFile(input_file_path, "r") as file_handler:
            urls = [
                (i, url)
                async for i, url in asyncstdlib.enumerate(LineReader(file_handler))
            ]
        return urls
