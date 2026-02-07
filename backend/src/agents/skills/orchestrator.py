"""
Skill Orchestrator

Coordinates multiple skills to handle complex task management requests.
Acts as the main entry point for skill-based task processing.
"""

import asyncio
from typing import Any

from .base import SkillResult
from .nlp_processor import NaturalLanguageProcessorSkill
from .productivity_coach import ProductivityCoachSkill
from .task_analyzer import TaskAnalyzerSkill
from .task_organizer import TaskOrganizerSkill
from .task_scheduler import TaskSchedulerSkill


class SkillOrchestrator:
    """
    Orchestrates multiple AI skills for comprehensive task management.

    The orchestrator can:
    - Route requests to appropriate skills
    - Combine results from multiple skills
    - Handle skill failures gracefully
    - Provide unified responses
    """

    def __init__(self, openai_api_key: str | None = None):
        self.openai_api_key = openai_api_key

        # Initialize all skills
        self.skills = {
            "analyzer": TaskAnalyzerSkill(openai_api_key),
            "organizer": TaskOrganizerSkill(openai_api_key),
            "scheduler": TaskSchedulerSkill(openai_api_key),
            "coach": ProductivityCoachSkill(openai_api_key),
            "nlp": NaturalLanguageProcessorSkill(openai_api_key),
        }

    async def process_natural_language(
        self,
        text: str,
        context: dict[str, Any] | None = None,
        language: str = "en",
    ) -> SkillResult:
        """
        Process natural language input and route to appropriate skills.

        This is the main entry point for chatbot interactions.
        """
        # First, parse the natural language input
        nlp_result = await self.skills["nlp"].execute(
            {
                "text": text,
                "context": context or {},
                "preferred_language": language,
            }
        )

        if not nlp_result.success:
            return nlp_result

        parsed_data = nlp_result.data or {}
        intent = parsed_data.get("intent", "other")
        extracted = parsed_data.get("extracted_data", {})

        # Based on intent, invoke additional skills
        additional_insights = {}

        if intent == "create_task" and extracted.get("title"):
            # Analyze the new task
            analysis = await self.skills["analyzer"].execute(
                {
                    "title": extracted.get("title", ""),
                    "description": extracted.get("description", ""),
                    "context": context or {},
                }
            )
            if analysis.success:
                additional_insights["analysis"] = analysis.data

        elif intent == "list_tasks" or intent == "search":
            # If we have task context, provide organization suggestions
            tasks = (context or {}).get("tasks", [])
            if tasks:
                org_result = await self.skills["organizer"].execute({"tasks": tasks})
                if org_result.success:
                    additional_insights["organization"] = org_result.data

        # Combine results
        return SkillResult(
            success=True,
            data={
                "parsed": parsed_data,
                "insights": additional_insights,
            },
            message=nlp_result.message,
            confidence=nlp_result.confidence,
            suggestions=nlp_result.suggestions,
        )

    async def analyze_task(self, task: dict[str, Any]) -> SkillResult:
        """Analyze a single task for complexity, priority, etc."""
        return await self.skills["analyzer"].execute(
            {
                "title": task.get("title", ""),
                "description": task.get("description", ""),
                "context": {
                    "existing_tags": task.get("tags", []),
                    "current_priority": task.get("priority"),
                    "due_date": task.get("due_date"),
                },
            }
        )

    async def organize_tasks(self, tasks: list[dict[str, Any]]) -> SkillResult:
        """Organize a list of tasks into groups and projects."""
        return await self.skills["organizer"].execute({"tasks": tasks})

    async def schedule_tasks(
        self,
        tasks: list[dict[str, Any]],
        preferences: dict[str, Any] | None = None,
    ) -> SkillResult:
        """Generate scheduling suggestions for tasks."""
        return await self.skills["scheduler"].execute(
            {
                "tasks": tasks,
                "preferences": preferences or {},
            }
        )

    async def get_productivity_insights(
        self,
        task_history: list[dict[str, Any]],
        goals: list[str] | None = None,
    ) -> SkillResult:
        """Get productivity coaching and insights."""
        return await self.skills["coach"].execute(
            {
                "task_history": task_history,
                "goals": goals or [],
            }
        )

    async def comprehensive_analysis(
        self,
        tasks: list[dict[str, Any]],
        task_history: list[dict[str, Any]] | None = None,
    ) -> dict[str, SkillResult]:
        """
        Run all skills in parallel for comprehensive task analysis.

        Returns results from all skills.
        """
        results = {}

        # Run skills in parallel
        skill_calls = [
            ("organization", self.skills["organizer"].execute({"tasks": tasks})),
            ("scheduling", self.skills["scheduler"].execute({"tasks": tasks})),
        ]

        if task_history:
            skill_calls.append(
                (
                    "productivity",
                    self.skills["coach"].execute({"task_history": task_history}),
                )
            )

        # Analyze first 5 tasks individually
        for i, task in enumerate(tasks[:5]):
            skill_calls.append(
                (
                    f"task_analysis_{i}",
                    self.skills["analyzer"].execute(
                        {
                            "title": task.get("title", ""),
                            "description": task.get("description", ""),
                        }
                    ),
                )
            )

        # Execute all in parallel
        call_results = await asyncio.gather(
            *[call[1] for call in skill_calls],
            return_exceptions=True,
        )

        # Collect results
        for (name, _), result in zip(skill_calls, call_results):
            if isinstance(result, Exception):
                results[name] = SkillResult(
                    success=False,
                    data=None,
                    message=f"Skill failed: {str(result)}",
                )
            else:
                results[name] = result

        return results

    def get_available_skills(self) -> list[dict[str, Any]]:
        """Get information about all available skills."""
        return [
            {
                "name": skill.name,
                "description": skill.description,
                "version": skill.version,
                "capabilities": skill.get_capabilities(),
            }
            for skill in self.skills.values()
        ]
