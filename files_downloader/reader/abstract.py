from abc import ABC, abstractmethod
from typing import Any


class Reader(ABC):  # pylint: disable=R0903
    @abstractmethod
    async def read(self, *args, **kwargs) -> Any:
        pass
