from babybuddy_mcp.date_filters import (
    DAY_END,
    DAY_START,
    expand_date_filters,
    is_bare_calendar_day,
)


def test_is_bare_calendar_day() -> None:
    assert is_bare_calendar_day("2024-01-15") is True
    assert is_bare_calendar_day(" 2024-01-15 ") is True
    assert is_bare_calendar_day("2024-01-15T10:00:00") is False
    assert is_bare_calendar_day("2024-01-15T00:00:00Z") is False
    assert is_bare_calendar_day("2024-01-15 10:00:00") is False
    assert is_bare_calendar_day("") is False


def test_expand_bare_date_to_local_day_range() -> None:
    params = expand_date_filters(date="2024-01-15")
    assert params == {
        "date_min": f"2024-01-15{DAY_START}",
        "date_max": f"2024-01-15{DAY_END}",
    }
    assert "date" not in params


def test_expand_iso_datetime_keeps_exact_date() -> None:
    params = expand_date_filters(date="2024-01-15T10:00:00")
    assert params == {"date": "2024-01-15T10:00:00"}


def test_expand_bare_date_min_and_date_max() -> None:
    params = expand_date_filters(date_min="2024-01-01", date_max="2024-02-01")
    assert params == {
        "date_min": f"2024-01-01{DAY_START}",
        "date_max": f"2024-02-01{DAY_END}",
    }


def test_expand_iso_range_bounds_pass_through() -> None:
    params = expand_date_filters(
        date_min="2024-01-01T08:00:00",
        date_max="2024-01-02T12:00:00Z",
    )
    assert params == {
        "date_min": "2024-01-01T08:00:00",
        "date_max": "2024-01-02T12:00:00Z",
    }


def test_explicit_range_overrides_bare_date_bounds() -> None:
    params = expand_date_filters(
        date="2024-01-15",
        date_min="2024-01-10",
        date_max="2024-01-20T12:00:00",
    )
    assert params == {
        "date_min": f"2024-01-10{DAY_START}",
        "date_max": "2024-01-20T12:00:00",
    }


def test_none_args_produce_empty_params() -> None:
    assert expand_date_filters() == {}
