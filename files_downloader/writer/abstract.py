from abc import ABC, abstractmethod
from typing import Any


class Writer(ABC):  # pylint: disable=R0903
    def __init__(self, destination: Any):
        self.destination = destination

    @abstractmethod
    async def save(self, index, response, data, *args, **kwargs) -> Any:
        pass
