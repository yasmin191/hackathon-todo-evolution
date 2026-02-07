"""
Natural Language Processor Skill

Handles natural language understanding:
- Parse task descriptions into structured data
- Extract dates, priorities, tags from text
- Intent classification
- Multi-language support (English, Urdu)
- Context-aware parsing
"""

import json
import os
from typing import Any

from openai import OpenAI

from .base import BaseSkill, SkillResult


class NaturalLanguageProcessorSkill(BaseSkill):
    """Skill for natural language processing of task inputs."""

    name = "nlp_processor"
    description = (
        "Parses natural language into structured task data with multi-language support"
    )
    version = "1.0.0"

    @property
    def system_prompt(self) -> str:
        return """You are a Natural Language Processing Expert for a task management system.

Parse user input (in English or Urdu) and extract structured task information.

Return a JSON object with:
{
    "detected_language": "en" | "ur",
    "intent": "create_task" | "update_task" | "delete_task" | "list_tasks" | "complete_task" | "search" | "schedule" | "other",
    "confidence": 0.95,
    "extracted_data": {
        "title": "Extracted task title",
        "title_ur": "Urdu translation if applicable",
        "description": "Extracted description",
        "description_ur": "Urdu translation if applicable",
        "priority": "low" | "medium" | "high" | "urgent" | null,
        "due_date": "YYYY-MM-DD" | null,
        "due_time": "HH:MM" | null,
        "relative_date": "tomorrow" | "next week" | etc,
        "tags": ["tag1", "tag2"],
        "recurrence": "daily" | "weekly" | "monthly" | null,
        "task_id": null or number if updating/deleting
    },
    "entities": [
        {"type": "date", "value": "tomorrow", "normalized": "2025-01-15"},
        {"type": "priority", "value": "urgent", "normalized": "urgent"},
        {"type": "tag", "value": "work", "normalized": "work"}
    ],
    "ambiguities": [
        {"field": "due_date", "options": ["today", "tomorrow"], "needs_clarification": true}
    ],
    "suggested_response": "Confirmation or clarification message in the detected language",
    "suggested_response_ur": "Urdu version if input was Urdu"
}

Handle common patterns:
- "remind me to X tomorrow" → create task with due date
- "کل مجھے X یاد دلانا" → same in Urdu
- "urgent: complete report" → high priority task
- "every Monday: team meeting" → recurring task
- "#work buy supplies" → task with tag"""

    def get_capabilities(self) -> list[str]:
        return [
            "intent_classification",
            "entity_extraction",
            "date_parsing",
            "priority_detection",
            "tag_extraction",
            "multi_language",
            "urdu_support",
            "context_awareness",
        ]

    async def execute(self, input_data: dict[str, Any]) -> SkillResult:
        """Parse natural language input into structured task data."""
        text = input_data.get("text", "")
        context = input_data.get("context", {})
        preferred_language = input_data.get("preferred_language", "en")

        if not text:
            return SkillResult(
                success=False,
                data=None,
                message="No text provided for parsing",
            )

        try:
            client = OpenAI(api_key=self.openai_api_key or os.getenv("OPENAI_API_KEY"))

            context_text = ""
            if context:
                context_text = f"""
Context:
- Current date: {context.get("current_date", "unknown")}
- User timezone: {context.get("timezone", "UTC")}
- Existing tags: {context.get("existing_tags", [])}
- Recent tasks: {context.get("recent_tasks", [])}
"""

            user_prompt = f"""Parse this user input:

"{text}"

{context_text}
User's preferred language: {preferred_language}

Extract structured data as JSON."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )

            parsed = json.loads(response.choices[0].message.content or "{}")

            suggestions = []
            intent = parsed.get("intent", "other")
            if intent == "create_task":
                title = parsed.get("extracted_data", {}).get("title", "")
                suggestions.append(f"Creating task: {title}")

            ambiguities = parsed.get("ambiguities", [])
            if ambiguities:
                suggestions.append(f"Note: {len(ambiguities)} items need clarification")

            lang = parsed.get("detected_language", "en")
            if lang == "ur":
                suggestions.append(
                    "Urdu input detected - response available in both languages"
                )

            return SkillResult(
                success=True,
                data=parsed,
                message=parsed.get("suggested_response", "Input parsed successfully"),
                confidence=parsed.get("confidence", 0.8),
                suggestions=suggestions,
            )

        except Exception as e:
            return SkillResult(
                success=False,
                data=None,
                message=f"NLP parsing failed: {str(e)}",
            )
