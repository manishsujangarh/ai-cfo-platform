from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Tool:
    """
    Represents a business tool that can be executed by the AI agent.
    """

    name: str
    description: str
    function: Callable[..., Any]


class ToolRegistry:
    """
    Registry responsible for managing AI tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """
        Register a new tool.

        Raises:
            ValueError: If a tool with the same name already exists.
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        """
        Retrieve a tool by name.

        Raises:
            KeyError: If the tool does not exist.
        """
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"Tool '{name}' is not registered.") from exc

    def exists(self, name: str) -> bool:
        """
        Check whether a tool exists.
        """
        return name in self._tools

    def list_tools(self) -> list[Tool]:
        """
        Return all registered tools.
        """
        return list(self._tools.values())


registry = ToolRegistry()