from dataclasses import dataclass
from typing import Any


@dataclass
class Result:
    index: int
    url: str

    def to_string(self):
        pass


@dataclass
class Success(Result):
    location: Any

    def to_string(self):
        return f"Download of {self.index} from {self.url} " f"saved in {self.location}"


@dataclass
class Failed(Result):
    message: str

    def to_string(self):
        return (
            f"!!ERROR!! Download of {self.index} from {self.url} "
            f"failed with {self.message}"
        )
