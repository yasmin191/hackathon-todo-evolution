"""
Infrastructure Analyzer Blueprint

Analyzes Kubernetes infrastructure and provides:
- Resource optimization suggestions
- Cost analysis
- Security recommendations
- Performance insights
"""

import json
import os
from typing import Any

from openai import OpenAI

from .base import BaseBlueprint, BlueprintResult


class InfraAnalyzerSkill(BaseBlueprint):
    """Blueprint for analyzing and optimizing infrastructure."""

    name = "infra_analyzer"
    description = "Analyzes Kubernetes infrastructure for optimization opportunities"
    version = "1.0.0"

    @property
    def system_prompt(self) -> str:
        return """You are a Kubernetes Infrastructure Expert. Analyze and optimize infrastructure.

Given infrastructure details, provide comprehensive analysis.

Return a JSON object with:
{
    "health_score": 85,
    "resource_analysis": {
        "cpu": {
            "requested": "2000m",
            "used": "800m",
            "efficiency": 40,
            "recommendation": "Reduce CPU requests"
        },
        "memory": {
            "requested": "4Gi",
            "used": "2Gi",
            "efficiency": 50,
            "recommendation": "Memory is appropriately sized"
        }
    },
    "cost_analysis": {
        "current_monthly": 150,
        "optimized_monthly": 100,
        "savings_percentage": 33,
        "recommendations": ["Right-size pods", "Use spot instances"]
    },
    "security_analysis": {
        "score": 70,
        "issues": [
            {"severity": "high", "issue": "Pods running as root", "fix": "Add securityContext"}
        ],
        "passed_checks": ["Network policies in place", "Secrets encrypted"]
    },
    "performance_analysis": {
        "bottlenecks": ["Database connection pool exhausted"],
        "recommendations": ["Increase connection pool", "Add caching layer"]
    },
    "reliability_analysis": {
        "single_points_of_failure": ["Single replica for API"],
        "recommendations": ["Increase replica count", "Add PDB"]
    },
    "action_items": [
        {"priority": "high", "action": "Fix security issues", "effort": "low"},
        {"priority": "medium", "action": "Right-size resources", "effort": "medium"}
    ]
}"""

    def get_capabilities(self) -> list[str]:
        return [
            "resource_optimization",
            "cost_analysis",
            "security_audit",
            "performance_analysis",
            "reliability_assessment",
        ]

    async def generate(self, requirements: dict[str, Any]) -> BlueprintResult:
        """Analyze infrastructure and provide recommendations."""
        resources = requirements.get("resources", [])
        metrics = requirements.get("metrics", {})
        namespace = requirements.get("namespace", "default")

        if not resources:
            # Generate sample analysis for demo
            resources = [
                {
                    "kind": "Deployment",
                    "name": "api",
                    "replicas": 2,
                    "cpu": "500m",
                    "memory": "512Mi",
                },
                {
                    "kind": "Deployment",
                    "name": "frontend",
                    "replicas": 2,
                    "cpu": "200m",
                    "memory": "256Mi",
                },
            ]

        try:
            client = OpenAI(api_key=self.openai_api_key or os.getenv("OPENAI_API_KEY"))

            resources_text = "\n".join(
                [
                    f"- {r.get('kind', 'Unknown')}: {r.get('name', 'unnamed')} "
                    f"(replicas: {r.get('replicas', 1)}, cpu: {r.get('cpu', 'unset')}, "
                    f"memory: {r.get('memory', 'unset')})"
                    for r in resources
                ]
            )

            user_prompt = f"""Analyze this Kubernetes infrastructure:

Namespace: {namespace}

Resources:
{resources_text}

Metrics:
- CPU utilization: {metrics.get("cpu_utilization", "unknown")}
- Memory utilization: {metrics.get("memory_utilization", "unknown")}
- Request latency p95: {metrics.get("latency_p95", "unknown")}
- Error rate: {metrics.get("error_rate", "unknown")}

Cloud provider: {requirements.get("cloud_provider", "unknown")}
Budget constraints: {requirements.get("budget", "none specified")}

Provide comprehensive infrastructure analysis as JSON."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content or "{}")

            # Create analysis report
            report = self._create_report(result, namespace)

            artifacts = {
                "analysis.json": json.dumps(result, indent=2),
                "infrastructure-report.md": report,
            }

            # Extract high priority items as warnings
            warnings = [
                item["action"]
                for item in result.get("action_items", [])
                if item.get("priority") == "high"
            ]

            recommendations = []
            if result.get("cost_analysis", {}).get("savings_percentage"):
                savings = result["cost_analysis"]["savings_percentage"]
                recommendations.append(f"Potential cost savings: {savings}%")

            if result.get("health_score"):
                recommendations.append(
                    f"Infrastructure health score: {result['health_score']}/100"
                )

            return BlueprintResult(
                success=True,
                artifacts=artifacts,
                message=f"Infrastructure analysis complete for namespace '{namespace}'",
                warnings=warnings,
                recommendations=recommendations,
            )

        except Exception as e:
            return BlueprintResult(
                success=False,
                artifacts={},
                message=f"Analysis failed: {str(e)}",
            )

    def _create_report(self, analysis: dict, namespace: str) -> str:
        """Create a markdown report from the analysis."""
        lines = [
            f"# Infrastructure Analysis Report",
            f"**Namespace:** {namespace}",
            f"**Health Score:** {analysis.get('health_score', 'N/A')}/100",
            "",
            "## Executive Summary",
        ]

        # Cost section
        cost = analysis.get("cost_analysis", {})
        if cost:
            lines.extend(
                [
                    "",
                    "### Cost Analysis",
                    f"- Current monthly cost: ${cost.get('current_monthly', 'N/A')}",
                    f"- Optimized monthly cost: ${cost.get('optimized_monthly', 'N/A')}",
                    f"- Potential savings: {cost.get('savings_percentage', 'N/A')}%",
                ]
            )

        # Security section
        security = analysis.get("security_analysis", {})
        if security:
            lines.extend(
                [
                    "",
                    "### Security Analysis",
                    f"**Security Score:** {security.get('score', 'N/A')}/100",
                    "",
                    "#### Issues Found:",
                ]
            )
            for issue in security.get("issues", []):
                lines.append(
                    f"- [{issue.get('severity', 'info').upper()}] {issue.get('issue', '')}"
                )
                lines.append(f"  - Fix: {issue.get('fix', 'N/A')}")

        # Action items
        lines.extend(["", "## Action Items"])
        for item in analysis.get("action_items", []):
            priority = item.get("priority", "medium").upper()
            lines.append(
                f"- [{priority}] {item.get('action', '')} (Effort: {item.get('effort', 'medium')})"
            )

        return "\n".join(lines)
