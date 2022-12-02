import mimetypes
from pathlib import Path
from typing import Any

from aiofile import async_open
from aiohttp.web_response import Response

from files_downloader.writer.abstract import Writer


class FileWriter(Writer):
    @staticmethod
    def get_filepath_with_extension(
        output_dir: Path, index: int, response: Response
    ) -> Path:
        if (content_type := response.headers.get("Content-Type")) and (
            extension := mimetypes.guess_extension(str(content_type))
        ):
            return Path(output_dir, str(index) + extension)
        return Path(output_dir, str(index))

    async def save(
        self, index: int, response: Response, data: bytes | bytearray, *args, **kwargs
    ) -> Any:
        filepath_with_extension = self.get_filepath_with_extension(
            self.destination, index, response
        )
        async with async_open(filepath_with_extension, "wb") as out_file:
            await out_file.write(data)
        return filepath_with_extension
