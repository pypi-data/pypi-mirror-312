"""Tool Inventory Router.

This module contains the API routes for managing tools in the tool inventory.
It provides endpoints for creating, reading, and updating tools.

Routes:
    - POST /api/tool: Create a new tool.
    - GET /api/tool/{tool_id}: Get a tool by its ID.
    - GET /api/tool: Get tools by name.
    - PATCH /api/tool/{tool_id}: Update an existing tool.
"""

from __future__ import annotations

__all__: list[str] = ["router"]

from uuid import UUID  # noqa: TC003

from fastapi import APIRouter, status
from sqlmodel import Session

from tool_inventory.connections import Database, engine
from tool_inventory.models import Tool, ToolCreate, ToolPatch  # noqa: TC001

router = APIRouter(prefix="/api/tool")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a tool",
)
async def create_tool(
    tool: ToolCreate,
) -> Tool:
    """Create a new tool.

    Args:
        tool: The tool creation model.

    Returns:
        The created tool.
    """
    with Session(engine) as session:
        db = Database(session)
        return db.create_tool(tool.to_model())


@router.get(
    "/{tool_id}",
    summary="Get a tool by ID",
)
async def get_tool_by_id(
    tool_id: UUID,
) -> Tool:
    """Get a tool by its ID.

    Args:
        tool_id: The UUID of the tool.

    Returns:
        The tool with the specified ID.
    """
    with Session(engine) as session:
        db = Database(session)
        return db.get_tool_by_id(tool_id)


@router.get(
    "/",
    summary="Get tools",
)
async def get_tools(
    name: str | None = None,
) -> list[Tool]:
    """Get tools by name.

    Args:
        name: The name of the tool to filter by.

    Returns:
        A list of tools.
    """
    with Session(engine) as session:
        db = Database(session)
        return db.get_tools(name=name)


@router.patch(
    "/{tool_id}",
    summary="Update a tool",
)
async def update_tool(
    tool_id: UUID,
    tool_patch: ToolPatch,
) -> Tool:
    """Update an existing tool.

    Args:
        tool_id: The UUID of the tool to update.
        tool_patch: The tool patch model.

    Returns:
        The updated tool.
    """
    with Session(engine) as session:
        db = Database(session)
        tool = db.get_tool_by_id(tool_id)
        tool_patch.patch(tool)
        return db.update_tool(tool)
