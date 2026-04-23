# tools package
"""Lazy tool exports for runtime call sites."""

from importlib import import_module
from typing import Any

_TOOL_MODULES = {
	"product_recommendations": "aiSearchTools",
	"inventory_check": "inventoryCheck",
	"calculate_discount": "discountLogic",
	"create_image": "imageCreationTool",
}

__all__ = list(_TOOL_MODULES)


def __getattr__(name: str) -> Any:
	module_name = _TOOL_MODULES.get(name)
	if module_name is None:
		raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

	module = import_module(f".{module_name}", __name__)
	return getattr(module, name)