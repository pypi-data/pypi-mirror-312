from conductor_api.utils import week_number, conductor_date_format


def test_week_number():
    number = week_number("2018-04-12")
    assert number == 455


def test_conductor_date_format():
    number = conductor_date_format("2018-04-12")
    assert number == "20180412"
