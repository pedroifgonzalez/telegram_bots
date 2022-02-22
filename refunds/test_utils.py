import os
import pathlib
from datetime import datetime
from typing import Any, Dict, List
from unittest.mock import MagicMock

import pytest
from utils import (filter_travels, filter_travels_by_day_and_month,
                   parse_refunds)


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


Travel = MagicMock
empty_dict: Dict[str, Any] = dict()


@pytest.mark.parametrize(
    "travels, filters, expected_count",
    [
        (
            [Travel(origin="La Habana"), Travel(origin="Matanzas")],
            dict(origin="La Habana"),
            1,
        ),
        (
            [
                Travel(destination="La Habana", seat=11),
                Travel(destination="Matanzas", seat=11),
            ],
            dict(seat=11),
            2,
        ),
        (
            [
                Travel(destination="La Habana", seat=11),
                Travel(destination="Matanzas", seat=11),
            ],
            empty_dict,
            2,
        ),
    ],
)
def test_filter_travels(
        travels: List[Travel],
        filters: Any,
        expected_count: int
        ):
    assert len(filter_travels(travels, **filters)) == expected_count


@pytest.mark.parametrize(
    "travels, day, month, expected_count",
    [(
        [
            Travel(
                destination="La Habana",
                day=datetime.now().day,
                month=datetime.now().month)
        ],
        datetime.now().day,
        datetime.now().month,
        1
    ),
     (
        [
            Travel(
                destination="La Habana",
                day=29,
                month=1)
        ],
        14,
        10,
        0
    )]
)
def test_filter_travels_by_day_and_month(
        travels: List[Travel],
        day: int,
        month: int,
        expected_count: int
        ):
    travels_count = len(filter_travels_by_day_and_month(travels, day, month))
    assert travels_count == expected_count
