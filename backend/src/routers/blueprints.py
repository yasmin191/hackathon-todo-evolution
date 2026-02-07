"""
Cloud-Native Blueprints API Router

Exposes infrastructure generation skills as REST endpoints.
"""

from typing import Any

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from ..agents.blueprints import BlueprintOrchestrator

router = APIRouter(prefix="/blueprints", tags=["Blueprints"])

# Initialize orchestrator
orchestrator = BlueprintOrchestrator()


class K8sRequest(BaseModel):
    """Request for K8s manifest generation."""

    description: str
    app_name: str = "my-app"
    namespace: str = "default"
    replicas: int = 2
    image: str = "nginx:latest"
    port: int = 80
    additional: str | None = None


class HelmRequest(BaseModel):
    """Request for Helm chart generation."""

    description: str
    chart_name: str = "my-chart"
    app_version: str = "1.0.0"
    chart_version: str = "0.1.0"
    features: list[str] = ["deployment", "service"]
    environment: str = "production"


class DeploymentRequest(BaseModel):
    """Request for deployment planning."""

    action: str = "deploy"
    app_name: str
    namespace: str = "default"
    current_state: dict[str, Any] | None = None
    target_state: dict[str, Any] | None = None
    environment: str = "production"
    risk_tolerance: str = "low"


class AnalysisRequest(BaseModel):
    """Request for infrastructure analysis."""

    resources: list[dict[str, Any]] | None = None
    metrics: dict[str, Any] | None = None
    namespace: str = "default"
    cloud_provider: str = "oracle"
    budget: str | None = None


class BlueprintResponse(BaseModel):
    """Standard blueprint response."""

    success: bool
    artifacts: dict[str, str]
    message: str
    warnings: list[str] = []
    recommendations: list[str] = []


@router.get("/")
async def list_blueprints() -> dict[str, Any]:
    """List all available blueprints and their capabilities."""
    return {
        "blueprints": orchestrator.get_available_blueprints(),
        "version": "1.0.0",
    }


@router.post("/k8s/generate", response_model=BlueprintResponse)
async def generate_k8s_manifests(request: K8sRequest) -> BlueprintResponse:
    """
    Generate Kubernetes manifests from natural language description.

    Returns YAML manifests for deployments, services, and other resources.
    """
    result = await orchestrator.generate_k8s_manifests(
        description=request.description,
        app_name=request.app_name,
        namespace=request.namespace,
        replicas=request.replicas,
        image=request.image,
        port=request.port,
        additional=request.additional,
    )

    return BlueprintResponse(
        success=result.success,
        artifacts=result.artifacts,
        message=result.message,
        warnings=result.warnings,
        recommendations=result.recommendations,
    )


@router.post("/k8s/generate/yaml")
async def generate_k8s_yaml(request: K8sRequest) -> PlainTextResponse:
    """
    Generate Kubernetes manifests and return combined YAML.
    """
    result = await orchestrator.generate_k8s_manifests(
        description=request.description,
        app_name=request.app_name,
        namespace=request.namespace,
        replicas=request.replicas,
        image=request.image,
        port=request.port,
        additional=request.additional,
    )

    if not result.success:
        return PlainTextResponse(
            content=f"# Error: {result.message}",
            status_code=400,
        )

    yaml_content = result.artifacts.get(
        "all-resources.yaml", "# No resources generated"
    )
    return PlainTextResponse(content=yaml_content, media_type="text/yaml")


@router.post("/helm/generate", response_model=BlueprintResponse)
async def generate_helm_chart(request: HelmRequest) -> BlueprintResponse:
    """
    Generate a complete Helm chart from natural language description.

    Returns Chart.yaml, values.yaml, and templates.
    """
    result = await orchestrator.generate_helm_chart(
        description=request.description,
        chart_name=request.chart_name,
        app_version=request.app_version,
        chart_version=request.chart_version,
        features=request.features,
        environment=request.environment,
    )

    return BlueprintResponse(
        success=result.success,
        artifacts=result.artifacts,
        message=result.message,
        warnings=result.warnings,
        recommendations=result.recommendations,
    )


@router.post("/deploy/plan", response_model=BlueprintResponse)
async def plan_deployment(request: DeploymentRequest) -> BlueprintResponse:
    """
    Generate deployment plan and runbook.

    Returns deployment commands, pre/post checks, and rollback plan.
    """
    result = await orchestrator.plan_deployment(
        action=request.action,
        app_name=request.app_name,
        namespace=request.namespace,
        current_state=request.current_state or {},
        target_state=request.target_state or {},
        environment=request.environment,
        risk_tolerance=request.risk_tolerance,
    )

    return BlueprintResponse(
        success=result.success,
        artifacts=result.artifacts,
        message=result.message,
        warnings=result.warnings,
        recommendations=result.recommendations,
    )


@router.post("/analyze", response_model=BlueprintResponse)
async def analyze_infrastructure(request: AnalysisRequest) -> BlueprintResponse:
    """
    Analyze infrastructure and get optimization recommendations.

    Returns cost analysis, security audit, and performance insights.
    """
    result = await orchestrator.analyze_infrastructure(
        resources=request.resources,
        metrics=request.metrics or {},
        namespace=request.namespace,
        cloud_provider=request.cloud_provider,
        budget=request.budget,
    )

    return BlueprintResponse(
        success=result.success,
        artifacts=result.artifacts,
        message=result.message,
        warnings=result.warnings,
        recommendations=result.recommendations,
    )


@router.post("/full-stack", response_model=dict[str, BlueprintResponse])
async def generate_full_stack(request: K8sRequest) -> dict[str, BlueprintResponse]:
    """
    Generate complete infrastructure stack in parallel.

    Returns K8s manifests, Helm chart, and deployment plan.
    """
    results = await orchestrator.full_stack_generation(
        description=request.description,
        app_name=request.app_name,
        namespace=request.namespace,
        replicas=request.replicas,
        image=request.image,
        port=request.port,
    )

    return {
        name: BlueprintResponse(
            success=result.success,
            artifacts=result.artifacts,
            message=result.message,
            warnings=result.warnings,
            recommendations=result.recommendations,
        )
        for name, result in results.items()
    }
