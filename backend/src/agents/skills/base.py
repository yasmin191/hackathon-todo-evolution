"""
Base Skill class for all reusable AI skills.

Each skill is a mini-agent with:
- A specific domain/responsibility
- Its own system prompt
- A set of tools it can use
- An execute method that can be called by the orchestrator
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class SkillResult:
    """Result from skill execution."""

    success: bool
    data: Any
    message: str
    confidence: float = 1.0
    suggestions: list[str] | None = None


class BaseSkill(ABC):
    """Base class for all reusable AI skills."""

    name: str = "base_skill"
    description: str = "Base skill class"
    version: str = "1.0.0"

    def __init__(self, openai_api_key: str | None = None):
        self.openai_api_key = openai_api_key
        self._initialized = False

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this skill."""
        pass

    @abstractmethod
    async def execute(self, input_data: dict[str, Any]) -> SkillResult:
        """Execute the skill with the given input data."""
        pass

    def validate_input(self, input_data: dict[str, Any]) -> tuple[bool, str]:
        """Validate input data before execution."""
        return True, "Valid"

    def get_capabilities(self) -> list[str]:
        """Return list of capabilities this skill provides."""
        return []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} v{self.version}>"
