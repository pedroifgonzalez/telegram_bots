import os
import pathlib

import pytest
from utils import filter_travels, parse_refunds


def read_from_file(file_path: str):
    content: str = ""
    with open(file_path, "r") as file:
        content = file.read()
    return content


@pytest.fixture
def text_to_parse():
    parent = str(pathlib.Path(__file__).parent)
    path = os.path.sep.join([parent, "fixtures", "refunds.txt"])
    return read_from_file(path)


def test_parse_refunds(text_to_parse: str):
    travels = parse_refunds(text_to_parse)
    assert len(travels) == 2


def test_filter_travels(text_to_parse: str):
    travels = parse_refunds(text_to_parse)
    fltr_travels = filter_travels(travels, destination="Santa Clara", seat=10)
    assert len(fltr_travels) == 1
