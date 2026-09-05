import httpx
import pytest
import respx

from babybuddy_mcp.tools.measurements import (
    create_bmi,
    create_head_circumference,
    create_height,
    create_temperature,
    create_weight,
    delete_bmi,
    list_bmi,
    list_head_circumference,
    list_height,
    list_temperature,
    list_weight,
    update_weight,
)

BASE = "http://test-babybuddy"


@pytest.fixture
def mock_api() -> respx.MockRouter:
    with respx.mock(base_url=BASE, assert_all_called=False) as router:
        yield router


async def test_list_bmi(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/bmi/").mock(
        return_value=httpx.Response(
            200,
            json={"count": 1, "next": None, "previous": None, "results": [{"id": 1, "bmi": 15.2}]},
        )
    )
    result = await list_bmi()
    assert result[0]["bmi"] == 15.2


async def test_list_bmi_exact_date_and_ordering(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/api/bmi/").mock(
        return_value=httpx.Response(
            200, json={"count": 0, "next": None, "previous": None, "results": []}
        )
    )
    await list_bmi(date="2024-01-01", ordering="-date")
    params = route.calls[0].request.url.params
    assert params["date"] == "2024-01-01"
    assert params["ordering"] == "-date"
    assert "date_min" not in params


async def test_list_temperature_range_and_tags(mock_api: respx.MockRouter) -> None:
    route = mock_api.get("/api/temperature/").mock(
        return_value=httpx.Response(
            200, json={"count": 0, "next": None, "previous": None, "results": []}
        )
    )
    await list_temperature(date_min="2024-01-01", date_max="2024-02-01", tags=["fever"])
    params = route.calls[0].request.url.params
    assert params["date_min"] == "2024-01-01T00:00:00"
    assert params["date_max"] == "2024-02-01T23:59:59.999999"
    assert params["tags"] == "fever"


async def test_create_bmi(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/bmi/").mock(
        return_value=httpx.Response(201, json={"id": 1, "child": 1, "date": "2024-01-01", "bmi": 15.2})
    )
    result = await create_bmi(child_id=1, date="2024-01-01", bmi=15.2)
    assert result["bmi"] == 15.2


async def test_delete_bmi(mock_api: respx.MockRouter) -> None:
    mock_api.delete("/api/bmi/1/").mock(return_value=httpx.Response(204))
    result = await delete_bmi(1)
    assert "1" in result


async def test_list_height(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/height/").mock(
        return_value=httpx.Response(
            200,
            json={"count": 1, "next": None, "previous": None, "results": [{"id": 1, "height": 55.0}]},
        )
    )
    result = await list_height()
    assert result[0]["height"] == 55.0


async def test_create_height(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/height/").mock(
        return_value=httpx.Response(201, json={"id": 1, "child": 1, "date": "2024-01-01", "height": 55.0})
    )
    result = await create_height(child_id=1, date="2024-01-01", height=55.0)
    assert result["height"] == 55.0


async def test_list_weight(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/weight/").mock(
        return_value=httpx.Response(
            200,
            json={"count": 1, "next": None, "previous": None, "results": [{"id": 1, "weight": 4.2}]},
        )
    )
    result = await list_weight()
    assert result[0]["weight"] == 4.2


async def test_create_weight(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/weight/").mock(
        return_value=httpx.Response(201, json={"id": 1, "child": 1, "date": "2024-01-01", "weight": 4.2})
    )
    result = await create_weight(child_id=1, date="2024-01-01", weight=4.2)
    assert result["weight"] == 4.2


async def test_update_weight(mock_api: respx.MockRouter) -> None:
    mock_api.patch("/api/weight/1/").mock(
        return_value=httpx.Response(200, json={"id": 1, "weight": 4.5})
    )
    result = await update_weight(1, weight=4.5)
    assert result["weight"] == 4.5


async def test_list_head_circumference(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/head-circumference/").mock(
        return_value=httpx.Response(
            200,
            json={"count": 1, "next": None, "previous": None, "results": [{"id": 1, "head_circumference": 36.0}]},
        )
    )
    result = await list_head_circumference()
    assert result[0]["head_circumference"] == 36.0


async def test_create_head_circumference(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/head-circumference/").mock(
        return_value=httpx.Response(
            201, json={"id": 1, "child": 1, "date": "2024-01-01", "head_circumference": 36.0}
        )
    )
    result = await create_head_circumference(child_id=1, date="2024-01-01", head_circumference=36.0)
    assert result["head_circumference"] == 36.0


async def test_list_temperature(mock_api: respx.MockRouter) -> None:
    mock_api.get("/api/temperature/").mock(
        return_value=httpx.Response(
            200,
            json={"count": 1, "next": None, "previous": None, "results": [{"id": 1, "temperature": 37.2}]},
        )
    )
    result = await list_temperature()
    assert result[0]["temperature"] == 37.2


async def test_create_temperature(mock_api: respx.MockRouter) -> None:
    mock_api.post("/api/temperature/").mock(
        return_value=httpx.Response(
            201, json={"id": 1, "child": 1, "time": "2024-01-15T10:00:00Z", "temperature": 37.2}
        )
    )
    result = await create_temperature(child_id=1, time="2024-01-15T10:00:00", temperature=37.2)
    assert result["temperature"] == 37.2
