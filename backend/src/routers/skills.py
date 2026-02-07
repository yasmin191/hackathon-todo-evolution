"""
Skills API Router

Exposes AI skills as REST endpoints for:
- Task analysis
- Task organization
- Scheduling suggestions
- Productivity coaching
- Natural language processing
"""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..agents.skills import SkillOrchestrator

router = APIRouter(prefix="/skills", tags=["Skills"])

# Initialize orchestrator
orchestrator = SkillOrchestrator()


class NLPRequest(BaseModel):
    """Request for natural language processing."""

    text: str
    language: str = "en"
    context: dict[str, Any] | None = None


class TaskAnalysisRequest(BaseModel):
    """Request for task analysis."""

    title: str
    description: str | None = None
    context: dict[str, Any] | None = None


class TasksRequest(BaseModel):
    """Request with multiple tasks."""

    tasks: list[dict[str, Any]]
    preferences: dict[str, Any] | None = None


class ProductivityRequest(BaseModel):
    """Request for productivity insights."""

    task_history: list[dict[str, Any]]
    goals: list[str] | None = None


class SkillResponse(BaseModel):
    """Standard skill response."""

    success: bool
    data: Any | None
    message: str
    confidence: float = 1.0
    suggestions: list[str] | None = None


@router.get("/")
async def list_skills() -> dict[str, Any]:
    """List all available skills and their capabilities."""
    return {
        "skills": orchestrator.get_available_skills(),
        "version": "1.0.0",
    }


@router.post("/nlp/parse", response_model=SkillResponse)
async def parse_natural_language(request: NLPRequest) -> SkillResponse:
    """
    Parse natural language input into structured task data.

    Supports English and Urdu.
    """
    result = await orchestrator.process_natural_language(
        text=request.text,
        context=request.context,
        language=request.language,
    )

    return SkillResponse(
        success=result.success,
        data=result.data,
        message=result.message,
        confidence=result.confidence,
        suggestions=result.suggestions,
    )


@router.post("/analyze", response_model=SkillResponse)
async def analyze_task(request: TaskAnalysisRequest) -> SkillResponse:
    """
    Analyze a task for complexity, priority suggestions, and time estimates.
    """
    result = await orchestrator.analyze_task(
        {
            "title": request.title,
            "description": request.description,
            **(request.context or {}),
        }
    )

    return SkillResponse(
        success=result.success,
        data=result.data,
        message=result.message,
        confidence=result.confidence,
        suggestions=result.suggestions,
    )


@router.post("/organize", response_model=SkillResponse)
async def organize_tasks(request: TasksRequest) -> SkillResponse:
    """
    Organize tasks into groups, detect duplicates, and suggest projects.
    """
    result = await orchestrator.organize_tasks(request.tasks)

    return SkillResponse(
        success=result.success,
        data=result.data,
        message=result.message,
        confidence=result.confidence,
        suggestions=result.suggestions,
    )


@router.post("/schedule", response_model=SkillResponse)
async def schedule_tasks(request: TasksRequest) -> SkillResponse:
    """
    Generate intelligent scheduling suggestions for tasks.
    """
    result = await orchestrator.schedule_tasks(
        tasks=request.tasks,
        preferences=request.preferences,
    )

    return SkillResponse(
        success=result.success,
        data=result.data,
        message=result.message,
        confidence=result.confidence,
        suggestions=result.suggestions,
    )


@router.post("/productivity", response_model=SkillResponse)
async def get_productivity_insights(request: ProductivityRequest) -> SkillResponse:
    """
    Get productivity coaching and insights based on task history.
    """
    result = await orchestrator.get_productivity_insights(
        task_history=request.task_history,
        goals=request.goals,
    )

    return SkillResponse(
        success=result.success,
        data=result.data,
        message=result.message,
        confidence=result.confidence,
        suggestions=result.suggestions,
    )


@router.post("/comprehensive", response_model=dict[str, SkillResponse])
async def comprehensive_analysis(request: TasksRequest) -> dict[str, SkillResponse]:
    """
    Run all skills in parallel for comprehensive task analysis.

    Returns results from organization, scheduling, and individual task analysis.
    """
    results = await orchestrator.comprehensive_analysis(
        tasks=request.tasks,
        task_history=request.preferences.get("task_history")
        if request.preferences
        else None,
    )

    return {
        name: SkillResponse(
            success=result.success,
            data=result.data,
            message=result.message,
            confidence=result.confidence,
            suggestions=result.suggestions,
        )
        for name, result in results.items()
    }
