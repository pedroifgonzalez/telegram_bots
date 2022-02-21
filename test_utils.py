from utils import parse_refunds, filter_travels


def read_from_file(file_path: str):
    content: str = ""
    with open(file_path, "r") as file:
        content = file.read()
    return content


def test_parse_refunds():
    text_to_parse = read_from_file("refunds.txt")
    travels = parse_refunds(text_to_parse)
    assert len(travels) == 2


def test_filter_travels():
    text_to_parse = read_from_file("refunds.txt")
    travels = parse_refunds(text_to_parse)
    filtered_travels = filter_travels(travels,
        destination="Santa Clara",
        seat=10
    )
    assert len(filtered_travels) == 1
