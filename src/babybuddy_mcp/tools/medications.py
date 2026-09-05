from typing import Annotated

from fastmcp import FastMCP

from ..client import QueryParams, api_delete, api_list, api_patch, api_post
from ..date_filters import DATE_ARG, DATE_MAX_ARG, DATE_MIN_ARG, apply_date_filters

mcp = FastMCP("medications")

_DOSAGE_UNITS = "mg, ml, tablets, drops"


@mcp.tool
async def list_medications(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    name: Annotated[str | None, "Filter by exact medication name"] = None,
    dosage_unit: Annotated[str | None, f"Filter by dosage unit: {_DOSAGE_UNITS}"] = None,
    date: Annotated[str | None, DATE_ARG] = None,
    date_min: Annotated[str | None, DATE_MIN_ARG] = None,
    date_max: Annotated[str | None, DATE_MAX_ARG] = None,
    tags: Annotated[list[str] | None, "Filter by tag names (records having all listed tags)"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'time' or '-time' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List medication administration records with optional filters."""
    params: QueryParams = {"limit": limit}
    if child_id is not None:
        params["child"] = child_id
    if name is not None:
        params["name"] = name
    if dosage_unit is not None:
        params["dosage_unit"] = dosage_unit
    apply_date_filters(params, date=date, date_min=date_min, date_max=date_max)
    if tags:
        params["tags"] = ",".join(tags)
    if ordering is not None:
        params["ordering"] = ordering
    return await api_list("medication", params)


@mcp.tool
async def create_medication(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    name: Annotated[str, "Medication name"],
    dosage: Annotated[float | None, "Dosage amount"] = None,
    dosage_unit: Annotated[str | None, f"Dosage unit: {_DOSAGE_UNITS}"] = None,
    time: Annotated[
        str | None,
        "Time administered in ISO 8601 format (e.g. 2024-01-15T14:30:00). Defaults to now.",
    ] = None,
    next_dose_interval: Annotated[
        str | None,
        "Interval until the next dose as a duration string (e.g. '04:00:00' for 4 hours)",
    ] = None,
    notes: Annotated[str | None, "Optional notes"] = None,
    tags: Annotated[list[str] | None, "List of tag names to apply"] = None,
) -> dict[str, object]:
    """Record a medication administration for a child."""
    data: dict[str, object] = {"child": child_id, "name": name}
    if dosage is not None:
        data["dosage"] = dosage
    if dosage_unit is not None:
        data["dosage_unit"] = dosage_unit
    if time is not None:
        data["time"] = time
    if next_dose_interval is not None:
        data["next_dose_interval"] = next_dose_interval
    if notes is not None:
        data["notes"] = notes
    if tags is not None:
        data["tags"] = tags
    return await api_post("medication", data)


@mcp.tool
async def update_medication(
    medication_id: Annotated[int, "ID of the medication record to update"],
    name: Annotated[str | None, "New medication name"] = None,
    dosage: Annotated[float | None, "New dosage amount"] = None,
    dosage_unit: Annotated[str | None, f"New dosage unit: {_DOSAGE_UNITS}"] = None,
    time: Annotated[str | None, "New time in ISO 8601 format"] = None,
    next_dose_interval: Annotated[
        str | None, "New interval until next dose as a duration string (e.g. '04:00:00')"
    ] = None,
    notes: Annotated[str | None, "New notes"] = None,
    tags: Annotated[list[str] | None, "New list of tag names (replaces existing tags)"] = None,
) -> dict[str, object]:
    """Update an existing medication record. Only provided fields are changed."""
    data: dict[str, object] = {}
    if name is not None:
        data["name"] = name
    if dosage is not None:
        data["dosage"] = dosage
    if dosage_unit is not None:
        data["dosage_unit"] = dosage_unit
    if time is not None:
        data["time"] = time
    if next_dose_interval is not None:
        data["next_dose_interval"] = next_dose_interval
    if notes is not None:
        data["notes"] = notes
    if tags is not None:
        data["tags"] = tags
    return await api_patch("medication", medication_id, data)


@mcp.tool
async def delete_medication(
    medication_id: Annotated[int, "ID of the medication record to permanently delete"],
) -> str:
    """Delete a medication record. This action is permanent."""
    await api_delete("medication", medication_id)
    return f"Medication record {medication_id} deleted successfully."
