from typing import Annotated

from fastmcp import FastMCP

from ..client import QueryParams, api_delete, api_list, api_patch, api_post
from ..date_filters import DATE_ARG, DATE_MAX_ARG, DATE_MIN_ARG, apply_date_filters

mcp = FastMCP("diapers")

_COLORS = "black, brown, green, yellow"


@mcp.tool
async def list_diaper_changes(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    date: Annotated[str | None, DATE_ARG] = None,
    date_min: Annotated[str | None, DATE_MIN_ARG] = None,
    date_max: Annotated[str | None, DATE_MAX_ARG] = None,
    wet: Annotated[bool | None, "Filter by wet diaper (True/False)"] = None,
    solid: Annotated[bool | None, "Filter by solid diaper (True/False)"] = None,
    color: Annotated[
        str | None, f"Filter by stool color: {_COLORS}"
    ] = None,
    tags: Annotated[list[str] | None, "Filter by tag names (records having all listed tags)"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'time' or '-time' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List diaper change records with optional filters."""
    params: QueryParams = {"limit": limit}
    if child_id is not None:
        params["child"] = child_id
    apply_date_filters(params, date=date, date_min=date_min, date_max=date_max)
    if wet is not None:
        params["wet"] = wet
    if solid is not None:
        params["solid"] = solid
    if color is not None:
        params["color"] = color
    if tags:
        params["tags"] = ",".join(tags)
    if ordering is not None:
        params["ordering"] = ordering
    return await api_list("changes", params)


@mcp.tool
async def create_diaper_change(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    time: Annotated[str, "Time of the change in ISO 8601 format (e.g. 2024-01-15T14:30:00)"],
    wet: Annotated[bool, "Whether the diaper was wet"],
    solid: Annotated[bool, "Whether the diaper had solid contents"],
    color: Annotated[str | None, f"Stool color: {_COLORS}"] = None,
    amount: Annotated[float | None, "Amount/volume of contents (arbitrary units)"] = None,
    notes: Annotated[str | None, "Optional notes"] = None,
) -> dict[str, object]:
    """Record a diaper change event."""
    data: dict[str, object] = {
        "child": child_id,
        "time": time,
        "wet": wet,
        "solid": solid,
    }
    if color is not None:
        data["color"] = color
    if amount is not None:
        data["amount"] = amount
    if notes is not None:
        data["notes"] = notes
    return await api_post("changes", data)


@mcp.tool
async def update_diaper_change(
    change_id: Annotated[int, "ID of the diaper change record to update"],
    time: Annotated[str | None, "New time in ISO 8601 format"] = None,
    wet: Annotated[bool | None, "Whether the diaper was wet"] = None,
    solid: Annotated[bool | None, "Whether the diaper had solid contents"] = None,
    color: Annotated[str | None, f"Stool color: {_COLORS}"] = None,
    amount: Annotated[float | None, "New amount"] = None,
    notes: Annotated[str | None, "New notes"] = None,
) -> dict[str, object]:
    """Update an existing diaper change record. Only provided fields are changed."""
    data: dict[str, object] = {}
    if time is not None:
        data["time"] = time
    if wet is not None:
        data["wet"] = wet
    if solid is not None:
        data["solid"] = solid
    if color is not None:
        data["color"] = color
    if amount is not None:
        data["amount"] = amount
    if notes is not None:
        data["notes"] = notes
    return await api_patch("changes", change_id, data)


@mcp.tool
async def delete_diaper_change(
    change_id: Annotated[int, "ID of the diaper change record to permanently delete"],
) -> str:
    """Delete a diaper change record. This action is permanent."""
    await api_delete("changes", change_id)
    return f"Diaper change {change_id} deleted successfully."
