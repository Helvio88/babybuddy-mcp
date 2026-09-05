import httpx
import pytest
import respx

from babybuddy_mcp.tools.medications import (
    create_medication,
    delete_medication,
    list_medications,
    update_medication,
)

BASE = "http://test-babybuddy"

MED = {
    "id": 1,
    "child": 1,
    "name": "Tylenol",
    "dosage": 5.0,
    "dosage_unit": "ml",
    "time": "2024-01-15T10:00:00Z",
}


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_medications(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/medication/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [MED]}
        )
    )
    result = await list_medications()
    assert result[0]["name"] == "Tylenol"


async def test_list_medications_calendar_day_expands_to_range(
    mock_api: respx.MockRouter,
) -> None:
    route = mock_api.get("/api/medication/").mock(
        return_value=httpx.Response(
            200, json={"count": 0, "next": None, "previous": None, "results": []}
        )
    )
    await list_medications(date="2024-01-15")
    params = route.calls[0].request.url.params
    assert "date" not in params
    assert params["date_min"] == "2024-01-15T00:00:00"
    assert params["date_max"] == "2024-01-15T23:59:59.999999"


async def test_list_medications_with_filters(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/api/medication/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "previous": None, "results": [MED]}
        )
    )
    await list_medications(name="Tylenol", dosage_unit="ml", tags=["fever"])
    params = route.calls[0].request.url.params
    assert params["name"] == "Tylenol"
    assert params["dosage_unit"] == "ml"
    assert params["tags"] == "fever"


async def test_create_medication(mock_api: respx.MockRouter) -> None:
    route = mock_api.post("/api/medication/").mock(
        return_value=httpx.Response(201, json=MED)
    )
    result = await create_medication(
        child_id=1,
        name="Tylenol",
        dosage=5.0,
        dosage_unit="ml",
        next_dose_interval="04:00:00",
    )
    assert result["id"] == 1
    body = route.calls[0].request.content
    assert b"next_dose_interval" in body


async def test_update_medication(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/medication/1/").mock(
        return_value=httpx.Response(200, json={**MED, "dosage": 10.0})
    )
    result = await update_medication(1, dosage=10.0)
    assert result["dosage"] == 10.0


async def test_delete_medication(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/medication/1/").mock(return_value=httpx.Response(204))
    result = await delete_medication(1)
    assert "1" in result
