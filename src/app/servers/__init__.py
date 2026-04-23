"""Server package exports."""

from typing import Any

from app.tools import __getattr__ as _get_tool_attr

__all__ = [
	"product_recommendations",
	"inventory_check",
	"calculate_discount",
	"create_image",
]


def __getattr__(name: str) -> Any:
	return _get_tool_attr(name)