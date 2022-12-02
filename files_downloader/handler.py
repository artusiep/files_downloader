import asyncio
import logging
import os

import click

from files_downloader.display import Display
from files_downloader.downloader import Downloader
from files_downloader.reader.file_reader import FileReader
from files_downloader.writer.file_writer import FileWriter

logger = logging.getLogger("files_downloader")
logging.basicConfig(level=logging.INFO, format="%(message)s")


@click.command()
@click.argument(
    "file", type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True)
)
@click.argument(
    "output-dir", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option("-c", "--concurrent-files", "limit", default=50)
@click.option("-p", "--display-progress", is_flag=True, default=False)
@click.option("-s", "--display-summary", is_flag=True, default=False)
@click.option("-v", "--verbose", is_flag=True, default=False)
def handler(
    file, output_dir, limit, display_progress, display_summary, verbose
):  # pylint: disable=R0913
    os.makedirs(output_dir, exist_ok=True)
    display = Display(logger, display_progress, display_summary, verbose)
    reader = FileReader()
    writer = FileWriter(output_dir)
    downloader = Downloader(display, reader, writer)
    results = asyncio.run(downloader.download(file, limit))
    display.summary(results)
