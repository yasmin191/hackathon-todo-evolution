"""
Deployment Manager Blueprint

Manages Kubernetes deployments with AI assistance:
- Deployment strategy recommendations
- Rollout monitoring
- Rollback suggestions
- Health check analysis
"""

import json
import os
from typing import Any

from openai import OpenAI

from .base import BaseBlueprint, BlueprintResult


class DeploymentManagerSkill(BaseBlueprint):
    """Blueprint for managing Kubernetes deployments."""

    name = "deployment_manager"
    description = "AI-powered deployment management and recommendations"
    version = "1.0.0"

    @property
    def system_prompt(self) -> str:
        return """You are a Kubernetes Deployment Expert. Provide deployment guidance.

Analyze deployment scenarios and provide recommendations.

Return a JSON object with:
{
    "action": "deploy" | "rollback" | "scale" | "update" | "monitor",
    "strategy": {
        "type": "RollingUpdate" | "Recreate" | "BlueGreen" | "Canary",
        "params": {
            "maxSurge": "25%",
            "maxUnavailable": "25%"
        },
        "reason": "Why this strategy"
    },
    "commands": [
        {"command": "kubectl ...", "description": "What it does"}
    ],
    "pre_checks": [
        {"check": "Verify image exists", "command": "docker pull ..."}
    ],
    "post_checks": [
        {"check": "Verify pods healthy", "command": "kubectl get pods"}
    ],
    "risks": ["Potential risks"],
    "rollback_plan": {
        "trigger": "When to rollback",
        "commands": ["kubectl rollout undo ..."]
    },
    "monitoring_queries": [
        {"name": "Error rate", "promql": "rate(http_errors_total[5m])"}
    ]
}"""

    def get_capabilities(self) -> list[str]:
        return [
            "deployment_strategy",
            "rollout_management",
            "rollback_planning",
            "health_monitoring",
            "scaling_recommendations",
        ]

    async def generate(self, requirements: dict[str, Any]) -> BlueprintResult:
        """Generate deployment recommendations and commands."""
        action = requirements.get("action", "deploy")
        app_name = requirements.get("app_name", "my-app")
        namespace = requirements.get("namespace", "default")
        current_state = requirements.get("current_state", {})
        target_state = requirements.get("target_state", {})

        try:
            client = OpenAI(api_key=self.openai_api_key or os.getenv("OPENAI_API_KEY"))

            user_prompt = f"""Provide deployment guidance for:

Action: {action}
Application: {app_name}
Namespace: {namespace}

Current state:
- Replicas: {current_state.get("replicas", "unknown")}
- Image: {current_state.get("image", "unknown")}
- Status: {current_state.get("status", "unknown")}

Target state:
- Replicas: {target_state.get("replicas", "same")}
- Image: {target_state.get("image", "same")}

Environment: {requirements.get("environment", "production")}
Risk tolerance: {requirements.get("risk_tolerance", "low")}

Provide deployment recommendations as JSON."""

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

            # Create runbook artifact
            runbook = self._create_runbook(result, app_name, namespace)

            artifacts = {
                "deployment-plan.json": json.dumps(result, indent=2),
                "runbook.md": runbook,
            }

            return BlueprintResult(
                success=True,
                artifacts=artifacts,
                message=f"Generated {action} plan for {app_name}",
                warnings=result.get("risks", []),
                recommendations=[
                    f"Strategy: {result.get('strategy', {}).get('type', 'RollingUpdate')}",
                    f"Pre-checks: {len(result.get('pre_checks', []))}",
                    f"Post-checks: {len(result.get('post_checks', []))}",
                ],
            )

        except Exception as e:
            return BlueprintResult(
                success=False,
                artifacts={},
                message=f"Deployment planning failed: {str(e)}",
            )

    def _create_runbook(self, plan: dict, app_name: str, namespace: str) -> str:
        """Create a markdown runbook from the deployment plan."""
        lines = [
            f"# Deployment Runbook: {app_name}",
            f"**Namespace:** {namespace}",
            f"**Strategy:** {plan.get('strategy', {}).get('type', 'RollingUpdate')}",
            "",
            "## Pre-Deployment Checks",
        ]

        for check in plan.get("pre_checks", []):
            lines.append(f"- [ ] {check.get('check', '')}")
            if check.get("command"):
                lines.append(f"  ```bash\n  {check['command']}\n  ```")

        lines.extend(["", "## Deployment Commands"])
        for cmd in plan.get("commands", []):
            lines.append(f"### {cmd.get('description', 'Step')}")
            lines.append(f"```bash\n{cmd.get('command', '')}\n```")

        lines.extend(["", "## Post-Deployment Verification"])
        for check in plan.get("post_checks", []):
            lines.append(f"- [ ] {check.get('check', '')}")
            if check.get("command"):
                lines.append(f"  ```bash\n  {check['command']}\n  ```")

        lines.extend(["", "## Rollback Plan"])
        rollback = plan.get("rollback_plan", {})
        lines.append(f"**Trigger:** {rollback.get('trigger', 'On failure')}")
        for cmd in rollback.get("commands", []):
            lines.append(f"```bash\n{cmd}\n```")

        return "\n".join(lines)
