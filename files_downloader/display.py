import logging
from logging import Logger

from files_downloader.schema import Result


class Display:
    def __init__(
        self, logger, should_display_status, should_display_summary, verbose=False
    ):
        self.__should_display_progress = should_display_status
        self.__should_display_summary = should_display_summary
        self.__verbose = verbose
        self.__logger: Logger = logger
        self.__logger.setLevel(logging.INFO)

    def start(self, pending: int):
        self.__logger.info("Starting downloading of %s files", pending)

    def progress(self, pending: int, done: int, failed: int) -> None:
        if self.__should_display_progress:
            self.__logger.info(
                "Pending: %s, Done: %s, Failed: %s", pending, done, failed
            )

    def summary(self, results: list[Result]):
        if self.__should_display_summary:
            self.__logger.info("\n\n--------Summary--------\n")
            for result in results:
                self.__logger.info(result.to_string())

    def retry_info(self, retry_num, index, url, exception):
        self.__logger.exception(
            "Exception while waiting (tried %s times), (index=%s, url=%s) retrying.",
            retry_num,
            index,
            url,
            exc_info=exception if self.__verbose else False,
        )

    def error(self, *args, **kwargs):
        self.__logger.error(*args, **kwargs)
