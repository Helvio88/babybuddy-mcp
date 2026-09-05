from pathlib import Path
from typing import Annotated

from fastmcp import FastMCP

from ..client import (
    QueryParams,
    api_delete,
    api_list,
    api_patch,
    api_patch_multipart,
    api_post,
    api_post_multipart,
)
from ..date_filters import DATE_ARG, DATE_MAX_ARG, DATE_MIN_ARG, apply_date_filters

mcp = FastMCP("notes")


def _read_image(image_path: str) -> dict[str, tuple[str, bytes]]:
    path = Path(image_path)
    return {"image": (path.name, path.read_bytes())}


# ── Notes ─────────────────────────────────────────────────────────────────────


@mcp.tool
async def list_notes(
    child_id: Annotated[int | None, "Filter by child ID. Use list_children to get IDs."] = None,
    date: Annotated[str | None, DATE_ARG] = None,
    date_min: Annotated[str | None, DATE_MIN_ARG] = None,
    date_max: Annotated[str | None, DATE_MAX_ARG] = None,
    tags: Annotated[list[str] | None, "Filter by tag names (notes having all listed tags)"] = None,
    ordering: Annotated[str | None, "Order by field, e.g. 'time' or '-time' (descending)"] = None,
    limit: Annotated[int, "Maximum number of records to return"] = 50,
) -> list[dict[str, object]]:
    """List notes with optional filters."""
    params: QueryParams = {"limit": limit}
    if child_id is not None:
        params["child"] = child_id
    apply_date_filters(params, date=date, date_min=date_min, date_max=date_max)
    if tags:
        params["tags"] = ",".join(tags)
    if ordering is not None:
        params["ordering"] = ordering
    return await api_list("notes", params)


@mcp.tool
async def create_note(
    child_id: Annotated[int, "ID of the child. Use list_children to get IDs."],
    note: Annotated[str, "The note text content"],
    time: Annotated[str, "Time of the note in ISO 8601 format (e.g. 2024-01-15T14:30:00)"],
    tags: Annotated[list[str] | None, "List of tag names to apply to this note"] = None,
    image_path: Annotated[
        str | None, "Path to a local image file to attach to the note"
    ] = None,
) -> dict[str, object]:
    """Create a new note for a child. Optionally attach an image."""
    if image_path is not None:
        form: dict[str, object] = {"child": child_id, "note": note, "time": time}
        if tags is not None:
            form["tags"] = tags
        return await api_post_multipart("notes", form, _read_image(image_path))
    data: dict[str, object] = {"child": child_id, "note": note, "time": time}
    if tags is not None:
        data["tags"] = tags
    return await api_post("notes", data)


@mcp.tool
async def update_note(
    note_id: Annotated[int, "ID of the note to update"],
    note: Annotated[str | None, "New note text"] = None,
    time: Annotated[str | None, "New time in ISO 8601 format"] = None,
    tags: Annotated[list[str] | None, "New list of tag names (replaces existing tags)"] = None,
    image_path: Annotated[
        str | None, "Path to a local image file to attach to the note"
    ] = None,
) -> dict[str, object]:
    """Update an existing note. Only provided fields are changed."""
    data: dict[str, object] = {}
    if note is not None:
        data["note"] = note
    if time is not None:
        data["time"] = time
    if tags is not None:
        data["tags"] = tags
    if image_path is not None:
        return await api_patch_multipart("notes", note_id, data, _read_image(image_path))
    return await api_patch("notes", note_id, data)


@mcp.tool
async def delete_note(
    note_id: Annotated[int, "ID of the note to permanently delete"],
) -> str:
    """Delete a note. This action is permanent."""
    await api_delete("notes", note_id)
    return f"Note {note_id} deleted successfully."


# ── Tags ──────────────────────────────────────────────────────────────────────


@mcp.tool
async def list_tags() -> list[dict[str, object]]:
    """List all available tags that can be applied to notes."""
    return await api_list("tags")


@mcp.tool
async def create_tag(
    name: Annotated[str, "Tag name"],
    color: Annotated[str | None, "Tag color as a hex code (e.g. #ff5733)"] = None,
) -> dict[str, object]:
    """Create a new tag."""
    data: dict[str, object] = {"name": name}
    if color is not None:
        data["color"] = color
    return await api_post("tags", data)


@mcp.tool
async def update_tag(
    slug: Annotated[str, "Slug of the tag to update (the 'slug' field from list_tags)"],
    name: Annotated[str | None, "New tag name"] = None,
    color: Annotated[str | None, "New color as a hex code (e.g. #ff5733)"] = None,
) -> dict[str, object]:
    """Update an existing tag by slug. Tags are keyed by slug, not numeric ID."""
    data: dict[str, object] = {}
    if name is not None:
        data["name"] = name
    if color is not None:
        data["color"] = color
    return await api_patch("tags", slug, data)


@mcp.tool
async def delete_tag(
    slug: Annotated[str, "Slug of the tag to permanently delete (the 'slug' field from list_tags)"],
) -> str:
    """Delete a tag by slug. This action is permanent and removes the tag from all notes."""
    await api_delete("tags", slug)
    return f"Tag {slug} deleted successfully."
