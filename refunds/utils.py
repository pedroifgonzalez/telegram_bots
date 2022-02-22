import re
from datetime import datetime
from typing import Iterable, List

from model import Travel

SEP = "(-){41}\n"
HEADER = re.compile(f"Reintegros\n{SEP}")
COMMENT = re.compile(f"{SEP}Venta por el apk y agencia\n")
ORIGIN_DESTINATION = "(🌐)((.+) - (.+))\n"
TRANSPORT = "(🚌|🚂)(.*)\n"
SECTION = "Tramo: ((.+) - (.+))\n"
DETAILS = "(.{3}). ([0-9]{2}-[0-9]{2}-[0-9]{4}) ([0-9]{2}:[0-9]{2}) (.*)\n?"
BLOCK = re.compile(f"{SEP}{ORIGIN_DESTINATION}{TRANSPORT}{SECTION}{DETAILS}")


def parse_refunds(text: str) -> List[Travel]:
    """
    Parse the raw text from channel's messages

    :param text: Raw text to parse
    :type text: str
    :return: A list of Travel objects
    :rtype: List[Travel]
    """
    travels: List[Travel] = []
    if HEADER.findall(text) and COMMENT.findall(text) and BLOCK.findall(text):
        for travel in BLOCK.finditer(text):
            origin = travel.group(4)
            destination = travel.group(5)
            transport = travel.group(6)
            section = travel.group(8)
            day_of_week = travel.group(11)
            date_parts = travel.group(12).split("-")
            date_parts[0], date_parts[-1] = date_parts[-1], date_parts[0]
            date_time = "-".join(date_parts) + " " + travel.group(13)
            date_time = datetime.fromisoformat(date_time)
            seat = re.findall("[0-9]+", travel.group(14))[0]
            travels.append(
                Travel(
                    origin=origin,
                    destination=destination,
                    transport=transport,
                    section=section,
                    date_time=date_time,
                    day_of_week=day_of_week,
                    seat=seat,
                )
            )
    return travels


def filter_travels(travels: Iterable[Travel], **travel_attrs) -> List[Travel]:
    """
    Filter travel objects

    :param travels: Travel objects to apply filters
    :type travels: List[Travel]
    :return: Travel objects according to filters
    :rtype: List[Travel]
    """
    filtered_travels: List[Travel] = []
    for travel in travels:
        valid = True
        for travel_attr, travel_attr_value in travel_attrs.items():
            if getattr(travel, travel_attr) != travel_attr_value:
                valid = False
        if valid:
            filtered_travels.append(travel)
    return filtered_travels


def filter_travels_by_day_and_month(
        travels: List[Travel],
        day: int,
        month: int
        ) -> List[Travel]:
    filtered_travels = [
        travel
        for travel in travels
        if travel.day == day and travel.month == month
    ]
    return filtered_travels
