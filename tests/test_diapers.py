import httpx
import pytest
import respx

from babybuddy_mcp.tools.diapers import (
    create_diaper_change,
    delete_diaper_change,
    list_diaper_changes,
    update_diaper_change,
)

BASE = "http://test-babybuddy"

CHANGE = {"id": 1, "child": 1, "time": "2024-01-15T10:00:00Z", "wet": True, "solid": False}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_diaper_changes(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/changes/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [CHANGE]}
        )
    )
    result = await list_diaper_changes()
    assert result[0]["wet"] is True


async def test_list_diaper_changes_calendar_day_expands_to_range(
    mock_api: respx.MockRouter,
) -> None:
    route = mock_api.get("/api/changes/").mock(
        return_value=httpx.Response(
            200, json={"count": 0, "next": None, "previous": None, "results": []}
        )
    )
    await list_diaper_changes(date="2024-01-15")
    params = dict(route.calls[0].request.url.params)
    assert "date" not in params
    assert params["date_min"] == "2024-01-15T00:00:00"
    assert params["date_max"] == "2024-01-15T23:59:59.999999"


async def test_list_diaper_changes_iso_datetime_keeps_exact_date(
    mock_api: respx.MockRouter,
) -> None:
    route = mock_api.get("/api/changes/").mock(
        return_value=httpx.Response(
            200, json={"count": 0, "next": None, "previous": None, "results": []}
        )
    )
    await list_diaper_changes(date="2024-01-15T10:00:00")
    params = dict(route.calls[0].request.url.params)
    assert params["date"] == "2024-01-15T10:00:00"
    assert "date_min" not in params
    assert "date_max" not in params


async def test_list_with_filters(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/api/changes/").mock(
        return_value=httpx.Response(
            200, json={"count": 0, "next": None, "previous": None, "results": []}
        )
    )
    await list_diaper_changes(child_id=1, wet=True, color="yellow")
    params = dict(route.calls[0].request.url.params)
    assert params["child"] == "1"
    assert params["wet"].lower() == "true"
    assert params["color"] == "yellow"


async def test_create_diaper_change(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/changes/").mock(return_value=httpx.Response(201, json=CHANGE))
    result = await create_diaper_change(
        child_id=1, time="2024-01-15T10:00:00", wet=True, solid=False
    )
    assert result["id"] == 1


async def test_update_diaper_change(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/changes/1/").mock(
        return_value=httpx.Response(200, json={**CHANGE, "solid": True})
    )
    result = await update_diaper_change(1, solid=True)
    assert result["solid"] is True


async def test_delete_diaper_change(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/changes/1/").mock(return_value=httpx.Response(204))
    result = await delete_diaper_change(1)
    assert "1" in result
