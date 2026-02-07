"""
Task Scheduler Skill

Handles scheduling intelligence:
- Optimal time slot suggestions
- Recurring task pattern detection
- Deadline risk assessment
- Workload balancing
- Calendar integration suggestions
"""

import json
import os
from datetime import datetime
from typing import Any

from openai import OpenAI

from .base import BaseSkill, SkillResult


class TaskSchedulerSkill(BaseSkill):
    """Skill for intelligent task scheduling."""

    name = "task_scheduler"
    description = "Provides intelligent scheduling suggestions and deadline management"
    version = "1.0.0"

    @property
    def system_prompt(self) -> str:
        return """You are a Task Scheduling Expert. Your job is to help schedule tasks optimally.

Analyze tasks and return a JSON object with:
{
    "schedule_suggestions": [
        {
            "task_id": 1,
            "suggested_date": "YYYY-MM-DD",
            "suggested_time": "HH:MM",
            "duration_minutes": 60,
            "reason": "Why this time slot",
            "flexibility": "fixed" | "flexible" | "anytime"
        }
    ],
    "deadline_risks": [
        {
            "task_id": 1,
            "risk_level": "low" | "medium" | "high" | "critical",
            "days_until_due": 3,
            "recommendation": "Action to take"
        }
    ],
    "recurring_patterns": [
        {
            "task_ids": [1, 5, 9],
            "pattern": "daily" | "weekly" | "monthly" | "custom",
            "pattern_description": "Every Monday at 9am",
            "confidence": 0.85
        }
    ],
    "workload_analysis": {
        "today": {"task_count": 5, "total_minutes": 180, "status": "manageable" | "heavy" | "overloaded"},
        "this_week": {"task_count": 15, "total_minutes": 600, "status": "manageable"},
        "recommendations": ["Spread high-priority tasks", "Consider delegating"]
    },
    "optimal_order": [
        {"task_id": 1, "order": 1, "reason": "Start with high-energy task"}
    ]
}

Consider task priorities, deadlines, and realistic time estimates."""

    def get_capabilities(self) -> list[str]:
        return [
            "schedule_optimization",
            "deadline_monitoring",
            "pattern_detection",
            "workload_analysis",
            "time_blocking",
            "priority_sequencing",
        ]

    async def execute(self, input_data: dict[str, Any]) -> SkillResult:
        """Generate scheduling suggestions for tasks."""
        tasks = input_data.get("tasks", [])
        current_date = input_data.get("current_date", datetime.now().isoformat())
        preferences = input_data.get("preferences", {})

        if not tasks:
            return SkillResult(
                success=False,
                data=None,
                message="No tasks provided for scheduling",
            )

        try:
            client = OpenAI(api_key=self.openai_api_key or os.getenv("OPENAI_API_KEY"))

            tasks_text = "\n".join(
                [
                    f"- ID {t.get('id', i)}: {t.get('title', 'Untitled')} "
                    f"(Priority: {t.get('priority', 'medium')}, "
                    f"Due: {t.get('due_date', 'not set')}, "
                    f"Estimated: {t.get('estimated_minutes', 30)} min, "
                    f"Recurring: {t.get('recurrence_rule', 'none')})"
                    for i, t in enumerate(tasks)
                ]
            )

            prefs_text = f"""
Work hours: {preferences.get("work_hours", "9am-5pm")}
Preferred focus time: {preferences.get("focus_time", "morning")}
Break preference: {preferences.get("break_duration", "15")} minutes between tasks
"""

            user_prompt = f"""Schedule these tasks:

Current date/time: {current_date}

Tasks:
{tasks_text}

User preferences:
{prefs_text}

Provide scheduling suggestions as JSON."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            schedule = json.loads(response.choices[0].message.content or "{}")

            suggestions = []
            if schedule.get("deadline_risks"):
                high_risks = [
                    r
                    for r in schedule["deadline_risks"]
                    if r.get("risk_level") in ["high", "critical"]
                ]
                if high_risks:
                    suggestions.append(
                        f"Warning: {len(high_risks)} tasks at risk of missing deadline"
                    )

            workload = schedule.get("workload_analysis", {})
            if workload.get("today", {}).get("status") == "overloaded":
                suggestions.append(
                    "Today's workload is heavy - consider rescheduling some tasks"
                )

            if schedule.get("recurring_patterns"):
                suggestions.append(
                    f"Detected {len(schedule['recurring_patterns'])} recurring patterns"
                )

            return SkillResult(
                success=True,
                data=schedule,
                message="Schedule generated successfully",
                confidence=0.75,
                suggestions=suggestions or ["Schedule looks manageable"],
            )

        except Exception as e:
            return SkillResult(
                success=False,
                data=None,
                message=f"Scheduling failed: {str(e)}",
            )
