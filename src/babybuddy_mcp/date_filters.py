"""Expand bare YYYY-MM-DD filters for Baby Buddy IsoDateTimeFilter params.

Baby Buddy's TimeFieldFilter (api/filters.py) defines:

    date = IsoDateTimeFilter(field_name="time")          # exact DateTime match
    date_min = IsoDateTimeFilter(..., lookup_expr="gte")
    date_max = IsoDateTimeFilter(..., lookup_expr="lte")

A bare calendar day such as ``?date=2026-09-05`` therefore matches only midnight,
not every record on that day. Assistants commonly pass YYYY-MM-DD and get empty
lists. This module expands those values to a full local-day datetime range.
"""

from __future__ import annotations

import re

from .client import QueryParams

_BARE_DAY = re.compile(r"\A\d{4}-\d{2}-\d{2}\Z")

DAY_START = "T00:00:00"
DAY_END = "T23:59:59.999999"

DATE_ARG = (
    "Calendar day YYYY-MM-DD is expanded to a full local day range "
    "(date_min={day}T00:00:00, date_max={day}T23:59:59.999999). "
    "ISO datetimes (containing T) pass through as an exact date= match."
)
DATE_MIN_ARG = (
    "Start of range. Bare YYYY-MM-DD expands to {day}T00:00:00. "
    "ISO datetimes pass through unchanged."
)
DATE_MAX_ARG = (
    "End of range. Bare YYYY-MM-DD expands to {day}T23:59:59.999999. "
    "ISO datetimes pass through unchanged."
)


def is_bare_calendar_day(value: str) -> bool:
    """Return True when value is exactly YYYY-MM-DD with no time component."""
    return bool(_BARE_DAY.fullmatch(value.strip()))


def expand_date_filters(
    date: str | None = None,
    date_min: str | None = None,
    date_max: str | None = None,
) -> dict[str, str]:
    """Map tool date args to Baby Buddy query params.

    Bare ``date`` becomes ``date_min``/``date_max`` covering that local day.
    Bare ``date_min``/``date_max`` get start-of-day / end-of-day times.
    Values that already include a time (or are otherwise not YYYY-MM-DD) pass
    through unchanged. Explicit ``date_min``/``date_max`` override the bounds
    produced by a bare ``date``.
    """
    params: dict[str, str] = {}

    if date is not None:
        day = date.strip()
        if is_bare_calendar_day(day):
            params["date_min"] = f"{day}{DAY_START}"
            params["date_max"] = f"{day}{DAY_END}"
        else:
            params["date"] = date

    if date_min is not None:
        day = date_min.strip()
        if is_bare_calendar_day(day):
            params["date_min"] = f"{day}{DAY_START}"
        else:
            params["date_min"] = date_min

    if date_max is not None:
        day = date_max.strip()
        if is_bare_calendar_day(day):
            params["date_max"] = f"{day}{DAY_END}"
        else:
            params["date_max"] = date_max

    return params


def apply_date_filters(
    params: QueryParams,
    date: str | None = None,
    date_min: str | None = None,
    date_max: str | None = None,
) -> None:
    """Write expanded date filters onto an existing query-param dict."""
    params.update(expand_date_filters(date=date, date_min=date_min, date_max=date_max))
