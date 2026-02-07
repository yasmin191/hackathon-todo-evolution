"""
Productivity Coach Skill

Provides productivity insights:
- Completion rate analysis
- Productivity patterns
- Personalized tips
- Goal tracking
- Motivation and encouragement
"""

import json
import os
from typing import Any

from openai import OpenAI

from .base import BaseSkill, SkillResult


class ProductivityCoachSkill(BaseSkill):
    """Skill for productivity coaching and insights."""

    name = "productivity_coach"
    description = "Analyzes productivity patterns and provides personalized coaching"
    version = "1.0.0"

    @property
    def system_prompt(self) -> str:
        return """You are a Productivity Coach. Your job is to help users improve their task completion and work habits.

Analyze the user's task history and return a JSON object with:
{
    "productivity_score": 85,
    "score_breakdown": {
        "completion_rate": 90,
        "on_time_rate": 80,
        "consistency": 85
    },
    "patterns": {
        "most_productive_day": "Tuesday",
        "most_productive_time": "morning",
        "average_tasks_per_day": 5,
        "average_completion_time_minutes": 45
    },
    "strengths": [
        "Consistent daily task completion",
        "Good at breaking down large tasks"
    ],
    "areas_for_improvement": [
        "High-priority tasks sometimes delayed",
        "Evening productivity drops"
    ],
    "personalized_tips": [
        {
            "tip": "Try tackling urgent tasks first thing in the morning",
            "reason": "Your data shows higher completion rates before noon",
            "impact": "high"
        }
    ],
    "weekly_goals": [
        {
            "goal": "Complete 3 high-priority tasks",
            "current_progress": 1,
            "target": 3
        }
    ],
    "motivational_message": "A positive, encouraging message based on their performance",
    "streak_info": {
        "current_streak": 5,
        "longest_streak": 12,
        "streak_type": "days with completed tasks"
    }
}

Be encouraging but honest. Focus on actionable improvements."""

    def get_capabilities(self) -> list[str]:
        return [
            "productivity_scoring",
            "pattern_analysis",
            "personalized_coaching",
            "goal_tracking",
            "streak_tracking",
            "motivational_support",
        ]

    async def execute(self, input_data: dict[str, Any]) -> SkillResult:
        """Analyze productivity and provide coaching."""
        task_history = input_data.get("task_history", [])
        user_goals = input_data.get("goals", [])
        time_range = input_data.get("time_range", "last_week")

        if not task_history:
            return SkillResult(
                success=True,
                data={
                    "productivity_score": 0,
                    "message": "No task history yet - start adding tasks to get insights!",
                    "motivational_message": "Every journey begins with a single step. Add your first task and let's build great habits together!",
                },
                message="No history available for analysis",
                suggestions=["Start tracking tasks to unlock productivity insights"],
            )

        try:
            client = OpenAI(api_key=self.openai_api_key or os.getenv("OPENAI_API_KEY"))

            # Summarize task history
            total_tasks = len(task_history)
            completed = sum(1 for t in task_history if t.get("completed"))
            completion_rate = (completed / total_tasks * 100) if total_tasks > 0 else 0

            history_text = f"""
Task Statistics ({time_range}):
- Total tasks: {total_tasks}
- Completed: {completed}
- Completion rate: {completion_rate:.1f}%

Recent tasks (last 10):
"""
            for t in task_history[-10:]:
                status = "Completed" if t.get("completed") else "Pending"
                history_text += f"- {t.get('title', 'Untitled')} [{status}] (Priority: {t.get('priority', 'medium')})\n"

            if user_goals:
                history_text += f"\nUser goals: {user_goals}"

            user_prompt = f"""Analyze this user's productivity:

{history_text}

Provide coaching insights as JSON."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.5,
                response_format={"type": "json_object"},
            )

            coaching = json.loads(response.choices[0].message.content or "{}")

            suggestions = []
            score = coaching.get("productivity_score", 0)
            if score >= 80:
                suggestions.append("Great productivity! Keep up the excellent work")
            elif score >= 60:
                suggestions.append(
                    "Good progress - a few improvements can boost your score"
                )
            else:
                suggestions.append("Let's work on building better task habits together")

            tips = coaching.get("personalized_tips", [])
            if tips:
                suggestions.append(f"Top tip: {tips[0].get('tip', '')}")

            return SkillResult(
                success=True,
                data=coaching,
                message=coaching.get("motivational_message", "Keep going!"),
                confidence=0.80,
                suggestions=suggestions,
            )

        except Exception as e:
            return SkillResult(
                success=False,
                data=None,
                message=f"Coaching analysis failed: {str(e)}",
            )
