from pathlib import Path

import pytest
from aiofile import async_open
from aiohttp.web_response import Response

from files_downloader.writer.file_writer import FileWriter


@pytest.mark.parametrize(
    "output_dir,index,response,expected_result",
    [
        (Path("temp"), 0, Response(), Path("temp/0")),
        (Path("temp"), 1, Response(content_type="text/css"), Path("temp/1.css")),
        (
            Path("temp"),
            9,
            Response(content_type="application/json"),
            Path("temp/9.json"),
        ),
        (Path("temp"), 0, Response(content_type="image/png"), Path("temp/0.png")),
        (Path("temp"), 0, Response(content_type="image/webp"), Path("temp/0.webp")),
        (Path("temp"), 0, Response(content_type="text/plain"), Path("temp/0.txt")),
        (Path("temp"), 0, Response(content_type="text/xml"), Path("temp/0.xml")),
        (Path("temp"), 0, Response(content_type="image/jpeg"), Path("temp/0.jpg")),
    ],
)
def test_get_file_path_with_extension(
    output_dir: Path, index: int, response: Response, expected_result: Path
):
    # WHEN
    path = FileWriter.get_filepath_with_extension(output_dir, index, response)
    # THEN
    assert path == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    # Data is a code to be evaluated in test itself as parametrize outputs to stdout
    # value of the parameters which makes test significantly longer
    "index,mime,extension,data",
    [
        (1, "image/png", ".png", 'b""'),
        (1, "image/webp", ".webp", 'b"This not have to be valid content"'),
        (1, "image/jpeg", ".jpg", 'b"0" * 2 ** 30'),  # Around 1024 MB of data
    ],
)
async def test_save(tmpdir, index: int, mime: str, extension: str, data: str):
    # GIVEN
    evaluated_data = eval(data)
    # WHEN
    file_writer = FileWriter(tmpdir)
    result_path = await file_writer.save(
        index, Response(content_type=mime), evaluated_data
    )
    # THEN
    async with async_open(result_path, "rb") as tmp_file:
        result_data = await tmp_file.read()
    assert result_path == Path(tmpdir, str(index) + extension)
    assert result_data == evaluated_data
