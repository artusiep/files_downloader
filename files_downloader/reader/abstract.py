from abc import ABC
from typing import Any


class Reader(ABC):  # pylint: disable=R0903
    def __init__(self, source: Any):
        self.source = source

    async def read(self, *args, **kwargs) -> Any:
        pass
