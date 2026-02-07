"""
Blueprint Orchestrator

Coordinates cloud-native blueprint skills for infrastructure management.
"""

import asyncio
from typing import Any

from .base import BlueprintResult
from .deployment_manager import DeploymentManagerSkill
from .helm_builder import HelmChartBuilderSkill
from .infra_analyzer import InfraAnalyzerSkill
from .k8s_generator import K8sManifestGeneratorSkill


class BlueprintOrchestrator:
    """
    Orchestrates cloud-native blueprint skills for comprehensive
    infrastructure management via natural language.
    """

    def __init__(self, openai_api_key: str | None = None):
        self.openai_api_key = openai_api_key

        self.blueprints = {
            "k8s": K8sManifestGeneratorSkill(openai_api_key),
            "helm": HelmChartBuilderSkill(openai_api_key),
            "deploy": DeploymentManagerSkill(openai_api_key),
            "analyze": InfraAnalyzerSkill(openai_api_key),
        }

    async def generate_k8s_manifests(
        self,
        description: str,
        app_name: str = "my-app",
        **kwargs: Any,
    ) -> BlueprintResult:
        """Generate Kubernetes manifests from natural language."""
        return await self.blueprints["k8s"].generate(
            {
                "description": description,
                "app_name": app_name,
                **kwargs,
            }
        )

    async def generate_helm_chart(
        self,
        description: str,
        chart_name: str = "my-chart",
        **kwargs: Any,
    ) -> BlueprintResult:
        """Generate a Helm chart from natural language."""
        return await self.blueprints["helm"].generate(
            {
                "description": description,
                "chart_name": chart_name,
                **kwargs,
            }
        )

    async def plan_deployment(
        self,
        action: str,
        app_name: str,
        **kwargs: Any,
    ) -> BlueprintResult:
        """Get deployment recommendations and runbook."""
        return await self.blueprints["deploy"].generate(
            {
                "action": action,
                "app_name": app_name,
                **kwargs,
            }
        )

    async def analyze_infrastructure(
        self,
        resources: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> BlueprintResult:
        """Analyze infrastructure and get optimization recommendations."""
        return await self.blueprints["analyze"].generate(
            {
                "resources": resources or [],
                **kwargs,
            }
        )

    async def full_stack_generation(
        self,
        description: str,
        app_name: str,
        **kwargs: Any,
    ) -> dict[str, BlueprintResult]:
        """
        Generate complete infrastructure stack:
        - Kubernetes manifests
        - Helm chart
        - Deployment plan
        """
        results = {}

        # Run all generators in parallel
        tasks = [
            (
                "k8s_manifests",
                self.blueprints["k8s"].generate(
                    {
                        "description": description,
                        "app_name": app_name,
                        **kwargs,
                    }
                ),
            ),
            (
                "helm_chart",
                self.blueprints["helm"].generate(
                    {
                        "description": description,
                        "chart_name": app_name,
                        **kwargs,
                    }
                ),
            ),
            (
                "deployment_plan",
                self.blueprints["deploy"].generate(
                    {
                        "action": "deploy",
                        "app_name": app_name,
                        **kwargs,
                    }
                ),
            ),
        ]

        task_results = await asyncio.gather(
            *[t[1] for t in tasks],
            return_exceptions=True,
        )

        for (name, _), result in zip(tasks, task_results):
            if isinstance(result, Exception):
                results[name] = BlueprintResult(
                    success=False,
                    artifacts={},
                    message=f"Failed: {str(result)}",
                )
            else:
                results[name] = result

        return results

    def get_available_blueprints(self) -> list[dict[str, Any]]:
        """Get information about all available blueprints."""
        return [
            {
                "name": bp.name,
                "description": bp.description,
                "version": bp.version,
                "capabilities": bp.get_capabilities(),
            }
            for bp in self.blueprints.values()
        ]
