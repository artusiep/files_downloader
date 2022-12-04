import os
from pathlib import Path

import pytest


@pytest.fixture()
def test_directory():
    working_directory = Path(os.getcwd(), "tests")
    return working_directory
