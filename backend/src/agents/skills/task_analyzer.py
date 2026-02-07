"""
Task Analyzer Skill

Analyzes tasks to provide:
- Complexity assessment (simple, moderate, complex)
- Priority suggestions based on content analysis
- Time estimates
- Dependency detection
- Risk assessment
"""

import json
import os
from typing import Any

from openai import OpenAI

from .base import BaseSkill, SkillResult


class TaskAnalyzerSkill(BaseSkill):
    """Skill for analyzing tasks and providing insights."""

    name = "task_analyzer"
    description = "Analyzes tasks for complexity, priority, and time estimates"
    version = "1.0.0"

    @property
    def system_prompt(self) -> str:
        return """You are a Task Analysis Expert. Your job is to analyze tasks and provide structured insights.

For each task, analyze and return a JSON object with:
{
    "complexity": "simple" | "moderate" | "complex",
    "complexity_reasons": ["reason1", "reason2"],
    "suggested_priority": "low" | "medium" | "high" | "urgent",
    "priority_reasons": ["reason1", "reason2"],
    "estimated_minutes": number,
    "time_estimation_basis": "string explaining the estimate",
    "potential_blockers": ["blocker1", "blocker2"],
    "suggested_subtasks": ["subtask1", "subtask2"],
    "tags_suggested": ["tag1", "tag2"],
    "risk_level": "low" | "medium" | "high",
    "risk_factors": ["factor1", "factor2"]
}

Be concise but thorough. Base estimates on typical scenarios."""

    def get_capabilities(self) -> list[str]:
        return [
            "complexity_assessment",
            "priority_suggestion",
            "time_estimation",
            "blocker_detection",
            "subtask_generation",
            "tag_suggestion",
            "risk_assessment",
        ]

    async def execute(self, input_data: dict[str, Any]) -> SkillResult:
        """Analyze a task and return insights."""
        title = input_data.get("title", "")
        description = input_data.get("description", "")
        context = input_data.get("context", {})

        if not title:
            return SkillResult(
                success=False,
                data=None,
                message="Task title is required for analysis",
            )

        try:
            client = OpenAI(api_key=self.openai_api_key or os.getenv("OPENAI_API_KEY"))

            user_prompt = f"""Analyze this task:

Title: {title}
Description: {description or "No description provided"}

Additional context:
- Existing tags: {context.get("existing_tags", [])}
- Current priority: {context.get("current_priority", "not set")}
- Due date: {context.get("due_date", "not set")}
- Related tasks count: {context.get("related_tasks_count", 0)}

Provide your analysis as JSON."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            analysis = json.loads(response.choices[0].message.content or "{}")

            return SkillResult(
                success=True,
                data=analysis,
                message="Task analyzed successfully",
                confidence=0.85,
                suggestions=[
                    f"Suggested priority: {analysis.get('suggested_priority', 'medium')}",
                    f"Estimated time: {analysis.get('estimated_minutes', 30)} minutes",
                    f"Complexity: {analysis.get('complexity', 'moderate')}",
                ],
            )

        except Exception as e:
            return SkillResult(
                success=False,
                data=None,
                message=f"Analysis failed: {str(e)}",
            )
