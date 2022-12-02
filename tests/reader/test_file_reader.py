from pathlib import Path

import pytest

from files_downloader.reader.file_reader import FileReader


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "file_path,expected_result",
    [
        (
            Path("resources/input/example.txt"),
            [
                (0, "https://cdn-icons-png.flaticon.com/1.png\n"),
                (1, "https://cdn-icons-png.flaticon.com/2.png\n"),
                (2, "https://cdn-icons-png.flaticon.com/3.png\n"),
                (3, "https://cdn-icons-png.flaticon.com/4.png\n"),
                (4, "https://cdn-icons-png.flaticon.com/5.png\n"),
            ],
        ),
        (Path("resources/input/empty.txt"), []),
    ],
)
async def test_file_reader(file_path: Path, expected_result: list[tuple[int, str]]):
    # GIVEN
    file_reader = FileReader()
    # WHEN
    urls = await file_reader.read(file_path)
    # THEN
    assert len(urls) == len(expected_result)
    assert urls == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "file_path,exception",
    [
        (Path("resources/input/not-existing.txt"), FileNotFoundError),
        (Path("resources/input"), IsADirectoryError),
    ],
)
async def test_file_reader_with_exception(file_path: Path, exception):
    # GIVEN
    file_reader = FileReader()
    # WHEN & THEN
    with pytest.raises(exception):
        await file_reader.read(file_path)
