"""
Helm Chart Builder Blueprint

Creates Helm charts from natural language requirements.
Generates Chart.yaml, values.yaml, templates, and helpers.
"""

import json
import os
from typing import Any

from openai import OpenAI

from .base import BaseBlueprint, BlueprintResult


class HelmChartBuilderSkill(BaseBlueprint):
    """Blueprint for generating Helm charts from requirements."""

    name = "helm_chart_builder"
    description = "Creates complete Helm charts from natural language requirements"
    version = "1.0.0"

    @property
    def system_prompt(self) -> str:
        return """You are a Helm Chart Expert. Create production-ready Helm charts.

Given requirements, generate a complete Helm chart structure.

Return a JSON object with:
{
    "chart_name": "my-chart",
    "files": {
        "Chart.yaml": "... yaml content ...",
        "values.yaml": "... yaml content ...",
        "templates/deployment.yaml": "... template content ...",
        "templates/service.yaml": "... template content ...",
        "templates/_helpers.tpl": "... helper content ...",
        "templates/NOTES.txt": "... notes content ..."
    },
    "dependencies": [
        {"name": "postgresql", "version": "12.0.0", "repository": "https://charts.bitnami.com/bitnami"}
    ],
    "usage_instructions": "How to install and configure the chart",
    "customization_options": ["List of key values that can be customized"]
}

Best practices:
1. Use template functions for reusability
2. Provide sensible defaults in values.yaml
3. Include resource limits as configurable values
4. Support multiple environments via values files
5. Include proper NOTES.txt for post-install info
6. Use named templates in _helpers.tpl
7. Support ingress, HPA, PDB as optional features"""

    def get_capabilities(self) -> list[str]:
        return [
            "chart_generation",
            "template_creation",
            "values_configuration",
            "dependency_management",
            "multi_environment_support",
        ]

    async def generate(self, requirements: dict[str, Any]) -> BlueprintResult:
        """Generate a Helm chart from requirements."""
        description = requirements.get("description", "")
        chart_name = requirements.get("chart_name", "my-app")
        app_version = requirements.get("app_version", "1.0.0")
        chart_version = requirements.get("chart_version", "0.1.0")

        if not description:
            return BlueprintResult(
                success=False,
                artifacts={},
                message="Description is required for chart generation",
            )

        try:
            client = OpenAI(api_key=self.openai_api_key or os.getenv("OPENAI_API_KEY"))

            user_prompt = f"""Create a Helm chart for:

Description: {description}

Chart details:
- Chart name: {chart_name}
- App version: {app_version}
- Chart version: {chart_version}

Features needed: {requirements.get("features", ["deployment", "service"])}
Environment: {requirements.get("environment", "production")}

Generate a complete Helm chart as JSON."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content or "{}")
            files = result.get("files", {})

            # Prefix files with chart name
            artifacts = {}
            for path, content in files.items():
                full_path = f"{chart_name}/{path}"
                artifacts[full_path] = content

            recommendations = result.get("customization_options", [])
            if result.get("usage_instructions"):
                recommendations.insert(0, result["usage_instructions"])

            return BlueprintResult(
                success=True,
                artifacts=artifacts,
                message=f"Generated Helm chart '{chart_name}' with {len(files)} files",
                warnings=[],
                recommendations=recommendations,
            )

        except Exception as e:
            return BlueprintResult(
                success=False,
                artifacts={},
                message=f"Chart generation failed: {str(e)}",
            )
