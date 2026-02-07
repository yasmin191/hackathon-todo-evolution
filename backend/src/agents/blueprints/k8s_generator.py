"""
Kubernetes Manifest Generator Blueprint

Generates Kubernetes YAML manifests from natural language descriptions.
Supports: Deployments, Services, ConfigMaps, Secrets, Ingress, HPA, PDB, etc.
"""

import json
import os
from typing import Any

import yaml
from openai import OpenAI

from .base import BaseBlueprint, BlueprintResult


class K8sManifestGeneratorSkill(BaseBlueprint):
    """Blueprint for generating Kubernetes manifests from natural language."""

    name = "k8s_manifest_generator"
    description = (
        "Generates Kubernetes YAML manifests from natural language descriptions"
    )
    version = "1.0.0"

    @property
    def system_prompt(self) -> str:
        return """You are a Kubernetes Expert. Generate production-ready Kubernetes manifests.

Given a natural language description, create appropriate K8s resources.

Return a JSON object with:
{
    "resources": [
        {
            "kind": "Deployment" | "Service" | "ConfigMap" | "Secret" | "Ingress" | "HPA" | etc,
            "name": "resource-name",
            "manifest": { ... full K8s manifest as JSON ... }
        }
    ],
    "notes": ["Important notes about the generated resources"],
    "security_considerations": ["Security best practices applied"],
    "missing_info": ["Information needed for complete manifest"]
}

Best practices to apply:
1. Use appropriate resource limits and requests
2. Include health checks (liveness/readiness probes)
3. Use non-root security contexts
4. Include appropriate labels and annotations
5. Use namespaces appropriately
6. Include PodDisruptionBudget for production
7. Use ConfigMaps/Secrets for configuration
8. Include NetworkPolicies when applicable"""

    def get_capabilities(self) -> list[str]:
        return [
            "deployment_generation",
            "service_generation",
            "ingress_generation",
            "configmap_generation",
            "secret_generation",
            "hpa_generation",
            "pdb_generation",
            "networkpolicy_generation",
        ]

    async def generate(self, requirements: dict[str, Any]) -> BlueprintResult:
        """Generate Kubernetes manifests from requirements."""
        description = requirements.get("description", "")
        app_name = requirements.get("app_name", "my-app")
        namespace = requirements.get("namespace", "default")
        replicas = requirements.get("replicas", 2)
        image = requirements.get("image", "nginx:latest")
        port = requirements.get("port", 80)

        if not description:
            return BlueprintResult(
                success=False,
                artifacts={},
                message="Description is required for manifest generation",
            )

        try:
            client = OpenAI(api_key=self.openai_api_key or os.getenv("OPENAI_API_KEY"))

            user_prompt = f"""Generate Kubernetes manifests for:

Description: {description}

Details:
- Application name: {app_name}
- Namespace: {namespace}
- Replicas: {replicas}
- Container image: {image}
- Port: {port}

Additional requirements: {requirements.get("additional", "None")}

Generate production-ready manifests as JSON."""

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
            resources = result.get("resources", [])

            # Convert to YAML files
            artifacts = {}
            for resource in resources:
                kind = resource.get("kind", "Unknown").lower()
                name = resource.get("name", "resource")
                manifest = resource.get("manifest", {})

                filename = f"{name}-{kind}.yaml"
                artifacts[filename] = yaml.dump(manifest, default_flow_style=False)

            # Create combined manifest
            if artifacts:
                combined = "\n---\n".join(artifacts.values())
                artifacts["all-resources.yaml"] = combined

            return BlueprintResult(
                success=True,
                artifacts=artifacts,
                message=f"Generated {len(resources)} Kubernetes resources",
                warnings=result.get("missing_info", []),
                recommendations=result.get("security_considerations", []),
            )

        except Exception as e:
            return BlueprintResult(
                success=False,
                artifacts={},
                message=f"Generation failed: {str(e)}",
            )
