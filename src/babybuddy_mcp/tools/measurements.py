from typing import Annotated

from fastmcp import FastMCP

from ..client import QueryParams, api_delete, api_list, api_patch, api_post
from ..date_filters import DATE_ARG, DATE_MAX_ARG, DATE_MIN_ARG, apply_date_filters

mcp = FastMCP("measurements")


def _measure_params(
    child_id: int | None,
    date: str | None,
    ordering: str | None,
    limit: int,
) -> QueryParams:
    """Build list params for BMI/height/weight/head-circumference.

    Upstream only exposes exact `date` matching for these resources (no range).
    """
    params: QueryParams = {"limit": limit}
    if child_id is not None:
        params["child"] = child_id
    if date is not None:
        params["date"] = date
    if ordering is not None:
        params["ordering"] = ordering
    return params


# ── BMI ───────────────────────────────────────────────────────────────────────


@mcp.tool
async def list_bmi(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    date: Annotated[str | None, "Filter by exact date, YYYY-MM-DD"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'date' or '-date' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List BMI measurements."""
    return await api_list("bmi", _measure_params(child_id, date, ordering, limit))


@mcp.tool
async def create_bmi(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    date: Annotated[str, "Measurement date in YYYY-MM-DD format"],
    bmi: Annotated[float, "BMI value"],
    notes: Annotated[str | None, "Optional notes"] = None,
) -> dict[str, object]:
    """Record a BMI measurement."""
    data: dict[str, object] = {"child": child_id, "date": date, "bmi": bmi}
    if notes is not None:
        data["notes"] = notes
    return await api_post("bmi", data)


@mcp.tool
async def update_bmi(
    bmi_id: Annotated[int, "ID of the BMI record to update"],
    date: Annotated[str | None, "New date in YYYY-MM-DD format"] = None,
    bmi: Annotated[float | None, "New BMI value"] = None,
    notes: Annotated[str | None, "New notes"] = None,
) -> dict[str, object]:
    """Update an existing BMI record. Only provided fields are changed."""
    data: dict[str, object] = {}
    if date is not None:
        data["date"] = date
    if bmi is not None:
        data["bmi"] = bmi
    if notes is not None:
        data["notes"] = notes
    return await api_patch("bmi", bmi_id, data)


@mcp.tool
async def delete_bmi(
    bmi_id: Annotated[int, "ID of the BMI record to permanently delete"],
) -> str:
    """Delete a BMI record. This action is permanent."""
    await api_delete("bmi", bmi_id)
    return f"BMI record {bmi_id} deleted successfully."


# ── Height ────────────────────────────────────────────────────────────────────


@mcp.tool
async def list_height(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    date: Annotated[str | None, "Filter by exact date, YYYY-MM-DD"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'date' or '-date' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List height measurements."""
    return await api_list("height", _measure_params(child_id, date, ordering, limit))


@mcp.tool
async def create_height(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    date: Annotated[str, "Measurement date in YYYY-MM-DD format"],
    height: Annotated[float, "Height in centimeters"],
    notes: Annotated[str | None, "Optional notes"] = None,
) -> dict[str, object]:
    """Record a height measurement."""
    data: dict[str, object] = {"child": child_id, "date": date, "height": height}
    if notes is not None:
        data["notes"] = notes
    return await api_post("height", data)


@mcp.tool
async def update_height(
    height_id: Annotated[int, "ID of the height record to update"],
    date: Annotated[str | None, "New date in YYYY-MM-DD format"] = None,
    height: Annotated[float | None, "New height in centimeters"] = None,
    notes: Annotated[str | None, "New notes"] = None,
) -> dict[str, object]:
    """Update an existing height record. Only provided fields are changed."""
    data: dict[str, object] = {}
    if date is not None:
        data["date"] = date
    if height is not None:
        data["height"] = height
    if notes is not None:
        data["notes"] = notes
    return await api_patch("height", height_id, data)


@mcp.tool
async def delete_height(
    height_id: Annotated[int, "ID of the height record to permanently delete"],
) -> str:
    """Delete a height record. This action is permanent."""
    await api_delete("height", height_id)
    return f"Height record {height_id} deleted successfully."


# ── Weight ────────────────────────────────────────────────────────────────────


@mcp.tool
async def list_weight(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    date: Annotated[str | None, "Filter by exact date, YYYY-MM-DD"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'date' or '-date' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List weight measurements."""
    return await api_list("weight", _measure_params(child_id, date, ordering, limit))


@mcp.tool
async def create_weight(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    date: Annotated[str, "Measurement date in YYYY-MM-DD format"],
    weight: Annotated[float, "Weight in kilograms"],
    notes: Annotated[str | None, "Optional notes"] = None,
) -> dict[str, object]:
    """Record a weight measurement."""
    data: dict[str, object] = {"child": child_id, "date": date, "weight": weight}
    if notes is not None:
        data["notes"] = notes
    return await api_post("weight", data)


@mcp.tool
async def update_weight(
    weight_id: Annotated[int, "ID of the weight record to update"],
    date: Annotated[str | None, "New date in YYYY-MM-DD format"] = None,
    weight: Annotated[float | None, "New weight in kilograms"] = None,
    notes: Annotated[str | None, "New notes"] = None,
) -> dict[str, object]:
    """Update an existing weight record. Only provided fields are changed."""
    data: dict[str, object] = {}
    if date is not None:
        data["date"] = date
    if weight is not None:
        data["weight"] = weight
    if notes is not None:
        data["notes"] = notes
    return await api_patch("weight", weight_id, data)


@mcp.tool
async def delete_weight(
    weight_id: Annotated[int, "ID of the weight record to permanently delete"],
) -> str:
    """Delete a weight record. This action is permanent."""
    await api_delete("weight", weight_id)
    return f"Weight record {weight_id} deleted successfully."


# ── Head Circumference ────────────────────────────────────────────────────────


@mcp.tool
async def list_head_circumference(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    date: Annotated[str | None, "Filter by exact date, YYYY-MM-DD"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'date' or '-date' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List head circumference measurements."""
    return await api_list(
        "head-circumference", _measure_params(child_id, date, ordering, limit)
    )


@mcp.tool
async def create_head_circumference(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    date: Annotated[str, "Measurement date in YYYY-MM-DD format"],
    head_circumference: Annotated[float, "Head circumference in centimeters"],
    notes: Annotated[str | None, "Optional notes"] = None,
) -> dict[str, object]:
    """Record a head circumference measurement."""
    data: dict[str, object] = {
        "child": child_id,
        "date": date,
        "head_circumference": head_circumference,
    }
    if notes is not None:
        data["notes"] = notes
    return await api_post("head-circumference", data)


@mcp.tool
async def update_head_circumference(
    head_circumference_id: Annotated[int, "ID of the head circumference record to update"],
    date: Annotated[str | None, "New date in YYYY-MM-DD format"] = None,
    head_circumference: Annotated[float | None, "New head circumference in centimeters"] = None,
    notes: Annotated[str | None, "New notes"] = None,
) -> dict[str, object]:
    """Update an existing head circumference record. Only provided fields are changed."""
    data: dict[str, object] = {}
    if date is not None:
        data["date"] = date
    if head_circumference is not None:
        data["head_circumference"] = head_circumference
    if notes is not None:
        data["notes"] = notes
    return await api_patch("head-circumference", head_circumference_id, data)


@mcp.tool
async def delete_head_circumference(
    head_circumference_id: Annotated[int, "ID of the head circumference record to permanently delete"],
) -> str:
    """Delete a head circumference record. This action is permanent."""
    await api_delete("head-circumference", head_circumference_id)
    return f"Head circumference record {head_circumference_id} deleted successfully."


# ── Temperature ───────────────────────────────────────────────────────────────


@mcp.tool
async def list_temperature(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    date: Annotated[str | None, DATE_ARG] = None,
    date_min: Annotated[str | None, DATE_MIN_ARG] = None,
    date_max: Annotated[str | None, DATE_MAX_ARG] = None,
    tags: Annotated[list[str] | None, "Filter by tag names (records having all listed tags)"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'time' or '-time' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List temperature readings."""
    params: QueryParams = {"limit": limit}
    if child_id is not None:
        params["child"] = child_id
    apply_date_filters(params, date=date, date_min=date_min, date_max=date_max)
    if tags:
        params["tags"] = ",".join(tags)
    if ordering is not None:
        params["ordering"] = ordering
    return await api_list("temperature", params)


@mcp.tool
async def create_temperature(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    time: Annotated[str, "Time of reading in ISO 8601 format (e.g. 2024-01-15T14:30:00)"],
    temperature: Annotated[float, "Temperature value (units depend on babybuddy settings)"],
    notes: Annotated[str | None, "Optional notes"] = None,
) -> dict[str, object]:
    """Record a temperature reading."""
    data: dict[str, object] = {"child": child_id, "time": time, "temperature": temperature}
    if notes is not None:
        data["notes"] = notes
    return await api_post("temperature", data)


@mcp.tool
async def update_temperature(
    temperature_id: Annotated[int, "ID of the temperature record to update"],
    time: Annotated[str | None, "New time in ISO 8601 format"] = None,
    temperature: Annotated[float | None, "New temperature value"] = None,
    notes: Annotated[str | None, "New notes"] = None,
) -> dict[str, object]:
    """Update an existing temperature record. Only provided fields are changed."""
    data: dict[str, object] = {}
    if time is not None:
        data["time"] = time
    if temperature is not None:
        data["temperature"] = temperature
    if notes is not None:
        data["notes"] = notes
    return await api_patch("temperature", temperature_id, data)


@mcp.tool
async def delete_temperature(
    temperature_id: Annotated[int, "ID of the temperature record to permanently delete"],
) -> str:
    """Delete a temperature record. This action is permanent."""
    await api_delete("temperature", temperature_id)
    return f"Temperature record {temperature_id} deleted successfully."
