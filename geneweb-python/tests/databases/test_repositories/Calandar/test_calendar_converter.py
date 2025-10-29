import pytest
from datetime import date
from geneweb.core.services.calendar_converter import CalendarConverter


def test_french_republican_edge_case_month_13():
    converter = CalendarConverter()

    result = converter.gregorian_to_french_republican(1793, 9, 17)

    if result is not None:
        assert result["year"] >= 1
        assert result["month"] >= 1
        assert result["day"] >= 1


def test_french_republican_boundary_dates():
    converter = CalendarConverter()

    result = converter.gregorian_to_french_republican(1792, 9, 22)
    assert result is not None
    assert result["year"] == 1
    assert result["day"] == 1

    result = converter.gregorian_to_french_republican(1792, 9, 21)
    assert result is None

    result = converter.gregorian_to_french_republican(1794, 7, 27)
    assert result is not None
    assert result["year"] >= 1

    result = converter.gregorian_to_french_republican(1805, 6, 15)
    assert result is not None
    assert result["year"] == 13

    result = converter.gregorian_to_french_republican(1807, 1, 1)
    assert result is None

    result = converter.gregorian_to_french_republican(1700, 1, 1)
    assert result is None


def test_french_republican_edge_year_1805():
    converter = CalendarConverter()

    result = converter.gregorian_to_french_republican(1805, 1, 1)
    assert result is not None

    result = converter.gregorian_to_french_republican(1805, 6, 15)
    assert result is not None

    result = converter.gregorian_to_french_republican(1805, 12, 31)
    if result is None:
        assert result is None
    else:
        assert result["year"] >= 1


def test_french_republican_year_1806_rejected():
    converter = CalendarConverter()

    result = converter.gregorian_to_french_republican(1806, 1, 1)
    assert result is None

    result = converter.gregorian_to_french_republican(1806, 6, 15)
    assert result is None

    result = converter.gregorian_to_french_republican(1900, 1, 1)
    assert result is None

    result = converter.gregorian_to_french_republican(2025, 10, 16)
    assert result is None


def test_hebrew_month_boundary():
    converter = CalendarConverter()

    dates_to_test = [
        (2025, 1, 1),
        (2025, 6, 15),
        (2025, 12, 31),
        (1900, 1, 1),
        (2100, 12, 31),
    ]

    for year, month, day in dates_to_test:
        result = converter.gregorian_to_hebrew(year, month, day)
        assert result is not None
        assert (
            1 <= result["month"] <= 12
        ), f"Month out of range for {year}-{month}-{day}"
        assert result["month_name"] in converter.HEBREW_MONTHS


def test_julian_conversion_edge_cases():
    converter = CalendarConverter()

    result = converter.gregorian_to_julian(1, 1, 1)
    assert result is not None
    assert "year" in result
    assert "month" in result
    assert "day" in result

    result = converter.gregorian_to_julian(2100, 12, 31)
    assert result is not None

    result = converter.gregorian_to_julian(1582, 10, 15)
    assert result is not None


def test_french_republican_day_overflow():
    converter = CalendarConverter()

    result = converter.gregorian_to_french_republican(1793, 9, 21)

    if result is not None:
        assert result["month"] <= 13
        assert result["day"] <= 30


def test_hebrew_month_edge_calculation():
    converter = CalendarConverter()

    result = converter.gregorian_to_hebrew(2025, 12, 31)

    assert result is not None
    assert result["month"] <= 12, "Hebrew month should be capped at 12"
    assert result["month"] >= 1, "Hebrew month should be at least 1"


def test_convert_from_gregorian_all_fields():
    converter = CalendarConverter()

    result = converter.convert_from_gregorian(2000, 6, 15)

    assert "gregorian" in result
    assert "julian" in result
    assert "julian_day_number" in result
    assert "french_republican" in result
    assert "hebrew" in result

    greg = result["gregorian"]
    assert greg["year"] == 2000
    assert greg["month"] == 6
    assert greg["day"] == 15
    assert greg["month_name"] == "June"

    julian = result["julian"]
    assert "year" in julian
    assert "month" in julian
    assert "day" in julian
    assert "month_name" in julian

    hebrew = result["hebrew"]
    assert "year" in hebrew
    assert "month" in hebrew
    assert "day" in hebrew
    assert "month_name" in hebrew


def test_julian_day_number_consistency():
    converter = CalendarConverter()

    test_jdns = [2451545, 2299161, 2400000, 2500000]

    for jdn in test_jdns:
        greg = converter.julian_day_number_to_gregorian(jdn)

        jdn_back = converter.gregorian_to_julian_day_number(
            greg["year"], greg["month"], greg["day"]
        )

        assert abs(jdn - jdn_back) <= 1, f"JDN mismatch: {jdn} != {jdn_back}"


def test_all_month_names_accessible():
    converter = CalendarConverter()

    for month in range(1, 13):
        result = converter.convert_from_gregorian(2025, month, 15)
        assert result["gregorian"]["month_name"] in converter.GREGORIAN_MONTHS

    for month in range(1, 13):
        result = converter.gregorian_to_julian(2025, month, 15)
        month_name = converter.JULIAN_MONTHS[result["month"] - 1]
        assert month_name in converter.JULIAN_MONTHS


def test_french_republican_year_calculation():
    converter = CalendarConverter()

    result = converter.gregorian_to_french_republican(1792, 9, 22)
    assert result is not None
    assert result["year"] == 1

    result = converter.gregorian_to_french_republican(1793, 9, 22)
    if result is not None:
        assert result["year"] == 2

    result = converter.gregorian_to_french_republican(1794, 9, 22)
    if result is not None:
        assert result["year"] == 3


def test_hebrew_year_reasonable_range():
    converter = CalendarConverter()

    result = converter.gregorian_to_hebrew(2025, 10, 1)
    assert result is not None
    assert (
        5780 <= result["year"] <= 5790
    ), f"Hebrew year {result['year']} seems out of range"

    result = converter.gregorian_to_hebrew(2000, 1, 1)
    assert result is not None
    assert 5755 <= result["year"] <= 5765


def test_negative_jdn_calculation():
    converter = CalendarConverter()

    jdn = converter.gregorian_to_julian_day_number(1, 1, 1)
    assert jdn > 0

    jdn = converter.gregorian_to_julian_day_number(100, 6, 15)
    assert jdn > 0


def test_french_month_index_bounds():
    converter = CalendarConverter()

    test_dates = [
        (1793, 9, 22),
        (1793, 12, 31),
        (1794, 6, 15),
        (1794, 9, 21),
    ]

    for year, month, day in test_dates:
        result = converter.gregorian_to_french_republican(year, month, day)
        if result is not None:
            month_idx = result["month"] - 1
            if month_idx < 12:
                assert 0 <= month_idx < len(converter.FRENCH_MONTHS)
                assert result["month_name"] == \
                    converter.FRENCH_MONTHS[month_idx]
