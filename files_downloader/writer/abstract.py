from abc import ABC
from typing import Any


class Writer(ABC):  # pylint: disable=R0903
    def __init__(self, destination: Any):
        self.destination = destination

    async def save(self, index, response, data, *args, **kwargs) -> Any:
        pass
