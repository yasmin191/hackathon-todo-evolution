"""
Task Organizer Skill

Organizes tasks by:
- Grouping related tasks
- Suggesting categories/projects
- Recommending task order
- Identifying duplicates
- Batch operations suggestions
"""

import json
import os
from typing import Any

from openai import OpenAI

from .base import BaseSkill, SkillResult


class TaskOrganizerSkill(BaseSkill):
    """Skill for organizing and grouping tasks."""

    name = "task_organizer"
    description = (
        "Organizes tasks into groups, suggests categories, and identifies patterns"
    )
    version = "1.0.0"

    @property
    def system_prompt(self) -> str:
        return """You are a Task Organization Expert. Your job is to help organize tasks effectively.

When given a list of tasks, analyze and return a JSON object with:
{
    "groups": [
        {
            "name": "Group Name",
            "description": "Why these tasks are grouped",
            "task_ids": [1, 2, 3],
            "suggested_order": [2, 1, 3],
            "group_priority": "high" | "medium" | "low"
        }
    ],
    "potential_duplicates": [
        {
            "task_ids": [1, 5],
            "similarity_reason": "Both involve X",
            "recommendation": "merge" | "keep_both" | "review"
        }
    ],
    "suggested_projects": [
        {
            "name": "Project Name",
            "task_ids": [1, 2, 3],
            "rationale": "Why these form a project"
        }
    ],
    "batch_suggestions": [
        {
            "action": "set_priority" | "add_tag" | "set_due_date",
            "task_ids": [1, 2],
            "value": "high",
            "reason": "Why this batch action"
        }
    ],
    "workflow_suggestion": "Overall recommendation for task workflow"
}

Focus on actionable, practical organization."""

    def get_capabilities(self) -> list[str]:
        return [
            "task_grouping",
            "duplicate_detection",
            "project_suggestion",
            "batch_operations",
            "workflow_optimization",
            "priority_balancing",
        ]

    async def execute(self, input_data: dict[str, Any]) -> SkillResult:
        """Organize a list of tasks."""
        tasks = input_data.get("tasks", [])

        if not tasks:
            return SkillResult(
                success=False,
                data=None,
                message="No tasks provided for organization",
            )

        if len(tasks) < 2:
            return SkillResult(
                success=True,
                data={"groups": [], "message": "Need at least 2 tasks to organize"},
                message="Single task - no organization needed",
            )

        try:
            client = OpenAI(api_key=self.openai_api_key or os.getenv("OPENAI_API_KEY"))

            tasks_text = "\n".join(
                [
                    f"- ID {t.get('id', i)}: {t.get('title', 'Untitled')} "
                    f"(Priority: {t.get('priority', 'medium')}, "
                    f"Tags: {t.get('tags', [])}, "
                    f"Status: {'completed' if t.get('completed') else 'pending'})"
                    for i, t in enumerate(tasks)
                ]
            )

            user_prompt = f"""Organize these {len(tasks)} tasks:

{tasks_text}

Provide organization suggestions as JSON."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            organization = json.loads(response.choices[0].message.content or "{}")

            suggestions = []
            if organization.get("groups"):
                suggestions.append(f"Found {len(organization['groups'])} task groups")
            if organization.get("potential_duplicates"):
                suggestions.append(
                    f"Detected {len(organization['potential_duplicates'])} potential duplicates"
                )
            if organization.get("suggested_projects"):
                suggestions.append(
                    f"Suggested {len(organization['suggested_projects'])} projects"
                )

            return SkillResult(
                success=True,
                data=organization,
                message="Tasks organized successfully",
                confidence=0.80,
                suggestions=suggestions
                or ["Tasks analyzed - no major reorganization needed"],
            )

        except Exception as e:
            return SkillResult(
                success=False,
                data=None,
                message=f"Organization failed: {str(e)}",
            )
