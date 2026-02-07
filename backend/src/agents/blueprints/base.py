"""
Base Blueprint class for cloud-native infrastructure skills.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BlueprintResult:
    """Result from blueprint execution."""

    success: bool
    artifacts: dict[str, str]  # filename -> content
    message: str
    warnings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


class BaseBlueprint(ABC):
    """Base class for cloud-native blueprint skills."""

    name: str = "base_blueprint"
    description: str = "Base blueprint class"
    version: str = "1.0.0"

    def __init__(self, openai_api_key: str | None = None):
        self.openai_api_key = openai_api_key

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this blueprint."""
        pass

    @abstractmethod
    async def generate(self, requirements: dict[str, Any]) -> BlueprintResult:
        """Generate infrastructure artifacts from requirements."""
        pass

    def validate_requirements(self, requirements: dict[str, Any]) -> tuple[bool, str]:
        """Validate requirements before generation."""
        return True, "Valid"

    def get_capabilities(self) -> list[str]:
        """Return list of capabilities this blueprint provides."""
        return []
