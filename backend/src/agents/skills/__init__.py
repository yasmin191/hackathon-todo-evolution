"""
Reusable AI Skills for Task Management

This module provides reusable, composable AI skills (subagents) that can be
orchestrated by the main task agent. Each skill is a specialized mini-agent
that handles a specific domain of task management.

Skills:
- TaskAnalyzer: Analyzes tasks for complexity, priority suggestions, and time estimates
- TaskOrganizer: Groups, categorizes, and suggests task organization strategies
- TaskScheduler: Handles scheduling, reminders, and recurring task management
- ProductivityCoach: Provides productivity insights and recommendations
- NaturalLanguageProcessor: Parses natural language into structured task data
"""

from .base import BaseSkill, SkillResult
from .nlp_processor import NaturalLanguageProcessorSkill
from .orchestrator import SkillOrchestrator
from .productivity_coach import ProductivityCoachSkill
from .task_analyzer import TaskAnalyzerSkill
from .task_organizer import TaskOrganizerSkill
from .task_scheduler import TaskSchedulerSkill

__all__ = [
    "BaseSkill",
    "SkillResult",
    "TaskAnalyzerSkill",
    "TaskOrganizerSkill",
    "TaskSchedulerSkill",
    "ProductivityCoachSkill",
    "NaturalLanguageProcessorSkill",
    "SkillOrchestrator",
]
